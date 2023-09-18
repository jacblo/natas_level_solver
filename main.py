from selenium import webdriver
import os
import sys
import time
import common

def main():
    solved_levels = os.listdir("levels")
    up_to = int(input("Up to what level do you want?: "))
    use_cached = "y" in input("Use cached passwords? (y/n): ").lower()
    
    start_level = 0
    last_pass = None
    driver = webdriver.Firefox()
    if use_cached:
        with open("passwords.txt", "r") as f:
            lines = f.readlines()
            last_pass = lines[-1][:-1]
            start_level = len(lines)

        driver.get(
            common.build_url(password = last_pass, level=start_level-1) # go to the last solved level and log in
        )
    
    passwords = open("passwords.txt", "a" if use_cached else "w")       # open the file to write the passwords to, append if we're not restarting from scratch
    
    sys.path.append("levels")                                           # add the levels directory to the python path so we can import
    # for each level
    for level in range(start_level, up_to+1):
        # if the level is solved
        if f"solver_{level}.py" in solved_levels:
            solver_module = __import__(f"solver_{level}")               # import the solver module
            last_pass = solver_module.solve(driver, last_pass) + "\n"              # solve the level
            passwords.write(last_pass)                                  # write the password to the file
            print(f"Level {level} solved")
        else:
            driver.quit()
            raise RuntimeError(f"Level {level} is not solved yet")      # pylance says it's unreachable but it is, so ignore the graying out
    
    passwords.close()
    input("Press enter to exit")
    driver.quit()

if __name__ == "__main__":
    main()