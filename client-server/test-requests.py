import threading
import requests

SERVER_URL = 'http://172.26.100.134:8000/groups'
NUM_REQUESTS = 10  

def make_request(i):
    response = requests.get(SERVER_URL)
    if not response.ok:
        print("Requisição ",i,response.text)

threads = []
for i in range(NUM_REQUESTS):
    t = threading.Thread(target=make_request, args=(i,))
    t.start()
    threads.append(t)

for t in threads:
    t.join()