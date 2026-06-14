import network
import urequests

from config import ssid, password

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
ssid = ssid
password = password
wlan.connect(ssid, password)

class HTTP:
    def __init__(self) -> None:
        self._response = None
        self._format = 'json'

    def _format_return(self):
        if self._format == 'json':
            return self._response.json()
        return self._response

    def get(self, url: str, format_response='json'):
        print(f'Get {url}')
        self._response = urequests.get(url)
        return self._format_return()
    
    def post(self):
        pass
