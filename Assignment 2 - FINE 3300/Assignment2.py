import pandas as pd
import os

#Define dataset filenames for different regions (list of CSV files to read)
csv_files = ['CANADA.csv', 'ONTARIO.csv', 'ALBERTA.csv', 'BC.csv', 'MANITOBA.csv', 
             'NB.csv', 'NL.csv', 'NS.csv', 'QUEBEC.csv', 'PEI.csv', 'SASK.csv']

#Store data from each file
data_frames = []

#Read/Process CSV files
for csv in csv_files:
    data = pd.read_csv(csv)
    
    #Remove extra spaces from column names
    data.columns = data.columns.str.strip()
    
    #Get the region name from the file name
    region_name = os.path.splitext(csv)[0].upper()
    
    #Add a new column for the region
    data['Jurisdiction'] = region_name
    
    #Save the processed data
    data_frames.append(data)

#List to store formatted data
reshaped_data = []

#Convert data into a better format
for dataset in data_frames:
    tidy_data = dataset.melt(id_vars=['Item', 'Jurisdiction'], var_name='Month', value_name='CPI')
    
    #Arrange columns
    tidy_data = tidy_data[['Item', 'Month', 'Jurisdiction', 'CPI']]
    
    reshaped_data.append(tidy_data)

#Combine all data into one table
final_dataset = pd.concat(reshaped_data, ignore_index=True)

#The final result
print("Final Dataset Columns:", final_dataset.columns.tolist())

print(final_dataset.head(12))


#QUESTIONS
#Question 1: For Canada and each of the provinces, report the average month-to-month change in food, shelter, All-items excluding food and energy. 
    #Report your numbers as a percent up to one decimal place.
print("\nQuestion 1: Average Month to Month change in Food, Shelter, All-items excluding food and energy.")
#Convert the Month column to a proper datetime format
final_dataset['Month'] = pd.to_datetime(final_dataset['Month'], format='%y-%b') 

#Sorting by Jurisdiction, Item, and Month
final_dataset = final_dataset.sort_values(by=['Jurisdiction', 'Item', 'Month'])

#Filter relevant items
selected_items = ["Food", "Shelter", "All-items excluding food and energy"]
filtered_data = final_dataset[final_dataset['Item'].isin(selected_items)].copy()

#Compute month-to-month percentage change
filtered_data['CPI_change'] = filtered_data.groupby(['Jurisdiction', 'Item'])['CPI'].pct_change() * 100

#Compute the average percentage change for each category in each jurisdiction
average_changes = filtered_data.groupby(['Jurisdiction', 'Item'])['CPI_change'].mean().unstack()    
average_changes = average_changes.round(1).astype(str) + "%" #formatting

#Final results
print("\nAverage Month-to-Month Changes (as percentages):")
print(average_changes)

#Question 2: Which province experienced the highest average change in the above categories?
print("\nQuestion 2: Provinces that experienced the highest average change in the above categories")
    #Find the province with the highest average change in each category
highest_changes = average_changes.idxmax()

#Results
print("\nProvinces with the Highest Average Change in the above categories:")
print(f"Highest Food Change: {highest_changes['Food']}")
print(f"Highest Shelter Change: {highest_changes['Shelter']}")
print(f"Highest All-items Excluding Food and Energy Change: {highest_changes['All-items excluding food and energy']}\n")

#Question 3: Compute the annual change in CPI for services across Canada and all provinces. Report your numbers as a percent up to one decimal place.
print("\nQuestion 3: Annual change in CPI for services across Canada and all provinces.")
#Filter data
services_df = final_dataset[final_dataset['Item'] == 'Services'].copy()
services_df['Month'] = pd.to_datetime(services_df['Month'], errors='coerce') #datetime format

#Extract the year from the 'Month' column
services_df['Year'] = services_df['Month'].dt.year

#Group by 'Jurisdiction' and 'Year', then get the first and last CPI values per year
annual_change_services = services_df.groupby(['Jurisdiction', 'Year'])['CPI'].agg(['first', 'last'])

#Compute the annual CPI change
annual_change_services['Annual_CPI_Change'] = ((annual_change_services['last'] - annual_change_services['first']) / annual_change_services['first']) * 100
#Round 
annual_change_services['Annual_CPI_Change'] = annual_change_services['Annual_CPI_Change'].round(1)

#Result
print("\n3. Annual change in CPI for services across Canada and all provinces:")
print(annual_change_services['Annual_CPI_Change'])


#Question 4: Which region experienced the highest inflation in services?
print("\nQuestion 4: Region that experienced the highest inflation in services?")
highest_inflation_region = annual_change_services['Annual_CPI_Change'].idxmax()

#result
print("\n4. Region with the highest inflation in services:")
print(annual_change_services.loc[highest_inflation_region]) 
print(f"Region: {highest_inflation_region[0]}, Year: {highest_inflation_region[1]}, Annual CPI Change: {annual_change_services.loc[highest_inflation_region, 'Annual_CPI_Change']}")

