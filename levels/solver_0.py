from common import *

def solve(driver, _ = None):
    password = "natas0"
    driver.get(build_url(password=password, level = 0))
    
    return password