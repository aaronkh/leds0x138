import requests
import time
import colorsys
import random
url = 'http://192.168.1.230:3000'
def smooth_rainbow(num):
    time.sleep(.01)
    return (num + 1) % 360

def random_color(num):
    time.sleep(.25)
    return random.randrange(0, 360)

def bold_rainbow(num):
    time.sleep(.6)
    return (num + 60) % 360

color = 0
while True:
    color = smooth_rainbow(color)
    brightness = 1
    r, g, b = colorsys.hls_to_rgb(color / 360, .5, 1)
    red, green, blue = (r * 254 * brightness) // 1 + 1, (g * 254 * brightness) // 1 + 1, (b * 254 * brightness) // 1 + 1
    requests.post(url + '/rgb', json={'red': red, 'green': green, 'blue': blue})
    

