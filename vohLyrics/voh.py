from urllib.request import urlopen, Request
from urllib.error import HTTPError
import json

def get_lyrics(artist, title):
    
    request = Request("https://api.lyrics.ovh/v1/" + artist.replace(' ', '-') + "/" + title.replace(' ', '-'))

    try:
        return (json.loads(urlopen(request).read().decode())['lyrics'])
    except (HTTPError, UnicodeEncodeError):
        return "sorry, lyrics for this track are not available"
