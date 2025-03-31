#######################################################
# packages
import dash_bootstrap_components as dbc
from dash import html, dcc, callback, Output, Input, State
import dash
import pandas as pd

#######################################################
# file imports
from style.mainStyle import INPUT_PROFILE_NOCENTER
from components import Baby_Function
from layout import Baby_DI, Baby_IVF

#######################################################
# 데이터를 받았을 때 맨 위에 배치할 이전, 다음 버튼과 현재 번호
analysis = dbc.Row([

    dbc.Col([
        dbc.Button("이전", id="prev_btn", color="primary", style={"width": "80px", "padding": "5px 10px"}),
        html.Span(id="index_display", style={"padding": "5px", "font-weight": "bold"}),
        dbc.Button("다음", id="next_btn", color="primary", style={"width": "80px", "padding": "5px 10px"})
    ], width="auto"),

    # 🔹 검색창 추가 (이전/다음 버튼 옆에 배치)
    dbc.Col([
        dcc.Input(id="search_input", type="text", placeholder="환자 번호 입력 (예: 000123)",
                  style={"width": "220px", "margin-left": "10px"}),  # 🔹 입력창 크기 조정
    ], width="auto"),

    dbc.Col([
        dbc.Button("검색", id="search_btn", color="primary", style={"width": "80px", "padding": "5px 10px"}),
    ], width="auto"),

    dbc.Row([
        # 데이터 표시 영역
        html.Div(id="output_container", className="mt-3"),
    ]),
])


profile = dbc.Row([
    dbc.Card([
        dbc.CardHeader(id = "patient_number"),
        dbc.CardBody(
            html.Div(id = "patient_info"),
            className="d-flex align-items-start justify-content-start",
            style={"height": "200px"}  # 카드 높이 지정 (원하는 크기로 조절 가능)
        )],
    style=INPUT_PROFILE_NOCENTER
    )
])
#######################################################
layout = dbc.Container([

    # analysis(이전/다음/검색)
    analysis,

    # profile(환자 프로필 카드)
    profile,

    # 🔥 output_container: 콜백에서 활용할 DIV
    html.Div(id="output_container", className="mt-3"),
    
], fluid=True)
#######################################################
# 콜백
@callback(
    Output("index_store", "data"),  # 인덱스 상태 업데이트
    [Input("prev_btn", "n_clicks"), 
     Input("next_btn", "n_clicks"), 
     Input("search_btn", "n_clicks")],
    [State("index_store", "data"),
     State("baby_stored_data", "data"),
     State("search_input", "value")],
     prevent_initial_call=True
)
def update_index(prev_clicks, next_clicks, search_clicks, index, data, search_value):
    ctx = dash.callback_context

    if not data or not ctx.triggered:
        print("nodata or triggered")
        return dash.no_update

    button_id = ctx.triggered[0]["prop_id"].split(".")[0]

    max_index = len(data) - 1
    
    # v01
    if index is None:
        index = 0

    # Previous Button
    if button_id == "prev_btn":
        if index > 0:
            return index - 1
        
    # Next Button
    elif button_id == "next_btn":
        if index < max_index:
            return index + 1
        
    # Search Button
    if button_id == "search_btn" and search_value:
        # 검색어에서 숫자만 추출 (ex. "TRAIN_000013" -> "000013")
        search_value_digits = "".join(filter(str.isdigit, search_value))
        
        for idx, row in enumerate(data):
            # 실제 데이터의 ID에서도 숫자만 추출
            patient_digits = "".join(filter(str.isdigit, row["ID"]))
            
            if patient_digits == search_value_digits:
                return idx
   
        return dash.no_update  # 검색 실패 시 변경 없음

    return 0

# 콜백: 인덱스가 변경되면 데이터 표시 및 버튼 상태 업데이트
@callback(
    [
        Output("output_container", "children"),
        Output("index_display", "children"),
        Output("prev_btn", "style"),
        Output("next_btn", "style")
    ],
    [Input("index_store", "data"), State("baby_stored_data", "data")],
    prevent_initial_call=True
)
def display_data(index, data):
    if not data:  # 데이터가 없을 때
        return "데이터가 없습니다.", "0 / 0", {"display": "none"}, {"display": "none"}

    if index is None or index >= len(data):
        return "유효하지 않은 인덱스입니다.", "N/A", {"display": "none"}, {"display": "none"}

    row = data[index]  # 현재 인덱스의 데이터

    if row['시술 유형'] == "IVF":
        layout = Baby_IVF.layout
        index_text = f"[{row['시술 유형']}] {index + 1} / {len(data)}"  # 인덱스 표시 (1부터 시작)

    elif row['시술 유형'] == "DI":
        layout = Baby_DI.layout
        index_text = f"[{row['시술 유형']}] {index + 1} / {len(data)}"  # 인덱스 표시 (1부터 시작)

    else:
        layout = []
        index_text = f"[존재하지 않은 시술 유형] {index + 1} / {len(data)}"  # 인덱스 표시 (1부터 시작)
    

    # 버튼의 스타일을 조건에 따라 변경
    prev_btn_style = {"display": "none"} if index == 0 else {"width": "80px"}
    next_btn_style = {"display": "none"} if index == len(data) - 1 else {"width": "80px"}

    return layout, index_text, prev_btn_style, next_btn_style

# 콜백: 인덱스 변경되면 프로필 표시 또한 같이 변경해줘야 함
@callback(
    [
        Output("patient_number", "children"),
        Output("patient_info", "children"),
    ],
    [
        Input("index_store", "data"),
        Input("baby_stored_data", "data")
    ]
)
def display_patient_profiles(index, data):

    if not data:
        return "데이터가 없습니다.", "N/A"
    
    
    if index is None or index >= len(data):
        return "인덱스 오류", "N/A"

    pt = data[index]

    title = html.Div([f"환자 번호: {pt['ID']}"],
                style={
                    "textAlign": "center",  # 텍스트 중앙 정렬
                    "fontSize": "24px",  # 글자 크기
                    "color": "#2C3E50",  # 글자 색상 (회색 계열)
                })

    info = html.Div(
        children=[
            html.Li([
                        html.Span("기본 정보", style={"fontWeight": "bold", "color": "#3498DB"}),
                    ]),
            html.A(f"나이: {pt['시술 당시 나이']}"),
            html.Li([
                        html.Span("과거 병력", style={"fontWeight": "bold", "color": "#3498DB"}),
                    ]),
            html.A(
                Baby_Function.patient_illness(pt)
            ),
        ],
        style={"fontSize": "20px",
            "listStyleType": "circle"}  # 글씨 크기 설정
    )    

    return title, info