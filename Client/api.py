import requests

def out(uuid):
    out_request = requests.get("http://71.79.22.168:5127/api?",
        params={"func" : "out", "uuid" : uuid}
    )
    print(out_request.url)
    print(out_request.text)