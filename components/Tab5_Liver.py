#######################################################
# packages
import dash_bootstrap_components as dbc
from dash import html
import os

#######################################################
# file imports

#######################################################
# load data
dir = os.getcwd()

#######################################################
contents = dbc.Row([

    # 대회 요약
    dbc.Row([
        html.H4("의료 데이터 파악, 분석 및 EDA", style = {'color':'#18bc9c'}),  # 제목
        html.Hr(),  # 대시 구분선
        html.H6("""
                주제로 선정한 의료 데이터를 직접 수집하거나 대회에 있는 데이터를 수집하여 데이터의 여러가지 특성을 파악하고 특성에 대해 EDA를 진행합니다.
                """, style={"fontWeight": "bold", "color": "#2c3e50"}),  # 제목
    ]),

    dbc.Row([
        html.Br(),
    ]),

    # 데이터 특징
    dbc.Row([
        html.H4("사용된 데이터의 특징", style = {'color':'#18bc9c'}),  # 제목
        html.Hr(),  # 대시 구분선
        html.Ul(
            children=[
                html.Li(["표본 환자의 인적 정보와 합병증상, 혈청학 수치와 간 수치 진행도가 존재합니다."]),
                html.Li(["상대적으로 사망율이 높은 간 질병에 대해 확인하고자 총 3가지의 데이터를 수집하였습니다."]),
                html.Li(["연속형 변수와 범주형 변수에 대해 ",
                         html.Span("간 질환 단계와의 관련성", style={"fontWeight": "bold", "color": "#f39c12"}),
                         "에 대해 분석하고 유의한 연속형 변수에 대해 사후 검정을 실시하였습니다."]),
                html.Li(["각 변수마다",
                         html.Span(" 관측값이 존재하지 않은 관측치를 제외", style={"fontWeight": "bold", "color": "#f39c12"}),
                         "하여 분석을 진행하였습니다."]),
                html.Li(["B형간염, C형간염에 대해도 분석하였으나 해당 대시보드는 Cirrhosis에 집중하였습니다."]),
            ],
            style={"fontSize": "15px",
                "listStyleType": "circle"}  # 글씨 크기 설정
        ),
    ]),

    dbc.Row([
        html.Br(),
    ]),

    # 주관 및 참조
    dbc.Row([
        html.H4("주관 및 참조", style = {'color':'#18bc9c'}),  # 제목
        html.P([    
                    "주관: Upstage, Fastcampus",
                    html.A("(link)", href="https://stages.ai/", target="_blank", style={"color": "#2c3e50", "fontWeight": "bold"}),
                    html.Br(),
                    "Data: ",
                    html.A("Kaggle", href="https://www.kaggle.com/datasets/fedesoriano/cirrhosis-prediction-dataset", target="_blank", style={"color": "#2c3e50", "fontWeight": "bold"}),
                    ', ',
                    html.A("Hepatitis B", href="https://www.kaggle.com/datasets/cdc/national-health-and-nutrition-examination-survey", target="_blank", style={"color": "#2c3e50", "fontWeight": "bold"}),
                    ', ',
                    html.A("Hepatitis C", href="https://www.kaggle.com/datasets/fedesoriano/hepatitis-c-dataset", target="_blank", style={"color": "#2c3e50", "fontWeight": "bold"}),
                    ', ',
                    html.A("population", href="https://www.cdc.gov/", target="_blank", style={"color": "#2c3e50", "fontWeight": "bold"}),
                    ', ',
                    html.A("국립암센터_암발생 통계 정보", href="https://www.data.go.kr/data/3039563/fileData.do", target="_blank", style={"color": "#2c3e50", "fontWeight": "bold"}),
                ]),
    ]),

])