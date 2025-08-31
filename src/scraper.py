from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd

# Columns for the final DataFrame
columns = ["Rank", "Name", "Sales", "Profit", "Assets", "Market Value", "Industry", "Country"]

# Function to map scraped company details into a structured dictionary
def get_company_details(company_details):
    contents = {}
    contents[columns[0]] = company_details[0]  # Rank
    contents[columns[1]] = company_details[1]  # Name
    contents[columns[2]] = company_details[4].replace("$", "").replace(" B", "")  # Sales
    contents[columns[3]] = company_details[5].replace("$", "").replace(" B", "")  # Profit
    contents[columns[4]] = company_details[6].replace("$", "").replace(" B", "")  # Assets
    contents[columns[5]] = company_details[7].replace("$", "").replace(" B", "")  # Market Value
    contents[columns[6]] = company_details[3]  # Industry
    contents[columns[7]] = company_details[2]  # Country
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

    # Save the DataFrame to CSV in the current working directory
    df.to_csv("Forbes_Global_2000_(2025).csv", index=False)

if __name__ == "__main__":
    main()
