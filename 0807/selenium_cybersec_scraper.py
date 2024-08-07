from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time

driver = webdriver.Firefox()
url = "https://cybersec.ithome.com.tw/2024/exhibition-page/2109"
driver.get(url)

# 電話
telephone_element = driver.find_element(By.CLASS_NAME, 'info-tel')
if telephone_element: # 確定有東西
    print("Telephone: ", telephone_element.text)
else:
    print("Telephone not found.")

# EMAIL
email_element = driver.find_element(By.CLASS_NAME, 'info-mail')
if email_element: # 確定有東西
    print("Email: ", email_element.text)
else:
    print("Email not found.")

# Website
website_elements = driver.find_elements(By.CLASS_NAME, 'border-icon')
if website_elements: # 確定有找到東西
    for website_element in website_elements:
        # 利用 element.get_attribute("屬性名稱") 取得資訊
        href = website_element.get_attribute('href')
        if href:
            if "facebook" in href: # facebook這幾個字有無出現在連結
                print("Facebook: ", href) 
            elif 'twitter' in href:
                print("Twitter: ", href)
            elif 'linkedin' in href:
                print("LinkedIn: ", href)
            else:
                print('Website: ',href)
else:
    print("Website not found.")

# Description
desc_element = driver.find_element(By.CLASS_NAME, 'ex-foreword')
if desc_element: # 確定有東西
    print("Description: ", desc_element.text)
else:
    print("Description not found.")


driver.close()