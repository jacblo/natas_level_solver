import os
import re
import readline                     # for arrow keys and history

while True:
    query = input("Enter query: ").replace("/etc/natas_webpass/natas17", "testing_webpass_file")
    if re.search(r'[;|&`\'"]', query):
        print("Invalid query")
        continue
    os.system(f'grep -i "{query}" dictionary.txt')