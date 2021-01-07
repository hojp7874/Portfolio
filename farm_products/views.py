from django.shortcuts import render

import io
import urllib, base64
import pandas as pd
import matplotlib.pyplot as plt
from .kamis import kamis

# Create your views here.
def show_graph(request):
    uri = ""
    region = {1101:'서울', 2100:'부산', 2200:'대구', 2300:'인천', 2401:'광주', 2501:'대전', 2601:'울산', 3111:'수원', 3211:'춘천', 3311:'청주', 3511:'전주', 3711:'포항', 3911:'제주', 3113:'의정부', 3613:'순천', 3714:'안동', 3814:'창원', 3145:'용인'}
    if request.method == 'POST':
        print(request.POST)

        kwargs = {'action':'monthlySalesList', 'p_returntype':'json'}
        kwargs['p_itemcode'] = request.POST['item']
        kwargs['p_yyyy'] = '2020'
        kwargs['p_period'] = '3'
        try:
            kwargs['p_kindcode'] = request.POST['variety']
        except: pass
        try:
            kwargs['p_graderank'] = request.POST['p_graderank']
        except: pass
        if request.POST['region'] != 'on':
            kwargs['p_countycode'] = request.POST['region']
        # data 불러오기
        response = kamis(**kwargs)
        plt.figure()
        data = {}
        print(response['price'][0]['item'][0].values())
        for item in response['price'][0]['item']:
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
    code = pd.read_excel('./code.xls', sheet_name='코드통합(부류＋품목＋품종코드)')
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
        'regions': region,
        'code_set':code_set,
    }
    return render(request, 'farm_products/index.html', context)