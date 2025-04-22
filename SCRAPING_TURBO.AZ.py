# from selenium.webdriver.chrome.service import Service
# from selenium import webdriver
# from csv import writer
# from selenium.webdriver.common.by import By
# from selenium.common.exceptions import NoSuchElementException

# service = Service(r"C:\Users\USER\Desktop\chromedriver.exe")

# driver = webdriver.Chrome(service=service)

# driver.get('https://turbo.az/autos')

# # Initialize a counter for the number of pages
# page_counter = 0
# max_pages = 550  # Set the maximum number of pages

# with open('car_info.csv', 'w', newline='', encoding='utf-8') as car_infos:
#     csv_writer = writer(car_infos)
#     csv_writer.writerow(['Price', 'Model', 'Year, Engine, Distance', 'Location, Date'])

#     while page_counter < max_pages:
#         cars = driver.find_elements(By.CLASS_NAME, "products-i__bottom")
#         for car in cars:
#             details = car.text.split("\n")  # Split the car details into lines
#             if len(details) == 4: 
#                 csv_writer.writerow(details) 
        
#         try:
#             next_button = driver.find_element(By.LINK_TEXT, 'Növbəti')
#             next_button.click()  # Go to the next page
#             page_counter += 1  # Increment the page counter

#         except NoSuchElementException:
#             print("No more pages available.")
#             driver.quit()
#             break

# driver.quit()


from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from csv import writer
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
import time

service = Service(r"C:\Users\USER\Desktop\chromedriver.exe")
driver = webdriver.Chrome(service=service)

driver.get('https://turbo.az/autos')

# Initialize a counter for the number of pages
page_counter = 0
max_pages = 550  # Set the maximum number of pages

with open('car_info.csv', 'w', newline='', encoding='utf-8') as car_infos:
    csv_writer = writer(car_infos)
    csv_writer.writerow(['Price', 'Model', 'Year, Engine, Distance', 'Location, Date'])

    while page_counter < max_pages:
        try:
            cars = driver.find_elements(By.CLASS_NAME, "products-i__bottom")
            if not cars:
                print("No cars found on this page, retrying.")
                continue  # Skip to the next iteration of the while loop

            for car in cars:
                details = car.text.split("\n")  # Split the car details into lines
                if len(details) == 4:
                    csv_writer.writerow(details)  # Write the details to CSV

            # Wait a bit before clicking to avoid rapid requests
            time.sleep(2)

            try:
                next_button = driver.find_element(By.LINK_TEXT, 'Növbəti')
                next_button.click()  # Go to the next page
                page_counter += 1  # Increment the page counter
                time.sleep(3)  # Wait a few seconds to allow the next page to load

            except ElementClickInterceptedException:
                print("Ad or overlay blocking the 'Next' button. Refreshing the page.")
                driver.refresh()  # Refresh the page and retry
                time.sleep(3)  # Wait before retrying

        except NoSuchElementException:
            print("No more pages available.")
            driver.quit()
            break

driver.quit()
