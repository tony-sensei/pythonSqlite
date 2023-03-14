from flask import Flask
import json
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///testDatabase.db'


db = SQLAlchemy(app)


class Survey(db.Model):
    __tablename__ = 'surveys'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    questions = db.relationship('Question', backref='survey', lazy='dynamic')

    def __init__(self, title):
        self.title = title

    @property
    def has_questions(self):
        return self.questions.count() > 0


class Question(db.Model):
    __tablename__ = 'questions'

    TEXT = 'text'
    NUMERIC = 'numeric'
    BOOLEAN = 'boolean'

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String, nullable=False)
    kind = db.Column(db.Enum(TEXT, NUMERIC, BOOLEAN, name='question_kind'))
    survey_id = db.Column(db.Integer, db.ForeignKey('surveys.id'))
    to_question_id = db.Column(db.Integer, db.ForeignKey('transitions.id'))
    to_question = db.relationship('Transition', foreign_keys=[to_question_id], backref='question')
    answers = db.relationship('Answer', backref='question', lazy='dynamic')

    def __init__(self, content, kind=TEXT):
        self.content = content
        self.kind = kind

    def next(self, session_id):
        transition = self.transitions.filter(Transition.session_id == session_id).first()
        if transition is not None:
            return transition.to_question
        else:
            return self.survey.questions.filter(Question.id > self.id).order_by('id').first()


class Transition(db.Model):
    __tablename__ = 'transitions'

    id = db.Column(db.Integer, primary_key=True)
    from_question_id = db.Column(db.Integer, db.ForeignKey('questions.id'))
    to_question_id = db.Column(db.Integer, db.ForeignKey('questions.id'))
    session_id = db.Column(db.String, nullable=False)

    from_question = db.relationship('Question', foreign_keys=[from_question_id],
                                    backref=db.backref('outgoing_transitions', lazy='dynamic'))
    to_question = db.relationship('Question', foreign_keys=[to_question_id],
                                  backref=db.backref('incoming_transitions', lazy='dynamic'))


class Answer(db.Model):
    __tablename__ = 'answers'

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String, nullable=False)
    session_id = db.Column(db.String, nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey('questions.id'))

    @classmethod
    def update_content(cls, session_id, question_id, content):
        existing_answer = cls.query.filter(
            Answer.session_id == session_id and Answer.question_id == question_id
        ).first()
        existing_answer.content = content
        db.session.add(existing_answer)
        db.session.commit()

    def __init__(self, content, question, session_id):
        self.content = content
        self.question = question
        self.session_id = session_id


if __name__ == '__main__':
    with app.app_context():
        # Create tables in the db
        db.create_all()

        # Load the JSON data from a file
        with open('survey.json') as survey_file:
            data = json.load(survey_file)

            # Create the survey and question objects and add them to the database
            survey = Survey(title=data['title'])
            db.session.add(survey)

            # Create the question objects and add them to
            # the survey and database, and create the transitions
            question_map = {}
            for question_data in data['questions']:
                question = Question(content=question_data['body'], kind=question_data['type'])
                survey.questions.append(question)
                db.session.add(question)
                question_map[question_data['name']] = question

            for question_data in data['questions']:
                # Create the transitions for this question
                if 'transition' in question_data:
                    transition_data = question_data['transition']
                    if transition_data['next'] == "-":
                        continue
                    from_question = question_map[question_data['name']]
                    to_question = question_map[transition_data['next']]
                    session_id = transition_data.get('session_id', '')
                    transition = Transition(from_question=from_question, to_question=to_question, session_id=session_id)
                    db.session.add(transition)

            db.session.commit()
