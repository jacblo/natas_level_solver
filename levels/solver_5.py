from common import *

js = f"""
a = document.createElement("a")
a.setAttribute('href', '{build_url(level=4)}')
a.text = 'link'
document.querySelector("body").appendChild(a)
"""

def solve(driver, _ = None):
    driver.get(build_url(level=5))
    
    # dismiss the alert
    driver.switch_to.alert.dismiss()
    
    # redirect to level 4
    driver.execute_script(js)   # not just running javascript because it's another origin so browser gets mad
    driver.find_element(By.XPATH, '/html/body/a').click()
    
    # return the password
    text = driver.find_element(By.XPATH, '//*[@id="content"]').text
    password = text[text.find("is ")+3:text.find('\n')]
    
    driver.get(build_url(password = password, level=5))
    return password