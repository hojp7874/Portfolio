from urllib.request import urlopen, Request
import json


def kamis(**kwargs):
    url = 'http://www.kamis.or.kr/service/price/xml.do'

    with open('./Portfolio/secret.json') as jsonfile:
        data = json.load(jsonfile)
        CERT_KEY = data["p_cert_key"]
        CERT_ID = data["p_cert_id"]

    queryParams = f'?p_cert_key={CERT_KEY}&p_cert_id={CERT_ID}'

    for key, value in kwargs.items():
        queryParams += f'&{key}={value}'
    request = Request(url + queryParams)
    request.get_method = lambda:'GET'
    response_body = urlopen(request).read().decode('utf8')
    
    return json.loads(response_body)