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
        html.H4("마니또 자동 추출", style = {'color':'#18bc9c'}),  # 제목
        html.Hr(),  # 대시 구분선
        html.H6("""
                마니또 게임을 진행하다 보면 모든 경우를 알고 있는 사회자가 동반되거나 자신을 뽑지 않을 때 까지 반복해서 선정 해야합니다.
                번거로운 과정 때문에 우정 기념 게임을 진행하다가도 포기하게 됩니다. 이를 방지하기 위해서 자동으로 분배 할 수 있는 알고리즘을 만들어
                각자의 메일로 전송할 수 있도록 적용합니다.
                """, style={"fontWeight": "bold", "color": "#2c3e50"}),  # 제목
        html.Ul(
            children=[
                html.Li(["모임 참여자 모두가 게임에 참여할 수 있도록 만들었습니다."]),
                html.Li(["제작자는 실제로 학회 발표 이후 대학원 동기와의 모임에서 직접 사용하였습니다."]),
            ],
            style={"fontSize": "15px",
                "listStyleType": "circle"}  # 글씨 크기 설정
        ),
    ]),

    dbc.Row([
        html.Br(),
    ]),

    # 보는 방법
    dbc.Row([
        html.H4("How to Use", style = {'color':'#18bc9c'}),  # 제목
        html.Hr(),  # 대시 구분선
        html.H6("""
                탭에 있는 프로젝트에 대해 간략한 설명을 읽고 대시보드를 확인하시는 것을 권장합니다. 
                """, style={"fontWeight": "bold", "color": "#2c3e50"}),  # 제목
        html.Ul(
            children=[
                html.Li(["페이지는 네이버 아이디로 발송되게 작성되었습니다."]),
                html.Li([
                            html.A("Velog", href="https://velog.io/@kkukky81/%ED%8C%8C%EC%9D%B4%EC%8D%AC%EC%97%90%EC%84%9C-%EB%84%A4%EC%9D%B4%EB%B2%84-%EB%A9%94%EC%9D%BC-%EC%A0%84%EC%86%A1", target="_blank", style={"color": "#2c3e50", "fontWeight": "bold"}),
                            "에서 1번 내용을 참조하셔서 사용할 때 한정 세팅을 권장드립니다."
                    ]),
                html.Li(["필수 항목을 입력하고 전송 버튼을 눌러주시기 바랍니다."]),
                html.Li([html.Span("주의사항", style={"fontWeight": "bold", "color": "#e74c3c"}),
                         ": 보낸이는 보낸 메일함을 열지 말아주시길 바랍니다. 게임의 본질을 흐릴 수 있습니다."]),
                html.Li([html.Span("주의사항", style={"fontWeight": "bold", "color": "#e74c3c"}),
                         ": 첨부파일에 본인도 포함시키셔야 본인에게도 메일이 전송됩니다."]),
                html.Li([html.Span("섬 없애기", style={"fontWeight": "bold", "color": "#f39c12"}),
                         ": 다수의 참여자 중에서 두명이서 또는 일부 인원이서 교환하는 형태의 경우의 수를 없애는 기능입니다."]),
            ],
            style={"fontSize": "15px",
                "listStyleType": "circle"}  # 글씨 크기 설정
        ),
    ]),
])