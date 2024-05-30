

import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

# Configuration
zoom_email = 'jay@pixeltests.com'
zoom_password = 'sgmoid234A!'
report_url = 'https://zoom.us/account/my/report/webinar'
download_directory = '/path/to/your/download/directory'

# Initialize the Chrome driver
options = webdriver.ChromeOptions()
prefs = {'download.default_directory': download_directory}
options.add_experimental_option('prefs', prefs)

driver = webdriver.Chrome(options=options)

try:
    # Navigate to the Zoom login page
    driver.get('https://zoom.us/signin')

    # Find and fill the email field
    email_field = driver.find_element(By.ID, 'email')
    email_field.send_keys(zoom_email)

    # Find and fill the password field
    password_field = driver.find_element(By.ID, 'password')
    password_field.send_keys(zoom_password)

    # Submit the login form
    password_field.send_keys(Keys.RETURN)
    
    # Wait for the login process to complete
    time.sleep(10)  # Adjust this time based on your internet speed

    # Navigate to the report page
    driver.get(report_url)

    # Wait for the page to load
    time.sleep(5)  # Adjust this time based on your internet speed

    # Locate and click the 'Attendee Report' button
    attendee_report_button = driver.find_element(By.XPATH, "/html/body/div[1]/div[4]/div[3]/div[3]/div/div/div[2]/div[3]/div[1]/div/label[2]/input")
    attendee_report_button.click()

    
    # Wait for the attendee report page to load
    time.sleep(5)  # Adjust this time based on your internet speed
    
    # Loacate webinar and click the radio
    webinar_report_button = driver.find_element(By.XPATH, "/html/body/div[1]/div[4]/div[3]/div[3]/div/div/div[2]/div[3]/div[2]/div[3]/table/tbody/tr/td[1]/input")
    webinar_report_button.click()

    
   

    # Wait for the attendee report page to load
    time.sleep(5)  # Adjust this time based on your internet speed

    # Locate and click the 'Export as CSV' button
    export_button = driver.find_element(By.XPATH, "/html/body/div[1]/div[4]/div[3]/div[3]/div/div/div[2]/div[3]/div[3]/form/a")
    export_button.click()

    # Wait for the download to complete
    time.sleep(10)  # Adjust this time based on your download speed

    print("Report downloaded successfully.")

finally:
    # Close the browser
    driver.quit()

