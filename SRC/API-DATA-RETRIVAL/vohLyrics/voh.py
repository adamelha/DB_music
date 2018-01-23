from six.moves import urllib
import urllib2
#from urllib.request import urlopen, Request
from urllib2 import HTTPError

import json

def get_lyrics(artist, title):
    
    request = urllib2.Request("https://api.lyrics.ovh/v1/" + artist.replace(' ', '-') + "/" + title.replace(' ', '-'))

    try:
        return (json.loads(urllib2.urlopen(request).read().decode())['lyrics'])
    except (HTTPError, UnicodeEncodeError, UnicodeDecodeError) as e:
        return "sorry, lyrics for this track are not available"

