import requests
import json
from time import perf_counter

if __name__ == '__main__':
    c = perf_counter()
    for i in range(8):
        response = requests.get('http://127.0.0.1:5000/expensive')
        print(json.loads(response.content.decode('utf-8'))['data'])

    print(" Got 8 responses in ", perf_counter() - c, "seconds")
