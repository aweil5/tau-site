import pandas as pd

number_table = pd.read_csv("number-sheet.csv")
for index, row in number_table.iterrows():
    print(row['Name'], row['Number'])