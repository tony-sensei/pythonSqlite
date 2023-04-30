import pandas as pd

# Load the data into a pandas DataFrame
df = pd.read_csv("datasets/testData1.csv", parse_dates=['created_date'])

# Sort the DataFrame by 'created_date' in descending order
df_sorted = df.sort_values(by='created_date', ascending=False)

# Group by 'child_id' and 'name', and get the first (latest) record for each group
latest_scores = df_sorted.groupby(['child_id', 'name']).first().reset_index()

# Keep only the relevant columns 'child_id', 'name', and 'score'
latest_scores = latest_scores[['child_id', 'name', 'score']]

latest_scores.to_csv('datasets/latest_scores.csv', index=False)
