#######################################################
# packages
import dash_bootstrap_components as dbc
from dash import html

#######################################################
# file imports
from style.mainStyle import NOINPUT_MESSAGE, INPUT_PROFILE

#######################################################
analysis = dbc.Card(
    dbc.CardBody(
        html.Div(
            [
                html.P("파일을 업로드 해주세요."),
                html.P("분석 결과가 여기에 표시됩니다.")
            ],
            style={
                "textAlign": "center",  # 텍스트 중앙 정렬
                "fontSize": "36px",  # 글자 크기
                "color": "#2C3E50",  # 글자 색상 (회색 계열)
            }
        ),
        className="d-flex align-items-center justify-content-center",
        style={"height": "200px"}  # 카드 높이 지정 (원하는 크기로 조절 가능)
    ),
    style=NOINPUT_MESSAGE
)

profile = dbc.Card(
        dbc.CardBody(
            html.Div(
                [
                    html.P("파일을 업로드 해주세요."),
                    html.P("프로필이 여기에 표시됩니다.")
                ],
                style={
                    "textAlign": "center",  # 텍스트 중앙 정렬
                    "fontSize": "18px",  # 글자 크기
                    "color": "#2C3E50",  # 글자 색상 (회색 계열)
                }
            ),
            className="d-flex align-items-center justify-content-center",
            style={"height": "200px"}  # 카드 높이 지정 (원하는 크기로 조절 가능)
        ),
    style=INPUT_PROFILE
)