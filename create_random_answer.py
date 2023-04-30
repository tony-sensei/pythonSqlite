import os
import random
import csv

question_type = ['RSDQE', 'RSDQB', 'RSDQH', 'RSDQP']
color_dict = {
    'RSDQE': {
        range(0, 4): 'green',
        range(4, 5): 'orange',
        range(5, 11): 'red'
    },
    'RSDQB': {
        range(0, 3): 'green',
        range(3, 4): 'orange',
        range(4, 11): 'red'
    },
    'RSDQH': {
        range(0, 6): 'green',
        range(6, 7): 'orange',
        range(7, 11): 'red'
    },
    'RSDQP': {
        range(0, 3): 'green',
        range(3, 4): 'orange',
        range(4, 11): 'red'
    }
}


def check_light(type_prob, num):
    if type_prob not in color_dict:
        return 'invalid'

    for level_range, color in color_dict[type_prob].items():
        if num in level_range:
            return color

    return 'invalid'


# Generate some random data
data = []
num_of_participants = 1000

for i in range(num_of_participants):
    for j in range(4):
        type_question = question_type[j]
        random_number = random.randint(0, 10)
        row = [4*i+j, "+19493440720", 1000+i, type_question,
               random_number, check_light(type_question, random_number)]
        data.append(row)

# Define the column names
field_names = ['id', 'phone', 'child_id', 'name', 'score', 'light']

# Check if the file exists, and delete it if it does
if os.path.exists('datasets/data.csv'):
    os.remove('datasets/data.csv')

# Write the data to a CSV file
with open('datasets/data.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    # Write the column names
    writer.writerow(field_names)
    # Write the data rows
    for row in data:
        writer.writerow(row)
