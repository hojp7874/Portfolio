from urllib.request import urlopen, Request
import json
import requests
from bs4 import BeautifulSoup


def kamis(**kwargs):
    url = 'http://www.kamis.or.kr/service/price/xml.do'

    with open('./Portfolio/secret.json') as jsonfile:
        data = json.load(jsonfile)
        CERT_KEY = data["p_cert_key"]
        CERT_ID = data["p_cert_id"]

    queryParams = f'?p_cert_key={CERT_KEY}&p_cert_id={CERT_ID}'

    for key, value in kwargs.items():
        queryParams += f'&{key}={value}'
    headers = {'User-Agent':'Mozilla/5.0'}
    # response = Request(url+queryParams, headers=headers)
    # response.get_method = lambda:'GET'
    response = requests.get(url+queryParams).json()
    # soup = BeautifulSoup(response.text)
    # response_body = urlopen(response).read().decode('utf8')
    
    # return json.loads(response_body)
    return response