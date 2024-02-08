#!/usr/bin/env python3
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from pathlib import Path
import time

USERNAME = ""
PASSWORD = ""

url = ""
new_page_url = ""

# Use try-except block to handle any exceptions during WebDriver initialization
try:
    driver = webdriver.Chrome()
except Exception as e:
    print(f"Error initializing WebDriver: {e}")
    exit()

driver.get(url)

# Use WebDriverWait to wait for the elements to be present before interacting with them
try:
    username_element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "username"))
    )
    password_element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "password"))
    )
    login_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='submit']"))
    )

    username_element.send_keys(USERNAME)
    password_element.send_keys(PASSWORD)
    login_button.click()

    print("Logged in successfully")

    # If login was successful, navigate to the desired page
    if "https://api.gmes.icpac.net/admin/" in driver.current_url:
        driver.get(new_page_url)

        # Wait for the specific element to be present on the new page
        element = WebDriverWait(driver, 60).until(
            EC.presence_of_element_located((By.XPATH, "//a[@href='/admin/ecoclimatic/ecoclimatic/'][text()='Eco Climatic Maps']"))
        )
        print(f"Successfully navigated to: {new_page_url}")

        # Set the start date to '20200701'
        start_year = 2020
        start_month = 5

        # Iterate through the range of years
        for year in range(start_year, 2024):  # Updated end_year to 2024 for a complete iteration
            # Iterate through months (assuming two-digit representation, 01 to 12)
            for month in range(1, 13):
                # Iterate through decades (01, 11, and 21)
                for decade in range(0, 3):
                    # Calculate the decade value (01, 11, 21)
                    decade_value = decade * 10 + 1

                    # Generate the file name based on the structure
                    file_name_relative = f"ndvi_country_10d_BDI_dmp_{year:04d}{month:02d}{decade_value:02d}.png"
                    file_path_absolute = Path("/home/vincent/gmes/web_updates_pngs_2020-05-01_2023_12_21/country/BDI/ndvi/10d") / file_name_relative

                    # Locate the "is_country" checkbox directly using its ID
                    is_country_checkbox = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.ID, "id_is_country"))
                    )

                    # Check if the checkbox is not already selected
                    if not is_country_checkbox.is_selected():
                        # If not selected, click the checkbox to select it
                        is_country_checkbox.click()
                        print("Checked the 'is_country' checkbox.")
                    else:
                        print("The 'is_country' checkbox is already checked.")

                    # ... (similar code for other form elements)

                    # Locate the "Choose File" input element by its ID
                    file_input = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.ID, "id_file"))
                    )

                    # Provide the absolute file path to the file input
                    file_input.send_keys(str(file_path_absolute))

                    # Extract the file name without the extension
                    file_name_without_extension = Path(file_name_relative).stem

                    # Locate the "File name" input element by its ID
                    file_name_input = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.ID, "id_file_name"))
                    )

                    # Fill in the file name without extension into the "File name" input
                    file_name_input.send_keys(file_name_without_extension)
                    print(f"Filled in the file name '{file_name_without_extension}' into the 'File name' section.")

                    # Locate the "Save and add another" button by its attributes
                    save_and_add_another_button = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.XPATH, "//input[@type='submit' and @value='Save and add another' and @name='_addanother']"))
                    )

                    # Click on the "Save and add another" button
                    save_and_add_another_button.click()
                    print("Clicked on 'Save and add another' button.")

                    # Wait for 60 seconds on the new page
                    time.sleep(60)
                    print("Waited for 60 seconds on the new page.")

except Exception as e:
    print(f"Error during login or navigation: {e}")

# Close the browser window at the end of your script or when you're done with the new page
driver.quit()