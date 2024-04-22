import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

driver = webdriver.Chrome()
driver.get("http://localhost:9090")
driver.find_element(By.XPATH, "/html/body/form[2]/input").click()
driver.find_element(By.NAME, "username").click()
driver.find_element(By.NAME, "username").send_keys("username5")
time.sleep(1)
driver.find_element(By.NAME, "password").click()
driver.find_element(By.NAME, "password").send_keys("password5")
time.sleep(1)
driver.find_element(By.NAME, "passkey").click()
driver.find_element(By.NAME, "passkey").send_keys("testingkey5")
driver.find_element(By.XPATH, "/html/body/form/input[4]").click()
time.sleep(3)
driver.find_element(By.NAME, "username").click()
driver.find_element(By.NAME, "username").send_keys("username5")
time.sleep(1)
driver.find_element(By.NAME, "password").click()
driver.find_element(By.NAME, "password").send_keys("password5")
time.sleep(1)
driver.find_element(By.XPATH, "/html/body/form[1]/input[3]").click()
time.sleep(3)
driver.find_element(By.XPATH, "/html/body/ul/li[1]/a").click()
driver.find_element(By.XPATH, "/html/body/div/form/input[1]").click()
driver.find_element(By.XPATH, "/html/body/div/form/input[1]").send_keys("newpassword5")
driver.find_element(By.XPATH, "/html/body/div/form/input[2]").click()
time.sleep(3)
driver.find_element(By.XPATH, "/html/body/ul/li[2]/a").click()
driver.find_element(By.XPATH, "/html/body/div[1]/form/input[1]").click()
encryption_word = "words"
driver.find_element(By.XPATH, "/html/body/div[1]/form/input[1]").send_keys(encryption_word)
driver.find_element(By.XPATH, "/html/body/div[1]/form/input[2]").click()
time.sleep(3)
encryption = driver.find_element(By.XPATH, "/html/body/div[1]/form/input[3]").get_attribute("value")
driver.find_element(By.XPATH, "/html/body/ul/li[3]/a").click()
driver.find_element(By.XPATH, "/html/body/div/form/input[1]").click()
driver.find_element(By.XPATH, "/html/body/div/form/input[1]").send_keys(encryption)
driver.find_element(By.XPATH, "/html/body/div/form/input[2]").click()
encryption_output = driver.find_element(By.XPATH, "/html/body/div[1]/form/input[3]").get_attribute("value")
if (encryption_output != encryption_word):
    # Throw error
    print("Decryption failed")
time.sleep(3)



# Register

# New Password

# Log out

# Log In

# Get Encryption

# Decryption

