from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from csv import writer
import time

service = Service(r"C:\Users\USER\Desktop\chromedriver.exe")
driver = webdriver.Chrome(service=service)

driver.get('https://turbo.az/autos')
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'a')))

with open('turboaz_autos.csv', 'w', newline='', encoding='utf-8') as car_infos:
    csv_writer = writer(car_infos)
    csv_writer.writerow(['Main_Info', 'Extra_Info', 'Description', 'Properties'])

    count = 0
    page_count = 0

    while page_count < 300:

        unique_links = set()
        links = driver.find_elements(By.XPATH, '//a[contains(@class, "products-i__link")]')

        for link in links:
            href = link.get_attribute("href")

            if href and "turbo.az/autos" in href and href not in unique_links:
                unique_links.add(href)

                # print(f"Avtomobil səhifə linki: {href}")
                driver.execute_script("window.open(arguments[0]);", href)
                driver.switch_to.window(driver.window_handles[1])

                try:
                    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.product-title')))
                    Main_Info = driver.find_element(By.CSS_SELECTOR, '.product-title').text
                except (NoSuchElementException, TimeoutException):
                    Main_Info = "Məlumat yoxdur"

                try:
                    Extra_Info = [element.text for element in driver.find_elements(By.CLASS_NAME, "product-section--wide")]
                except (NoSuchElementException, TimeoutException):
                    Extra_Info = "Məlumat yoxdur"

                try:
                    Description = driver.find_element(By.CLASS_NAME, "product-description__content").text
                except (NoSuchElementException, TimeoutException):
                    Description = "Məlumat yoxdur"

                try:
                    Properties = [p.text for p in driver.find_elements(By.CLASS_NAME, 'product-extras')]
                except (NoSuchElementException, TimeoutException):
                    Properties = "Məlumat yoxdur"

                csv_writer.writerow([Main_Info, Extra_Info, Description, Properties])
                count += 1
                print(f"{count} avtomobil məlumatı çəkildi")

                driver.close()
                driver.switch_to.window(driver.window_handles[0])
                time.sleep(2)

        page_count += 1
        print(f"{page_count}. səhifə çəkildi.")

        try:
            next_button = driver.find_element(By.LINK_TEXT, 'Növbəti')
            next_button.click()
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'a')))
        except (NoSuchElementException, TimeoutException):
            print("Daha çox səhifə yoxdur.")
            break

driver.quit()

# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.common.by import By
# from selenium.common.exceptions import NoSuchElementException, TimeoutException
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from csv import writer
# import time
# from selenium.webdriver.chrome.options import Options

# options = Options()
# options.add_argument('--headless')  
# options.add_argument('--disable-gpu')
# options.add_argument('--no-sandbox')  
# service = Service(r"C:\Users\USER\Desktop\chromedriver.exe")
# driver = webdriver.Chrome(service=service, options=options)

# driver.get('https://turbo.az/autos')
# WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'a')))

# with open('turboaz_autos.csv', 'w', newline='', encoding='utf-8') as car_infos:
#     csv_writer = writer(car_infos)
#     csv_writer.writerow(['Main_Info', 'Extra_Info', 'Description', 'Properties'])

#     count = 0
#     page_count = 0
#     visited_links = set()

#     while page_count < 300:
#         WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, '//a[contains(@class, "products-i__link")]')))
#         links = driver.find_elements(By.XPATH, '//a[contains(@class, "products-i__link")]')

#         # Kopyalanan linklərə bax və təkrarlananları aradan qaldır
#         page_links = list(set([link.get_attribute("href") for link in links if link.get_attribute("href") and "turbo.az/autos" in link.get_attribute("href")]) - visited_links)

#         for href in page_links:
#             visited_links.add(href)
#             driver.get(href)

#             try:
#                 WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.product-title')))
#                 Main_Info = driver.find_element(By.CSS_SELECTOR, '.product-title').text
#             except (NoSuchElementException, TimeoutException):
#                 Main_Info = "Məlumat yoxdur"

#             try:
#                 Extra_Info = " | ".join([element.text for element in driver.find_elements(By.CLASS_NAME, "product-section--wide")])
#             except (NoSuchElementException, TimeoutException):
#                 Extra_Info = "Məlumat yoxdur"

#             try:
#                 Description = driver.find_element(By.CLASS_NAME, "product-description__content").text
#             except (NoSuchElementException, TimeoutException):
#                 Description = "Məlumat yoxdur"

#             try:
#                 Properties = " | ".join([p.text for p in driver.find_elements(By.CLASS_NAME, 'product-extras')])
#             except (NoSuchElementException, TimeoutException):
#                 Properties = "Məlumat yoxdur"

#             csv_writer.writerow([Main_Info, Extra_Info, Description, Properties])
#             count += 1
#             print(f"{count} avtomobil məlumatı çəkildi")

#             time.sleep(0.2)  # 0.2 saniyəlik kiçik gecikmə

#         page_count += 1
#         print(f"{page_count}. səhifə çəkildi.")

#         try:
#             next_button = driver.find_element(By.LINK_TEXT, 'Növbəti')
#             next_button.click()
#             WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'a')))
#         except (NoSuchElementException, TimeoutException):
#             print("Daha çox səhifə yoxdur.")
#             break

# driver.quit()
