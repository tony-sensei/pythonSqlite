# pythonSqlite
1. installing packages by using  
'pip install -r requirements.txt'  

2. if using postgresql, running create_tables.py by  
'python3 create_tables.py' (drop table and check tables not useful)  
if using sqlite, changing the database_url to the upper line's code, and
do the following

3. running check_tables.py by  
'python3 check_tables.py'

4. ans_present.ipynb contains the distribution of the answers

# Data Analysis
1. the raw data is `datasets/testData1.csv`

2. use `datasets/testData1.csv` as the dataset for time series

3. run `latest_entry_generator.py` for getting the modified dataset 
`datasets/latest_scores.csv` from `data/testData1.csv` for get the 
latest entries for heatmap:
```bash
python3 latest_entry_generator.py
```

4. follow instructions in `ans_present.ipynb`