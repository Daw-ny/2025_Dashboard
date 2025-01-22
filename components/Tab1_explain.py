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
        html.H4("제작 계기 및 목적", style = {'color':'#18bc9c'}),  # 제목
        html.Hr(),  # 대시 구분선
        html.H6("""
                프로젝트 진행 과정을 이해하기 쉽게 정리한 대시보드를 온라인으로 배포하여 누구나 과정을 쉽게 받아들일 수 있도록
                제작하였습니다. 
                """, style={"fontWeight": "bold", "color": "#2c3e50"}),  # 제목
        html.Ul(
            children=[
                html.Li(["Python을 베이스로 담았으며",
                        html.Span("Docker를 활용하여 fly.io로 배포", style={"fontWeight": "bold", "color": "#f39c12"}),
                        "하였습니다."]),
                html.Li(["Python의 Dash 패키지를 사용하여",
                        html.Span("프론트엔드를 구현하고 웹 페이지를 생성", style={"fontWeight": "bold", "color": "#f39c12"}),
                        "하였습니다."]),
                html.Li(["페이지 구성 자유도가 높으며",
                        html.Span("Python 기반의 언어로 모델링과 동시에 작업", style={"fontWeight": "bold", "color": "#f39c12"}),
                        "이 가능합니다."]),
                html.Li(["디자인은 ",
                        html.Span("Dash Bootstrap Components을 주로 활용", style={"fontWeight": "bold", "color": "#f39c12"}),
                        "하였습니다."]),
            ],
            style={"fontSize": "15px",
                "listStyleType": "circle"}  # 글씨 크기 설정
        ),
    ]),

    html.Br(),
    html.Br(),

    # 보는 방법
    dbc.Row([
        html.H4("How to Use", style = {'color':'#18bc9c'}),  # 제목
        html.Hr(),  # 대시 구분선
        html.H6("""
                탭에 있는 프로젝트에 대해 간략한 설명을 읽고 대시보드를 확인하시는 것을 권장합니다. 
                """, style={"fontWeight": "bold", "color": "#2c3e50"}),  # 제목
        html.Ul(
            children=[
                html.Li(["탭에 주로 배경과 사용했던 데이터에 대해 작성하였습니다."]),
                html.Li(["일부 대회는 제한된 공개로 되어있기 때문에 원 대회 페이지를 찾기 어려울 수 있습니다."]),
                html.Li(["대시보드는 분석 내용을 최대한 압축하여 표현했습니다. 중간에 생략된 내용이 있을 수 있습니다."]),
            ],
            style={"fontSize": "15px",
                "listStyleType": "circle"}  # 글씨 크기 설정
        ),
    ]),


])