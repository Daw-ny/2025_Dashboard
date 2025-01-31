#######################################################
# packages
import dash_bootstrap_components as dbc
from dash import Dash, Input, Output, dcc, html
import dash

#######################################################
# file imports
from layout.navigation import create_sidebar
from style.navistyle import HAMBURGER_STYLE
from components.mainfunction import render_page_content

#######################################################
# Dash initialization
app = Dash(
    external_stylesheets=[dbc.themes.FLATLY],
    suppress_callback_exceptions=True,
    meta_tags=[
        {"name": "viewport", "content": "width=device-width, initial-scale=1"},
    ],
    assets_folder='assets',
)

# 서버 객체 설정
server = app.server

# 네비게이션바 생성
sidebar = create_sidebar()
content = html.Div(id="page-content")

# 레이아웃 설정
app.layout = html.Div([
    dcc.Location(id="url"), # URL 상태 관리
    dbc.Button(
        children="☰",  # 햄버거 아이콘
        id="hamburger-button",
        style=HAMBURGER_STYLE,
    ),
    sidebar,
    content,
    dash.page_container,  # 페이지 콘텐츠 렌더링
])

# URL 경로에 따라 페이지 컨텐츠 변경
@app.callback(
    Output("page-content", "children"),
    Input("url", "pathname"))
def url_render(pathname):
    return render_page_content(pathname)

# 콜백: 햄버거 버튼으로 Offcanvas 토글
@app.callback(
    Output("offcanvas", "is_open"),
    Input("hamburger-button", "n_clicks"),
    prevent_initial_call=True,
)
def toggle_offcanvas(n_clicks):
    return True  # 클릭 시 열림

if __name__ == "__main__":
    app.run_server(debug=True)