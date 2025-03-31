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
        html.H4("난임 환자 대상 임신 성공 여부 예측", style = {'color':'#18bc9c'}),  # 제목
        html.Hr(),  # 대시 구분선
        html.H6("""
                난임 환자 예측 모델을 활용한 진단 차트 데이터를 활용하여 임신 성공 확률을 예측해주는 페이지 입니다.
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
                html.Li(["Train데이터 약 23만개와 Test데이터 약 9만개로 이루어져있습니다."]),
                html.Li(["시술 유형이 DI와 IVF 유형으로 분류 되어 있습니다."]),
                html.Li(["DI 유형은",
                         html.Span(" 정자를 기증 받은 경우 해당하는 유형", style={"fontWeight": "bold", "color": "#f39c12"}),
                         "입니다."]),
                html.Li(["IVF는 ",
                         html.Span("체외 수정 방법을 시행하는 유형", style={"fontWeight": "bold", "color": "#f39c12"}),
                         "입니다."]),
                html.Li(["각각 해당하는 유형에 대해 ",
                         html.Span("값이 존재하는 변수의 종류에 대해 차이가 존재", style={"fontWeight": "bold", "color": "#f39c12"}),
                         "합니다."]),
                html.Li(["해당 페이지를 활용하기 위한 ",
                         html.Span("샘플 데이터", style={"fontWeight": "bold", "color": "#f39c12"}),
                         "를 아래 링크에 담아두었습니다."]),
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
                    "주관: LG Aimers",
                    html.A("(link)", href="https://www.lgaimers.ai/", target="_blank", style={"color": "#2c3e50", "fontWeight": "bold"}),
                    html.Br(),
                    "Data: ",
                    html.A("원본 HFEA", href="https://www.hfea.gov.uk/about-us/data-research/", target="_blank", style={"color": "#2c3e50", "fontWeight": "bold"}),
                    ', ',
                    html.A("대시보드 적용 Sample 데이터", href="https://docs.google.com/uc?export=download&id=1T7wpQqYvYvnA6uAkuyDxK0W8QCp0dOXy", target="_blank", style={"color": "#2c3e50", "fontWeight": "bold"}),
                ]),
    ]),

])