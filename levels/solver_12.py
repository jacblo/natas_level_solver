from common import *
import base64
import urllib

def xor_strings(a,b):
    return bytes([x^y for x,y in zip(a,b)])

def repeating_key_xor(a, key):
    return bytes([x^y for x,y in zip(a, key*(len(a)//len(key)+1))])

def solve(driver, _ = None):
    driver.get(build_url(level=11))
    
    colors = ('#000000', '#ffffff')
    cookies = []
    for color in colors:
        textbox = driver.find_element(By.XPATH, '/html/body/div[1]/form/input[1]')
        textbox.clear()
        textbox.send_keys(color)
        driver.find_element(By.XPATH, '/html/body/div[1]/form/input[2]').click()
        cookies.append(urllib.parse.unquote(driver.get_cookie('data')['value']))
    
    decoded = [base64.b64decode(urllib.parse.unquote(cookie)) for cookie in cookies]
    
    # find range in which they are different
    for first_diff in range(len(decoded[0])):
        if decoded[0][first_diff] != decoded[1][first_diff]:
            break
    
    different = [d[first_diff-1:first_diff+6] for d in decoded] # they both start with # so we need to move everything back one
    xors = [xor_strings(different[i], colors[i].encode('utf-8')) for i in range(2)]
    if xors[0] != xors[1]:
        raise RuntimeError("XORs are not equal")
    
    # find length of repeating key
    for length in range(1,len(xors[0])):
        if (xors[0][:length]*((len(xors[0])//length)+1))[:len(xors[0])] == xors[0]:
            break
    xors[0] = xors[0][:length]
    
    # try all rotations to get the original color
    for _ in range(length):
        if repeating_key_xor(decoded[0], xors[0])[first_diff-1:first_diff+6].decode('utf-8') == colors[0]:
            break
        
        xors[0] = xors[0][1:] + xors[0][:1]
    else:
        raise RuntimeError("Could not find xor key")
    
    fully_decoded = repeating_key_xor(decoded[0], xors[0]).decode('utf-8')      # fully decode the cookie
    fully_decoded = fully_decoded.replace('"no"', '"yes"')                      # change the cookie to say yes 
    
    # reencode
    encoded = base64.b64encode(repeating_key_xor(fully_decoded.encode('utf-8'), xors[0]))
    driver.execute_script(f'document.cookie = "data={urllib.parse.quote(encoded)}"')
    driver.get(build_url(level=11))
    
    text = driver.find_element(By.XPATH, '//*[@id="content"]').text
    password = text[text.find("is ")+3:text.find('\nBackground color:')]
    
    driver.get(build_url(password = password, level=12))
    return password