import os
import re
import readline                     # for arrow keys and history

while True:
    query = input("Enter query: ").replace("/etc/natas_webpass/natas17", "testing_webpass_file").replace("index.php", "simulators/16-source.php")
    if re.search(r'[;|&`\'"]', query) or query == "":
        print("Invalid query")
        continue
    
    if ":" == query[0]:
        query = query[1:]
        command = query
    else:
        command = f'grep -i "{query}" dictionary.txt'
    print("Executing command: ", command)
    os.system(command)