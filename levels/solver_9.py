from common import *
import base64

def solve(driver, _ = None):
    driver.get(build_url(level=8, end_arguments="/index-source.html"))
    encoded_secret = driver.find_element(By.XPATH, '/html/body/code/span/span[3]').text[1:-1]
    from_hex = bytes.fromhex(encoded_secret)
    reversed_bytes = from_hex[::-1]
    decoded = base64.b64decode(reversed_bytes).decode('utf-8')
    driver.get(build_url(level=8))
    driver.find_element(By.XPATH, '/html/body/div[1]/form/input[1]').send_keys(decoded)
    driver.find_element(By.XPATH, '/html/body/div[1]/form/input[2]').click()
    
    text = driver.find_element(By.XPATH, '//*[@id="content"]').text
    password = text[text.find("is ")+3:text.find('\n')]
    
    driver.get(build_url(password = password, level=9))
    return password