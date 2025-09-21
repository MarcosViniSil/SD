import requests
from dotenv import load_dotenv
load_dotenv()
import os

url = os.environ["URL"]

def make_request(i):
    print(i)
    response = requests.get(url)
    print('Status code:', response.status_code)
    print('Response:', response.text)
