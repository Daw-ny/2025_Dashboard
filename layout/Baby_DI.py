#######################################################
# packages
import dash_bootstrap_components as dbc
from dash import html, callback, Output, Input, State, dcc
import pickle
import pandas as pd
import xgboost, catboost, lightgbm
import warnings
warnings.filterwarnings("ignore", category=UserWarning)

#######################################################
# file imports
from components.Baby_Function import di_prob_cal, make_force
from components.Baby_graph_functions import make_pie, make_bar
from components.Baby_Input import DI_value
from components.Baby_dtype import DI

#######################################################
# 레이아웃
layout = [
    dbc.Row([
        dbc.Col([
            dbc.Row([
                dbc.Col([
                    dcc.Graph(figure={}, id = 'pie_chart_patient_age_di')
                ],width = 6),

                dbc.Col([
                    dcc.Graph(figure={}, id = 'pie_chart_donate_age_di')
                ],width = 6),
            ]),

            dbc.Row([
                dbc.Col([
                    html.H6(id = "pie_chart_patient_owner_di", style={"textAlign": "center"})
                ],width = 6),

                dbc.Col([
                    html.H6(id = "pie_chart_donate_owner_di", style={"textAlign": "center"})
                ],width = 6),
            ]),

            dbc.Row([
                dcc.Dropdown(
                    DI_value,
                    value='DI 시술 횟수',
                    id='bar_chart_DI',
                    searchable=False,
                    clearable=False,
                    style={'width': '50%', 'margin': '0 auto'}
                ),
            ]),

            dbc.Row([
                dcc.Graph(figure={}, id = 'bar_chart_patient_experience_di')
            ]),
        ], width = 6),

        dbc.Col([
            dbc.Row([
                html.Div(id = 'shap_plot_di')
            ]),

            dbc.Row([
                html.Br()
            ]),
            
            dbc.Row([
                dbc.Card([
                    dbc.CardHeader(html.Span("SHAP 그래프 해석 방법", style={"fontWeight": "bold", "color": "#F39C12"}),
                        className="d-flex align-items-start justify-content-center"),
                    dbc.CardBody(
                            [
                                dbc.Row([
                                    html.Ol([
                                        html.Li(["좌측에 있는 변수 순서는 해당 환자에게 ",
                                                html.Span("영향력이 높은 순서", style={"fontWeight": "bold", "color": "#E95420"}),
                                                "대로 나열되어 있습니다."]),
                                        html.Li(["변수 옆에 ",
                                                html.Span("실제 샘플의 값이 무엇", style={"fontWeight": "bold", "color": "#E95420"}),
                                                "인지 볼 수 있습니다."]),
                                        html.Li([html.Span("붉은 색", style={"fontWeight": "bold", "color": "#E95420"}),
                                                "은 임신 성공률이 높도록 작용한 요인임을 의미하며, ",
                                                html.Span("푸른색", style={"fontWeight": "bold", "color": "#3498DB"}),
                                                "은 임신 성공률이 낮도록 작용한 요인임을 의미합니다."]),
                                    ]),
                                ]),
                                dbc.Row([
                                    html.Span("유의점 : 시술 당시 나이와 같은 일부 변수는 매핑이 존재할 수 있습니다. 같이 확인해 주시기 바랍니다.", style={"color": "#3498DB"})
                                ]),
                            ],
                        className="align-items-start justify-content-start",
                        style={"height": "200px"}  # 카드 높이 지정 (원하는 크기로 조절 가능)
                    )
                ])
            ]),
        ]),
    ]),
    
    

    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader(html.Span("XGBoost", style={"fontWeight": "bold", "color": "#F39C12"}),
                    className="d-flex align-items-start justify-content-center"),
                dbc.CardBody(
                    html.Div(id = "xgb_perc_di"),
                    className="d-flex align-items-start justify-content-center",
                    style={"height": "50px"}  # 카드 높이 지정 (원하는 크기로 조절 가능)
                )
            ])
        ]),
        dbc.Col([
            dbc.Card([
                dbc.CardHeader(html.Span("LightGBM", style={"fontWeight": "bold", "color": "#F39C12"}),
                    className="d-flex align-items-start justify-content-center"),
                dbc.CardBody(
                    html.Div(id = "lgbm_perc_di"),
                    className="d-flex align-items-start justify-content-center",
                    style={"height": "50px"}  # 카드 높이 지정 (원하는 크기로 조절 가능)
                )
            ])
        ]),
        dbc.Col([
            dbc.Card([
                dbc.CardHeader(html.Span("CatBoost", style={"fontWeight": "bold", "color": "#F39C12"}),
                    className="d-flex align-items-start justify-content-center"),
                dbc.CardBody(
                    html.Div(id = "cat_perc_di"),
                    className="d-flex align-items-start justify-content-center",
                    style={"height": "50px"}  # 카드 높이 지정 (원하는 크기로 조절 가능)
                )
            ])
        ]),
        dbc.Col([
            dbc.Card([
                dbc.CardHeader(html.Span("Ensemble", style={"fontWeight": "bold", "color": "#F39C12"}),
                    className="d-flex align-items-start justify-content-center"),
                dbc.CardBody(
                    html.Div(id = "ensemble_perc_di"),
                    className="d-flex align-items-start justify-content-center",
                    style={"height": "50px"}  # 카드 높이 지정 (원하는 크기로 조절 가능)
                )
            ])
        ]),
    ]),

    dbc.Row([
        html.Br()
    ]),

    dbc.Card([
        dbc.CardHeader(html.Span("Results", style={"fontWeight": "bold", "color": "#F39C12"}),
                    className="d-flex align-items-start justify-content-center"),
        dbc.CardBody(
            html.Div(id = "ensemble_result_di"),
            className="d-flex align-items-start justify-content-center",
            style={"height": "80px"}  # 카드 높이 지정 (원하는 크기로 조절 가능)
        )
    ])

]
#######################################################
# callbacks
# probs
@callback(
    [
        Output("xgb_perc_di", "children"),    
        Output("lgbm_perc_di", "children"),    
        Output("cat_perc_di", "children"),    
        Output("ensemble_perc_di", "children"),
        Output("ensemble_result_di", "children"),
    ],
    [Input("index_store", "data"), State("preprocessed_store_data", "data")]
)
def cal_prob(index, data):

    return di_prob_cal(index, data)

@callback(
    [
        Output('pie_chart_patient_age_di', 'figure'),
        Output('pie_chart_patient_owner_di', 'children')
    ],
    [
        Input('index_store', 'data'),
        State('baby_stored_data', 'data'),
    ]
)
def piechart_patient_DI(index, data):

    # 데이터 불러와서 index 번호 고르기
    dt = pd.DataFrame(data)
    row = dt.loc[[index], :]

    # 그래프 그릴 데이터 불러오기
    count_data = pd.read_csv('./Data/DI_시술 당시 나이.csv')

    return make_pie(data = count_data, col = '시술 당시 나이', select_value = row['시술 당시 나이'].values), html.P('환자 나이 파이차트')

@callback(
    [
        Output('pie_chart_donate_age_di', 'figure'),
        Output('pie_chart_donate_owner_di', 'children')
    ],
    [
        Input('index_store', 'data'),
        State('baby_stored_data', 'data'),
    ]
)
def piechart_donate_DI(index, data):

    # 데이터 불러와서 index 번호 고르기
    dt = pd.DataFrame(data)
    row = dt.loc[[index], :]

    # 그래프 그릴 데이터 불러오기
    count_data = pd.read_csv('./Data/DI_정자 기증자 나이.csv')

    return make_pie(data = count_data, col = '정자 기증자 나이', select_value = row['정자 기증자 나이'].values), html.P('기증자 나이 파이차트')


@callback(
    Output('bar_chart_patient_experience_di', 'figure'),
    [
        Input('index_store', 'data'),
        State('baby_stored_data', 'data'),
        Input('bar_chart_DI', 'value')
    ]
)
def bar_chart_patient_experience(index, data, value):

    # 데이터 불러와서 index 번호 고르기
    dt = pd.DataFrame(data)
    row = dt.loc[[index], :]

    # 그래프 그릴 데이터 불러오기
    count_data = pd.read_csv('./Data/DI_'+ value +'.csv')

    return make_bar(data = count_data, col = value, select_value = row[value].values)


@callback(
    Output("shap_plot_di", "children"),
    [
        Input('index_store', 'data'),
        State('preprocessed_store_data', 'data')
    ]
)
def make_shap_graph_by_xgb(index, data):

    # 데이터 불러와서 index 번호 고르기
    dt = pd.DataFrame(data)
    row = dt.loc[[index], :]

    # DI, IVF에 따라 결과 다르게 산출하기
    di_dt, _ = DI(row)

    dir = './Models/'
    
    # XGBoost, LightGBM, CatBoost, Ensemble Modeling
    with open(dir + "test_exp_DI.pkl", "rb") as f:
        xgb_di = pickle.load(f)

    return make_force(xgb_di, di_dt)