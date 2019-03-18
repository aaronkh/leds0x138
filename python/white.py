import requests
import time
import colorsys
import random
url = 'http://192.168.1.230:3000'
requests.post(url + '/rgb', json={'red': 255, 'green': 255, 'blue': 255})
    

