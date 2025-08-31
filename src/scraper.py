from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd

# Columns for the final DataFrame
columns = ["Rank", "Name", "Sales", "Profit", "Assets", "Market Value", "Industry", "Country", "Year"]

#Convert a monetary string into a float in billions
def clean_value(val):
    val = val.replace("$", "").replace(",", "").strip()
    if val.endswith("B"):
        return float(val.replace("B", "").strip())
    elif val.endswith("M"):
        return round(float(val.replace("M", "").strip()) / 1000,2)  # convert millions → billions

# Function to map scraped company details into a structured dictionary
def get_company_details(company_details):
    contents = {}
    contents[columns[0]] = company_details[0]  
    contents[columns[1]] = company_details[1]  
    contents[columns[2]] = clean_value(company_details[4])
    contents[columns[3]] = clean_value(company_details[5])
    contents[columns[4]] = clean_value(company_details[6])
    contents[columns[5]] = clean_value(company_details[7])
    contents[columns[6]] = company_details[3] 
    contents[columns[7]] = company_details[2]  
    contents[columns[8]] = "2025"

    return contents

def main():
    company_data = []  # List to store all company dictionaries

    # Initialize Chrome WebDriver
    driver = webdriver.Chrome()

    # Open Forbes Global 2000 list page
    base_url = "https://www.forbes.com/lists/global2000/"
    driver.get(base_url)

    # Locate the main ranking table container
    ranking = driver.find_element(By.ID, 'table')
    ranking_tables = ranking.find_elements(By.CLASS_NAME, 'table')  # All tables on current page

    table_counter = 0  # Counter to track how many tables we've processed
    rank = 0           # Global rank counter

    # Loop through each table and its rows
    for table in ranking_tables:
        rows = table.find_elements(By.CLASS_NAME, 'table-row')
        for row in rows:
            rank += 1  # Increment global rank
            company_details = row.text.split('\n')

            # Replace the first element with global rank to avoid rank redundancy
            company_details[0] = str(rank)

            # Remove "PROFILE SPOTLIGHT" if present, so name is always at index 1
            if len(company_details) > 1 and company_details[1] == "PROFILE SPOTLIGHT":
                del company_details[1]

            # Add structured company data to the list
            company_data.append(get_company_details(company_details))

        table_counter += 1

        # Click "Next" button after every 2 tables to go to the next page
        if table_counter < 40 and table_counter % 2 == 0:
            buttons = driver.find_elements(By.CLASS_NAME, 'TVxEFOXb')
            nextButton = buttons[1] 
            nextButton.click()

    # Close the WebDriver
    driver.quit()

    # Convert the list of dictionaries into a DataFrame
    df = pd.DataFrame(data=company_data, columns=columns)

    # Profit Margin (%) = (Profit / Sales) * 100
    df["Profit Margin"] = (df["Profit"] / df["Sales"]) * 100
    df["Profit Margin"] = df["Profit Margin"].round(2)

    # Save the DataFrame to CSV 
    df.to_csv(r"datasets/scraped_data/Forbes_Global_2000_(2025).csv", index=False)

if __name__ == "__main__":
    main()
