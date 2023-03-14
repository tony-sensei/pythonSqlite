import random
import csv

# Generate some random data
data = []
for i in range(100):
    row = [random.randint(0, 100) for _ in range(3)]
    data.append(row)

# Write the data to a CSV file
with open('data.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    for row in data:
        writer.writerow(row)