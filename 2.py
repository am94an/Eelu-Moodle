from selenium import webdriver
import time
from selenium.webdriver.common.by import By
import pickle
driver = webdriver.Chrome()
driver.maximize_window()
driver.get('https://moodlelms.eelu.edu.eg/')
driver.delete_cookie("MoodleSession")
with open(".\cookies\cookies.pickle", "rb") as file:
    cookies = pickle.load(file)

for cookie in cookies:
    driver.add_cookie(cookie)

driver.refresh()
