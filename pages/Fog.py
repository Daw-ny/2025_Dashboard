#######################################################
# packages
import dash_bootstrap_components as dbc
from dash import html, dcc, callback, Output, Input
import pandas as pd
import os

#######################################################
# file imports
from components import FOG_graph, FOG_values, FOG_table
from style.pagestyle import CONTAINER_FIX

#######################################################
# load data
dir = os.getcwd()
fog_cnt_hour = pd.read_csv(dir + '/data/fog_cnt_hour.csv') # 시간별 안개 건수
fog_cnt_month = pd.read_csv(dir + '/data/fog_cnt_month.csv') # 월별 안개 건수
fog_size_hour = pd.read_csv(dir + '/data/fog_size_hour.csv') # 시간별 안개 지속시간
fog_size_month = pd.read_csv(dir + '/data/fog_size_month.csv') # 월별 안개 지속시간
category_new_value = pd.read_csv(dir + '/data/category_new_value.csv', index_col = 0) # 범주형 crosstab
continuous_new_value = pd.read_csv(dir + '/data/continuous_new_value.csv') # 연속형 boxplot 변수
shap_values = pd.read_csv(dir + '/data/shap_values.csv') # 연속형 boxplot 변수
high_shap = pd.read_csv(dir + '/data/high_shap.csv') # 연속형 boxplot 변수
mid_shap = pd.read_csv(dir + '/data/mid_shap.csv') # 연속형 boxplot 변수
low_shap = pd.read_csv(dir + '/data/low_shap.csv') # 연속형 boxplot 변수
no_shap = pd.read_csv(dir + '/data/no_shap.csv') # 연속형 boxplot 변수

#######################################################
# 화면 구성 레이아웃
layout = dbc.Container([

    # 대시보드 제목
    html.Br(), # 띄어쓰기
    dbc.Row([
        html.H3(children='주기변수와 Weighted Catboost 를 활용한 안개 발생 진단', style={"textAlign": "center"})
    ]),

    dbc.Row([
        html.Hr() # 구분선
    ]),

    # 구성 요소 3중으로 나눠서 펼치기
    dbc.Row([

        dbc.Col([
            dbc.Alert("조건에 따른 안개 발생 건수 분포를 확인하였습니다.", color="#95a5a6"),
        ], width=4),

        dbc.Col([
            dbc.Alert("안개 규모 분포에 대해 확인하였습니다.", color="#95a5a6"),
        ], width=4),

        dbc.Col([
            dbc.Alert("파생변수의 유효성 검증을 위한 분포 확인", color="#95a5a6"),
        ], width=4),
    ]),

    dbc.Row([
        
        # 두 그래프 사이 라디오 버튼 놓기
        dbc.Col([
            html.H6('▣ 그래프의 단위를 선택하실 수 있습니다. ▣',
                style={"textAlign": "center", "fontfamily": "NanumSquare"}
            ),   # 텍스트 가운데 정렬

            dbc.RadioItems(
                options=[
                    {"label": "Hour", "value": "hour"},
                    {"label": "Month", "value": "month"},
                ],
                value="hour",
                id="radio_time_type",
                inline=True,
            ),
        ], width = 8,
            align="center",  # 세로 정렬
            className="text-center",  # 수평 정렬
        ),

        dbc.Col([
            html.H6('▣ 생성한 변수 선택하기 ▣',
                style={"textAlign": "center", "fontfamily": "NanumSquare"}
            ),
            dcc.Dropdown(FOG_values.derive_value,
                        value = '이슬점 온도',
                        id = 'derived_val'
                    ),
        ]),

    ]),

    dbc.Row([
        
        # 안개 발생 횟수 그래프
        dbc.Col([
            dcc.Graph(figure={}, id='fog_cnt_graph'),
        ], width=4),

        # 안개 발생 지속 시간 그래프
        dbc.Col([
            dcc.Graph(figure={}, id='fog_size_graph'),
        ], width=4),

                # 파생변수 분포 그래프
        dbc.Col([
            dcc.Graph(figure={}, id='derive_value_plot'),
        ], width=4),
    ]),


    dbc.Row([

        dbc.Col([
            dbc.Alert("시계열 데이터에 강한 성능을 보이는 Catboost를 활용하였습니다.", color="#95a5a6"),

            html.H6('▣ 다음과 같은 전략을 통해 적합을 시도하였습니다. ▣',
                style={"textAlign": "center", "fontfamily": "NanumSquare"}
            ),

            # 테이블 불러오기
            FOG_table.MLtable
            
        ], width=6),

        dbc.Col([
            dbc.Alert("BEST 모델의 변수 중요도를 통해 안개 생성에 주요한 요인을 확인하였습니다.", color="#95a5a6"),

            html.H6('▣ 안개 농도 구간 선택 ▣',
                style={"textAlign": "center", "fontfamily": "NanumSquare"}
            ),

            dcc.Dropdown(FOG_values.shap_names,
                        value = '통합 확인',
                        id = 'shap_type'
                    ),

            dcc.Graph(figure={}, id='shap_plot'),

        ], width=6),

    ]),

], style=CONTAINER_FIX)

#######################################################
# 콜백 그래프 구성 함수

# 안개 발생 횟수
@callback(
    Output(component_id='fog_cnt_graph', component_property='figure'),
    Input(component_id='radio_time_type', component_property='value')
)
def select_fog_cnt(radio_button):
    
    if radio_button == 'hour':
        fog_cnt_graph = FOG_graph.fog_cnt_line_plot(fog_cnt_hour, radio_button)

    else:
        fog_cnt_graph = FOG_graph.fog_cnt_line_plot(fog_cnt_month, radio_button)

    return fog_cnt_graph

# 안개 지속 시간
@callback(
    Output(component_id='fog_size_graph', component_property='figure'),
    Input(component_id='radio_time_type', component_property='value')
)
def select_fog_size(radio_button):

    if radio_button == 'hour':
        fog_size_graph = FOG_graph.fog_size_line_plot(fog_size_hour, radio_button)

    else:
        fog_size_graph = FOG_graph.fog_size_line_plot(fog_size_month, radio_button)

    return fog_size_graph


# 변수 형태에 맞는 파생변수 그래프 띄우기
@callback(
    Output(component_id='derive_value_plot', component_property='figure'),
    Input(component_id='derived_val', component_property='value')
)
def print_derive_value_plot(selected_val):
    if selected_val == 'AWS 안개 발생 가능성': # 범주형 1개 변수
        derive_value_plot = FOG_graph.derive_value_category_plot(category_new_value)

    else: # 연속형 3개 변수
        derive_value_plot = FOG_graph.derive_value_continuous_plot(continuous_new_value, selected_val)

    return derive_value_plot

# SHAP을 활용한 변수 중요도 체크
@callback(
    Output(component_id='shap_plot', component_property='figure'),
    Input(component_id='shap_type', component_property='value')
)
def select_shap_plot_type(type_name):
    
    if type_name == '통합 확인':
        shap_plot = FOG_graph.get_shap_values(shap_values)

    elif type_name == '짙음':
        shap_plot = FOG_graph.get_shap_values_pick(high_shap)

    elif type_name == '중간':
        shap_plot = FOG_graph.get_shap_values_pick(mid_shap)

    elif type_name == '옅음':
        shap_plot = FOG_graph.get_shap_values_pick(low_shap)

    else:
        shap_plot = FOG_graph.get_shap_values_pick(no_shap)

    return shap_plot