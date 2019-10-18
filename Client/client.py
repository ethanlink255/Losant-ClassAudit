from pynfc import Nfc, Desfire, Timeout
import requests
import api

n = Nfc("pn532_i2c:/dev/i2c-1")

DESFIRE_DEFAULT_KEY = b'\x00' * 8
MIFARE_BLANK_TOKEN = b'\xFF' * 1024 * 4

for target in n.poll():
    try:
        out(target.uid)
        
    except TimeoutException:
        pass


























