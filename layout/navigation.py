#######################################################
# packages
import dash_bootstrap_components as dbc
from dash import html

#######################################################
# file imports

#######################################################
# 사이드 바 구성하기
def create_sidebar():
    return dbc.Offcanvas(
        [
            dbc.Nav(
                [
                    html.H2("Menu", className="display-4"),
                    html.Hr(),
                    html.P(
                        "프로젝트에 대한 설명과 제작의도가 담겨있습니다.", className="explain",
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
        id="offcanvas",
        is_open=False,  # 초기 상태는 닫힘
    )