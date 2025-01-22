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
        html.H4("안개 상태 다중분류", style = {'color':'#18bc9c'}),  # 제목
        html.Hr(),  # 대시 구분선
        html.H6("""
                시정구간으로 나뉘어져 있는 안개를 예측할 수 있는 모델을 만들고 안개에 대한 대처를 할 수 있는 방안을 모색합니다.
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
                html.Li(["10분 간격의 3년치의 훈련 데이터와 1년치의 test 데이터로 이루어져 있습니다."]),
                html.Li(["연도, 월, 일 등 시점에 관련된 변수와 10분평균 풍속, 풍향과 1분평균 강수량 등 기상에 관한 변수를 포함합니다."]),
                html.Li(["정상적인 시각의 사람이 목표를 식별할 수 있는 최대거리인 시정거리로 ",
                         html.Span("4단계의 시정거리 구간화를 진행하여 생성된 시정 구간", style={"fontWeight": "bold", "color": "#f39c12"}),
                         "을 예측하였습니다."]),
                html.Li(["평가 지표로 기상청에서 제시한 ",
                         html.Span("안개 미 발생을 제외한 정확도를 확인하는 지표 CSI를", style={"fontWeight": "bold", "color": "#f39c12"}),
                         "활용하였습니다."]),
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
                    "주관: 기상청 날씨누리",
                    html.A("(link)", href="https://bd.kma.go.kr/contest/main.do", target="_blank", style={"color": "#2c3e50", "fontWeight": "bold"}),
                    html.Br(),
                    "References: ",
                    html.A("Notion", href="https://round-radish-a83.notion.site/Weighted-Catboost-122a737493fb8061bc55f007060c5f81?pvs=4", target="_blank", style={"color": "#2c3e50", "fontWeight": "bold"}),
                ]),
    ]),

])