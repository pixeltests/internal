#1. Stable code
#2. Is this better than the API version
#3. Run this on Cloud as a Cron Job
#4. Make sure the file that is download can be piped into the attendee_report_gsheet.py

import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


#This will do

# Configuration
zoom_email = 'email'
zoom_password = 'password'
report_url = 'https://zoom.us/account/my/report/webinar'
download_directory = '/Users/jayanthrasamsetti/Desktop'

# Initialize the Chrome driver
options = webdriver.ChromeOptions()
prefs = {'download.default_directory': download_directory}
options.add_experimental_option('prefs', prefs)

driver = webdriver.Chrome(options=options)

try:
	# Navigate to the Zoom login page
	driver.get('https://zoom.us/signin')

	# Find and fill the email field
	email_field = WebDriverWait(driver, 10).until(	EC.presence_of_element_located((By.ID, 'email')))
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

	attendee_report_radio = driver.find_element(By.XPATH, "//input[@type='radio' and @name='option_audio' and @value='Attendee']")
	attendee_report_radio.click()
	# Wait for the next step to be available

	time.sleep(5)

	radio_buttons = driver.find_elements(By.XPATH, "//input[@type='radio' and @name='select_webinar']")
	radio_buttons[0].click()

	time.sleep(10)

	checkbox = driver.find_element(By.ID, 'withSortCheckbox')
	if not checkbox.is_selected():
		checkbox.click()
		print("Checkbox 'Sort the attendee list by attended status' is now checked.")
	else:
		print("Checkbox 'Sort the attendee list by attended status' was already checked.")

	time.sleep(9)  # Adjust this time based on your internet speed

	generate_report_button = driver.find_element(By.ID, 'GenerateReport')
	generate_report_button.click()
	print("Clicked 'Generate CSV Report' button.")

	time.sleep(8)

finally:
	print ("Done")
    # Close the browser
    # driver.quit()
