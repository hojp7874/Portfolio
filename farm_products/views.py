from django.shortcuts import render

import io
import urllib, base64
import pandas as pd
import matplotlib.pyplot as plt
from .kamis import kamis

# Create your views here.
def show_graph(request):

    # data 불러오기
    p_yyyy = '2020'
    p_period = '3'
    p_itemcode = '111'
    p_kindcode = '01'
    p_graderank = '2'
    p_countycode = '1101'
    response = kamis(**{'action':'monthlySalesList', 'p_returntype':'json', 'p_yyyy':p_yyyy, 'p_period':p_period, 'p_itemcode':p_itemcode, 'p_kindcode':p_kindcode, 'p_graderank':p_graderank, 'p_countycode':p_countycode})
    plt.figure()
    data = {}
    for item in response['price']['item']:
        data[item['yyyy']] = [(0 if (value == '-') else int(value.replace(',', ''))) for value in item.values()][1:-1]
    df = pd.DataFrame(data)

    all_data = pd.concat([df.loc[:, column] for column in df.columns], axis=0, ignore_index=True)
    plt.plot(all_data)
    fig = plt.gcf()
    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)
    string = base64.b64encode(buf.read())
    uri = urllib.parse.quote(string)

    # 품목코드 data 불러오기
    code = pd.read_excel('code.xls', sheet_name='코드통합(부류＋품목＋품종코드)')
    code_set = {}
    for i in range(code.shape[0]):
        if code.iloc[i, 0] not in code_set:
            code_set[code.iloc[i, 0]] = {'name':code.iloc[i, 1]}
        if code.iloc[i, 2] not in code_set[code.iloc[i, 0]]:
            code_set[code.iloc[i, 0]][code.iloc[i, 2]] = {'name':code.iloc[i, 3]}
        if code.iloc[i, 4] not in code_set[code.iloc[i, 0]][code.iloc[i, 2]]:
            code_set[code.iloc[i, 0]][code.iloc[i, 2]][code.iloc[i, 4]] = {'name':code.iloc[i, 5]}

    context = {
        'data':uri,
        'regions':['전체', '서울', '부산', '대구', '광주', '대전'],
        'code_set':code_set
    }
    return render(request, 'farm_products/index.html', context)