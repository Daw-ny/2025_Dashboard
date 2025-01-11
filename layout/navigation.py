#######################################################
# packages
import dash_bootstrap_components as dbc
from dash import html

#######################################################
# file imports
from style.mainstyle import SIDEBAR_STYLE, WRITE_STYLE  # 스타일 파일에서 임포트

#######################################################
# 사이드 바 구성하기
def create_sidebar():
    return html.Div(
        [
            html.H2("Menu", className="display-4"),
            dbc.Nav(
                [
                    
                    html.Hr(),
                    html.P(
                        "페이지는 Python의 Dash로 구성했습니다.", className="explain",
                    ),
                    dbc.NavLink("Home", href="/", active="exact"),
                    html.Br(),
                    html.Hr(),
                    html.P(
                        "진행했던 프로젝트 목록입니다.", className="explain",
                    ),
                    dbc.NavLink("화학 공정 이상탐지", href="/Anomaly-Detection", active="exact"),
                    dbc.NavLink("안개 상태 다중분류", href="/Fog-prediction", active="exact"),
                ],
                vertical=True,
                pills=True,
            ),
        ],
        style=SIDEBAR_STYLE,
    )