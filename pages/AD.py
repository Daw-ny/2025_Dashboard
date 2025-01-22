#######################################################
# packages
import dash_bootstrap_components as dbc
from dash import html, dcc, callback, Output, Input
import pandas as pd
import os

#######################################################
# file imports
from components import AD_graph, AD_values, AD_table
from style.pagestyle import CONTAINER_FIX

#######################################################
# load data
dir = os.getcwd()
simul1 = pd.read_csv(dir + "/data/simul1.csv") #시뮬레이션런1 샘플 데이터
colnames = AD_values.cols_distance #순서를 나타내는 변수 제외 변수 목록
corrdata = pd.read_csv(dir + '/data/ad_val_corr.csv') #상관관계 변수
df_normal = pd.read_csv(dir + '/data/test_X_scaler_normal.csv') #정상으로 분류된 test data
df_anomaly = pd.read_csv(dir + '/data/test_X_scaler_anomaly.csv') #이상으로 분류된 test data

#######################################################
# 화면 구성 레이아웃
layout = dbc.Container([
    # 대시보드 제목
    html.Br(), # 띄어쓰기
    dbc.Row([
        html.H3(children='효율적인 One-Class 이상치 탐지: 화학공정 데이터를 활용한 시각화', style={"textAlign": "center"})
    ]),

    dbc.Row([
        html.Hr() # 구분선
    ]),

    # 구성 요소 3중으로 나눠서 펼치기
    dbc.Row([

        dbc.Col([
            dbc.Alert("변수간의 상관관계를 확인 하였습니다.", color="primary"),

            dbc.Row([
                dbc.Col([
                    dcc.Dropdown(colnames,
                        value = 'xmeas_1',
                        id = 'corr_var1'
                    ),
                ]),
                
                dbc.Col([
                    dcc.Dropdown(colnames,
                        value = 'xmeas_2',
                        id = 'corr_var2'
                    ),
                ]),

            ]),
            
            # 상관관계 그래프 표시하기
            dcc.Graph(figure={}, id='corr_graph'),

            dbc.Alert("StandardScaler을 적용한 ML F1-score 비교", color="primary"),
            
            # 테이블 불러오기
            AD_table.MLtable

        ], width=4),

        dbc.Col([

            dbc.Alert("가장 성능이 좋은 앙상블 모형에서 k-means를 이용하여 사후 분석을 진행하였습니다.", color="primary"),
            html.H6('알고리즘 계산에서 정상과 이상의 평균 차이가 가장 큰 5가지의 변수를 확인할 수 있습니다.'),

            # top 5 graph 대입
            dbc.Row([
                dcc.Dropdown(['xmv_5', 'xmeas_16', 'xmeas_7', 'xmeas_13', 'xmv_2'],
                    value = 'xmv_5',
                    id = 'top5_variables'
                ),
            ]),

            html.Br(),
            dbc.Row([
                    dcc.Graph(figure={}, id='top5_graph')
            ]),

            # 결과 및 활용방안
            dbc.Row([

                dbc.Alert("분석으로 인한 주요점과 추후 개선 방향에 대해 작성하였습니다.", color="primary"),

                dbc.Accordion(
                    [
                        dbc.AccordionItem(
                            "샘플 번호 100 - 200 사이를 집중적으로 감시하는 것을 권장합니다.",
                            title="160번째 샘플 이후 이상 판정된 값의 변동이 심해지는 것을 확인하였습니다.",
                            style={"backgroundColor": "#18bc9c", "color": "white"}
                        ),
                        dbc.AccordionItem(
                            "변수 선택법 또는 너무 강한 상관관계를 갖는 변수를 제외한 나머지 변수로 적합을 시도할 수 있습니다.",
                            title="변수간의 상관관계의 절댓값이 1과 가까운 값이 존재합니다.",
                            style={"backgroundColor": "#18bc9c", "color": "white"}
                        ),
                    ],
                    start_collapsed=True,
                ),
            ]),

        ], width=8),
    ]),

], style=CONTAINER_FIX
)

#######################################################
# 콜백 그래프 구성 함수

## corr graph
@callback(
    Output(component_id='corr_graph', component_property='figure'),
    Input(component_id='corr_var1', component_property='value'),
    Input(component_id='corr_var2', component_property='value')
)
def get_corr_graph(first, second):
    figure = AD_graph.plot_pairs(simul1, corrdata, first, second)
    return figure

## top 5 graph

@callback(
    Output(component_id='top5_graph', component_property='figure'),
    Input(component_id='top5_variables', component_property='value')
)
def get_effective_top_5(col_chooser):
    figure = AD_graph.effective_value_top_5(df_normal, df_anomaly, col_chooser)
    return figure