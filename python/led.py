import requests
import time
import colorsys
import random
import json
import base64
import webbrowser

url = '' # add url to server
auth_id = '' # add personal auth 
secret = '' # add secret from spotify web api
brightness = 1
def smooth_rainbow(num):
    time.sleep(.01)
    return (num + 1) % 360

def random_color(num):
    time.sleep(.25)
    return random.randrange(0, 360)

def bold_rainbow(num):
    time.sleep(.6)
    return (num + 60) % 360



data = requests.get('https://accounts.spotify.com/authorize', params={'client_id': auth_id, 'response_type': 'code', 'redirect_uri': url + '/stats', 'scope': 'user-read-currently-playing'}) #.json()
webbrowser.open_new(data.url)
auth_code = requests.get(url + '/auth_code').text
time.sleep(1)
token_data = requests.post('https://accounts.spotify.com/api/token', data={'grant_type': 'authorization_code', 'code': auth_code, 'redirect_uri': url + '/stats'}, 
                                                                    headers={'Authorization': 'Basic ' + base64.b64encode(bytes(auth_id + ':' + secret, 'utf-8')).decode()}).json()

token = token_data['access_token']
refresh_token = token_data['refresh_token']
current_song = requests.get('https://api.spotify.com/v1/me/player/currently-playing', headers={'Authorization': 'Bearer ' + token}).json()
song_anal = requests.get('https://api.spotify.com/v1/audio-analysis/' + current_song['item']['id'], headers={'Authorization': 'Bearer ' + token}).json()
ref_start = time.time() * 1000 - current_song['progress_ms']

color = 0




beat_to_play = 0 #current_song['progress_ms'] // beat_interval

while song_anal['beats'][beat_to_play]['start'] * 1000 < current_song['progress_ms']:
	print(song_anal['beats'][beat_to_play]['start'])
	beat_to_play += 1
while True:
	now = time.time() * 1000 - ref_start
	if now > current_song['item']['duration_ms']:
		current_song = requests.get('https://api.spotify.com/v1/me/player/currently-playing', headers={'Authorization': 'Bearer ' + token}).json()
		song_anal = requests.get('https://api.spotify.com/v1/audio-analysis/' + current_song['item']['id'], headers={'Authorization': 'Bearer ' + token}).json()
		ref_start = time.time() * 1000
		color = 0
		beat_to_play = 0
	print(int(now), song_anal['beats'][beat_to_play]['start'] * 1000)
	if ((now - song_anal['beats'][beat_to_play]['start'] * 1000) < 100):
	    if song_anal['beats'][int(beat_to_play)]['confidence'] > .8:
	        color = bold_rainbow(color)
	        r, g, b = colorsys.hls_to_rgb(color / 360, .5, 1)
	        red, green, blue = (r * 254 * brightness) // 1 + 1, (g * 254 * brightness) // 1 + 1, (b * 254 * brightness) // 1 + 1
	        requests.post(url + '/rgb', json={'red': red, 'green': green, 'blue': blue})
	    beat_to_play += 1
	time.sleep(.020)
    

