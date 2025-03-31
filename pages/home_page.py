#######################################################
# packages
import dash_bootstrap_components as dbc
from dash import html, callback, Output, Input
import os

#######################################################
# file imports
from style.pagestyle import CONTAINER_FIX
from layout import home_Tab
from components import Tab1_explain, Tab2_AD, Tab3_FOG, Tab4_Manitto, Tab5_Liver, Tab6_Baby

#######################################################
# load directory
dir = os.getcwd()

#######################################################
# 홈 화면 구성
# 화면 구성 레이아웃
layout = dbc.Container([
    # 대시보드 제목
    html.Br(), # 띄어쓰기
    dbc.Row([
        html.H1(children='Main Page', style={"textAlign": "center"})
    ]),

    dbc.Row([
        html.Hr() # 구분선
    ]),

    # 프로필 내용 띄우기
    dbc.Row([

        # 이름과 프로필사진 넣는 곳
        dbc.Col([
            dbc.Row([
                html.Img(src = '/assets/profile.jpg',
                    style={
                        "maxWidth": "400px",  # 최대 너비
                        "maxHeight": "400px",  # 최대 높이
                        "display": "block",  # block 요소로 처리
                        "margin": "0 auto"  # 수평 가운데 정렬
                    }
                ),
            ]),

            dbc.Row([
                html.H3('Writer: Da-Woon Kim',
                    style={"textAlign": "center", "fontfamily": "NanumSquare"}
                ),
            ]),

        ],
        width = 4,
        style = {
            "paddingTop": "30px",  # 상단 내부 여백 10px
            "paddingBottom": "30px",  # 하단 내부 여백 10px
        
        }),

        # 간략한 나의 자기소개 및 관심사 넣는 곳(나의 페이지 링크 모두 포함 (contacts))
        dbc.Col([
            
            dbc.Row([
                html.H3("My Features", style = {'color':'#18bc9c'}),  # 제목
                html.Hr(),  # 대시 구분선
                html.H6("""
                        데이터 속 숨어있는 관계를 발굴하는 것을 좋아하고 누구나 쉽게 이해할 수 있도록 의사결정을 도울 수 있는
                        Data Scientist를 목표로 하고 있습니다.
                        """, style={"fontWeight": "bold", "color": "#2c3e50"}),  # 제목
                html.Ul(
                    children=[
                        html.Li(["목표를 도달하기 위해 쉽게 ",
                                html.Span("포기하지 않는 끈기", style={"fontWeight": "bold", "color": "#f39c12"}),
                                "가 있습니다."]),
                        html.Li(["분석을 해야하는 ",
                                html.Span("목적을 이해하고 진행", style={"fontWeight": "bold", "color": "#f39c12"}),
                                "하려 노력합니다."]),
                        html.Li(["데이터가 ",
                                html.Span("수집되는 과정을 이해", style={"fontWeight": "bold", "color": "#f39c12"}),
                                "하여 새로운 연관 변수를 얻는 것을 좋아합니다."]),
                        html.Li(["새로운 내용을 학습하면 ",
                                html.Span("적용", style={"fontWeight": "bold", "color": "#f39c12"}),
                                "해보려 노력합니다."]),
                        html.Li(["현재 ",
                                html.Span("Transformer을 활용한 문서 요약", style={"fontWeight": "bold", "color": "#f39c12"}),
                                "과 ",
                                html.Span("이해하기 쉬운 대시보드 구현", style={"fontWeight": "bold", "color": "#f39c12"}),
                                "에 주요 관심을 두고 있습니다."
                                ]),
                    ],
                    style={"fontSize": "15px",
                        "listStyleType": "circle"}  # 글씨 크기 설정
                ),
            ]),
            html.Br(),
            html.Br(),
            dbc.Row([
                html.H4("Contact", style = {'color':'#18bc9c'}),
                html.P([
                    html.A("Github", href="https://github.com/Daw-ny", target="_blank", style={"color": "#2c3e50", "fontWeight": "bold"}),
                    ", ",
                    html.A("Blog", href="https://velog.io/@wise_head/posts", target="_blank", style={"color": "#2c3e50", "fontWeight": "bold"}),
                    ", ",
                    html.A("Linkedin", href="http://www.linkedin.com/in/daw-ny", target="_blank", style={"color": "#2c3e50", "fontWeight": "bold"}),
                    ", ",
                    html.A("Notion Résumé", href="https://round-radish-a83.notion.site/Da-Woon-Kim-s-R-sum-248f6bff3ed04721821586ddf6dfab64?pvs=4", target="_blank", style={"color": "#2c3e50", "fontWeight": "bold"}),
                ]),
            ]),
        ], width = 8, style = {
            "paddingTop": "40px",  # 상단 내부 여백 10px
        }),

    ]),

    # 탭
    dbc.Row([
        
        home_Tab.card

    ]),


], style=CONTAINER_FIX
)

@callback(
    Output("card-content", "children"),
    [Input("card-tabs", "active_tab")]
)
def tab_content(active_tab):
    if active_tab == "tab-1":
        return Tab1_explain.contents
    
    elif active_tab == "tab-2":
        return Tab2_AD.contents
    
    elif active_tab == "tab-3":
        return Tab3_FOG.contents
    
    elif active_tab == "tab-4":
        return Tab4_Manitto.contents
    
    elif active_tab == "tab-5":
        return Tab5_Liver.contents
    
    elif active_tab == "tab-6":
        return Tab6_Baby.contents