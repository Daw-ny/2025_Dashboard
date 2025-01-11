#######################################################
# packages
import dash_bootstrap_components as dbc
from dash import Dash, Input, Output, dcc, html

#######################################################
# file imports
from style.mainstyle import CONTENT_STYLE
from layout.navigation import create_sidebar
from callbacks.page_callbacks import render_page_content

#######################################################
# Dash initialization
app = Dash(external_stylesheets=[dbc.themes.FLATLY], suppress_callback_exceptions=True)

# 네비게이션바 생성
sidebar = create_sidebar()
content = html.Div(id="page-content", style=CONTENT_STYLE)

# 레이아웃 설정
app.layout = html.Div([
    dcc.Location(id="url"), # URL 상태 관리
    sidebar,
    content
])

# URL 경로에 따라 페이지 컨텐츠 변경
@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def page_content_callback(pathname):
    return render_page_content(pathname)

if __name__ == "__main__":
    app.run_server(debug=True)