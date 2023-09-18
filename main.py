from selenium import webdriver
import os
import sys
import time
import common
import pandas as pd

PASSWORD_FILE = "passwords.csv"
def main():
    solved_levels = os.listdir("levels")
    up_to = int(input("Up to what level do you want?: "))
    use_cached = "y" in input("Use cached passwords? (y/n): ").lower()
    
    start_level = 0
    last_pass = None
    driver = webdriver.Firefox()
    if use_cached:
        data = pd.read_csv(PASSWORD_FILE)
        last_pass = data.iloc[-1]["password"]
        start_level = data.iloc[-1]["level"] + 1

        driver.get(
            common.build_url(password = last_pass, level=start_level-1) # go to the last solved level and log in
        )
    
    passwords = open(PASSWORD_FILE, "a" if use_cached else "w")         # open the file to write the passwords to, append if we're not restarting from scratch
    if not use_cached:
        passwords.write("level,password,time(seconds)\n")
    
    sys.path.append("levels")                                           # add the levels directory to the python path so we can import
    # for each level
    for level in range(start_level, up_to+1):
        # if the level is solved
        if f"solver_{level}.py" in solved_levels:
            solver_module = __import__(f"solver_{level}")               # import the solver module
            a = time.time()
            last_pass = solver_module.solve(driver, last_pass)          # solve the level
            b = time.time()
            passwords.write(f"{level},{last_pass},{b-a}\n")             # write the password to the file
            print(f"Level {level} solved in {b-a:.4} seconds")
        else:
            driver.quit()
            raise RuntimeError(f"Level {level} is not solved yet")      # pylance says it's unreachable but it is, so ignore the graying out
    
    passwords.close()
    input("Press enter to exit")
    driver.quit()

if __name__ == "__main__":
    main()