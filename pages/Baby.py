#######################################################
# packages
import dash_bootstrap_components as dbc
from dash import html, dcc, callback, Output, Input, State
import pandas as pd
import os

#######################################################
# file imports
from style.mainStyle import INPUT_CARDS, CONTAINER_FIX
from components.Baby_Function import sample_file_upload
from layout import Baby_NoInput, Baby_search
# from style.pagestyle import CONTAINER_FIX

#######################################################
# load data
dir = os.getcwd()

#######################################################
# 화면 구성 레이아웃
layout = dbc.Container([

    # 대시보드 제목
    html.Br(), # 띄어쓰기
    dbc.Row([
        html.H3(children='난임 환자 대상 임신 성공 여부 예측', style={"textAlign": "center"})
    ]),

    dbc.Row([
        html.Hr() # 구분선
    ]),

    # 데이터를 저장할 Store
    dcc.Store(id='baby_stored_data'),
    dcc.Store(id="index_store", data=0),  # 현재 인덱스를 저장할 dcc.Store
    dcc.Store(id='preprocessed_store_data'),

    dbc.Row([

        # 데이터를 입력 받기
        dbc.Col([
            dbc.Row([
                dbc.Card(
                    dbc.CardBody([
                        dcc.Upload(
                            id='upload_data',
                            children=html.Div([
                                'Drag and Drop 또는 ',
                                html.A('파일 선택', style={'color': '#E95420'}),
                            ], style={'textAlign': 'center'}),
                            style={
                                **INPUT_CARDS, 
                                'display': 'flex',  # flexbox 사용
                                'justifyContent': 'center',  # 가로 중앙 정렬
                                'alignItems': 'center',  # 세로 중앙 정렬
                            },
                            multiple=False
                        ),
                    ]), style={'boxShadow': '0 4px 8px rgba(0, 0, 0, 0.1)', 'borderRadius': '10px', 'width': '480px'}
                ),
            ]),

            dbc.Row([
                html.Div(id = "baby_upload_feedback"),
            ]),

            dbc.Row([
                html.Br(),
            ]),
            
            dbc.Row([
                html.Div(id="analysis_layout"),
            ]),

        ], width = 2),
        
        # 여기서부터 데이터가 있으면 띄워줘야 되는 구간 - 없으면 데이터 입력해달라는 문구가 들어가야됨!
        dbc.Col([
            
            html.Div(id="profile_layout"),
            html.Div(id="output_container"),

        ], width = 10)

    ])
    
], style=CONTAINER_FIX)

#######################################################
# 데이터 업로드
@callback(
    [Output("baby_upload_feedback", "children"),
     Output("baby_upload_feedback", "style"),
     Output("baby_stored_data", "data"),
     Output("preprocessed_store_data", "data")],
    [Input("upload_data", "contents")],
    [State("upload_data", "filename")]
)
def upload_csvfile(contents, filename):

    return sample_file_upload(contents, filename)

# 페이지 출력
@callback(
    [
        Output("profile_layout", "children"),
        Output("analysis_layout", "children"),
    ],
    [Input("baby_stored_data", "data")]
)

def present_profile_and_analysis(data):
    
    if data:

        return Baby_search.analysis, Baby_search.profile
    
    else:

        return Baby_NoInput.analysis, Baby_NoInput.profile # 데이터가 바깥쪽에 있는 것이 먼저 output으로 나감

###########################################################
# Primary: #E95420 (Orange-Red)
# Secondary: #F7F9FA (Light Gray)
# Success: #18BC9C (Teal Green)
# Info: #3498DB (Bright Blue)
# Warning: #F39C12 (Orange)
# Danger: #E74C3C (Red)
# Light: #F5F5F5 (Soft White)
# Dark: #2C3E50 (Deep Blue Gray)