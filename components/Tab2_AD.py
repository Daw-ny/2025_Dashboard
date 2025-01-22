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

    # 제작 계기
    dbc.Row([
        html.H4("화학 공정 이상탐지", style = {'color':'#18bc9c'}),  # 제목
        html.Hr(),  # 대시 구분선
        html.H6("""
                화학 공정 데이터를 이용한 이상 탐지(anomaly detection)으로, 공정 데이터에서 비정상적인 동작을 탐지하는 모델을 만드는 것입니다.
                이상유무를 탐지하는 것 뿐만 아니라 이상의 원인을 찾아 공정 과정에서 발생하는 이상을 대처할 수 있는 방안을 마련하는 것을 목표로 합니다.
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
                html.Li(["Train데이터 약 25만개와 Test데이터 약 72만개로 이루어져있습니다."]),
                html.Li(["하나의 시뮬레이션 안에 500개 또는 750개의 샘플이 기록되었습니다."]),
                html.Li(["하나의 시뮬레이션 중",
                         html.Span(" 한가지의 샘플이라도 이상이 존재하면 시뮬레이션 안의 모든 샘플이 이상판정", style={"fontWeight": "bold", "color": "#f39c12"}),
                         "을 받습니다."]),
                html.Li(["Train 데이터는 ",
                         html.Span("모든 관측값이 정상으로 판정된 값", style={"fontWeight": "bold", "color": "#f39c12"}),
                         "으로 존재하였습니다."]),
                html.Li(["시뮬레이션번호, 샘플번호, 이상 유무를 제외한 ",
                         html.Span("나머지 변수에 대해 접근이 제한", style={"fontWeight": "bold", "color": "#f39c12"}),
                         "되었습니다."]),
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
                    "References: ",
                    html.A("Notion", href="https://round-radish-a83.notion.site/One-Class-122a737493fb80aba16ecda4bf19101f?pvs=4", target="_blank", style={"color": "#2c3e50", "fontWeight": "bold"}),
                ]),
    ]),

])