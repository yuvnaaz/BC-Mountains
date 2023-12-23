from bs4 import BeautifulSoup
import requests 
import pandas as pd

url = "https://www.onthesnow.com/british-columbia/skireport"
page = requests.get(url)
soup = BeautifulSoup(page.text, 'html.parser')

tables = soup.find_all('table')

all_data = []  # List to store all the data from tables

for i, table in enumerate(tables[:-1]):
    table_rows = table.find_all('tr')
    world_table_titles = [title.text.strip() for title in table_rows[0].find_all('th')]
    
    table_data = []
    for row in table_rows[1:]:
        row_data = [data.text.strip() for data in row.find_all('td')]
        table_data.append(row_data)
    
    df = pd.DataFrame(table_data, columns=world_table_titles)
    df.to_csv(f"table_{i + 1}.csv", index=False)
    print(f"Table {i + 1} data saved to table_{i + 1}.csv\n")
    
    all_data.append(df)

# Combine all DataFrames into a single DataFrame
combined_df = pd.concat(all_data, ignore_index=True)

# Save the combined DataFrame to a single CSV file
combined_df.to_csv("combined_data.csv", index=False)
print("Combined data saved to combined_data.csv")
