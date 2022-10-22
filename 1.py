from selenium import webdriver
import time
from selenium.webdriver.common.by import By
import pickle
val = input("Enter your username: ")
val2 = input("Enter your password: ")
driver = webdriver.Chrome()
driver.get('http://sis.eelu.edu.eg/static/index.html')
searchbox = driver.find_element(By.ID, "name")
searchbox.send_keys(val)
searchbox = driver.find_element(By.ID, "password")
searchbox.send_keys(val2)
searchButton = driver.find_element(By.ID, "usertype_1")
searchButton.click()
searchButton = driver.find_element(By.ID, "login_btn")
searchButton.click()
time.sleep(3)
searchButton = driver.find_element(By.ID, "moodleLogin")
searchButton.click()
driver.get('https://moodlelms.eelu.edu.eg/')
with open(".\cookies\cookies.pickle", "wb") as file:
    pickle.dump(driver.get_cookies(), file)

    print("finish")&driver.quit()
    