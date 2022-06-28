from seleniumwire import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from configuration import environment_exection


def get_token():
    driver_path = r'./drivers/chromedriver.exe'  # 这是chrome驱动路径
    driver = webdriver.Chrome(executable_path=driver_path)
    wait = WebDriverWait(driver, 5)

    url = environment_exection.server_url + "/#/login"
    driver.get(url)
    
    elem_name = driver.find_element(By.XPATH, "//input[@placeholder='请输入账号']")
    elem_name.send_keys(environment_exection.server_username)

    elem_password = driver.find_element(By.XPATH, "//input[@placeholder='请输入密码']")
    elem_password.send_keys(environment_exection.server_password)

    elem_login = driver.find_element(By.XPATH, "//button//*[text()='登 录']")
    elem_login.click()
    try:
        wait.until(EC.presence_of_element_located((By.ID, "tags-view-container")))
    except TimeoutException:
        print("page time out")
        driver.quit()

    for request in driver.requests:
        if request.url == environment_exection.server_url + '/api/user-service/user/getUserInfo':
            token = request.headers['Authorization']
            break

    driver.quit()
    return token

token = get_token()
print(token)