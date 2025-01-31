#######################################################
# packages
import dash_bootstrap_components as dbc
from dash import html, dcc, callback, Output, Input
import pandas as pd
import os

#######################################################
# file imports
from components import liver_values, liver_graph
from style.pagestyle import CONTAINER_FIX

#######################################################
# load data
dir = os.getcwd()
liver_count = pd.read_csv(dir + '/data/liver_count.csv')
liver_perc = pd.read_csv(dir + '/data/liver_perc.csv')
cancer_death = pd.read_csv(dir + '/data/cancer_death.csv')
cirrhosis_data = pd.read_csv(dir + '/data/cirrhosis_setting.csv')
basic_analysis = pd.read_csv(dir + '/data/basic_analysis.csv')
tukey_analysis = pd.read_csv(dir + '/data/tukey_analysis.csv')

#######################################################
# 화면 구성 레이아웃
layout = dbc.Container([
    # 대시보드 제목
    html.Br(), # 띄어쓰기
    dbc.Row([
        html.H3(children='Exploring Risk Factors for Liver Disease', style={"textAlign": "center"})
    ]),

    dbc.Row([
        html.Hr() # 구분선
    ]),

    dbc.Row([
        # 왼쪽 그래프
        dbc.Col([

            dbc.Alert("간암으로 인한 사망에 대한 국가별 비교 그래프입니다.", color="secondary"),

            dbc.Row([
                dcc.Dropdown(['숫자', '비율'],
                    value = '숫자',
                    id = 'ani_graph_type', 
                    searchable=False,
                    clearable=False
                ),
            ]),

            dbc.Row([
                dcc.Graph(figure={}, id='ani_graph')
            ]),

        ], width=6),

        # 오른쪽 그래프
        dbc.Col([

            dbc.Alert("한국에서 간암의 위험성에 대한 추세가 증가하고 있습니다.", color="secondary"),

            dbc.Row([
                dcc.Graph(figure=liver_graph.cancer_death_graph(cancer_death), id='cancer_death_graph')
            ]),

        ], width=6),

    ]),

    dbc.Row([
        html.Br() # 공백
    ]),

    dbc.Row([

        dbc.Col([

            # 왼쪽 그래프
            dbc.Alert("Cirrhosis에 관한 데이터 분포와 집단간 분포에 대한 분석 결과입니다.", color="secondary"),   

            dbc.Form([
                dbc.Row([
                    dbc.Label("▣ Select Value", width={"size": 4, "order": 1, "offset": 2}),
                    dbc.Col([
                        dcc.Dropdown(liver_values.vars,
                        value = 'N_Days',
                        id = 'cirrhosis_basic_value', 
                        searchable=False,
                        clearable=False
                        ),
                    ], width = {"size": 4, "order": 4}),
                ], className="g-2")
            ]),

            dbc.Row([

                # 그래프
                dbc.Col([
                    dcc.Graph(figure={}, id='cirrhosis_basic_graph')
                ]),
                
                # 결과 카드
                dbc.Col([
                    dbc.Row([
                        html.Br(),
                        html.Br(),
                        html.Br()
                    ]),
                    dbc.Row([
                        html.Div(id = 'analysis_result'),
                    ])
                ]),
            ]),
        ], width = 7),

        dbc.Col([

            # 오른쪽 그래프
            dbc.Alert("Tukey의 사후 검정으로 연속형 변수에 대한 신뢰구간을 표시했습니다.", color="secondary"),

            dbc.Row([
                dcc.Dropdown(liver_values.tukey_vals,
                    value = 'N_Days',
                    id = 'tukey_type',
                    searchable=False,
                    clearable=False,
                    style={
                        'width': '300px',   # 너비 조정
                    }
                ),
            ], justify="center"),

            dbc.Row([
                dcc.Graph(figure={}, id='tukey_graph')
            ]),

            
        ], width = 5),
    ])

], style=CONTAINER_FIX
)

#######################################################
# 콜백 그래프 구성 함수

# 암에 관한 나라별 비교
@callback(
    Output(component_id='ani_graph', component_property='figure'),
    Input(component_id='ani_graph_type', component_property='value')
)
def select_ani_type(types):
    if types == '숫자':

        return liver_graph.bar_ani_count(liver_count, liver_values.years)
    
    elif types == '비율':
        
        return liver_graph.bar_ani_perc(liver_perc, liver_values.years)
    
# Cirrhosis Values Graph
@callback(
    Output(component_id='cirrhosis_basic_graph', component_property='figure'),
    Input(component_id='cirrhosis_basic_value', component_property='value')
)
def display_cirrhosis_basic_graph(col):

    return liver_graph.cirrhosis_demographic_plot(cirrhosis_data, col)

# 분석 결과 가져오기
@callback(
    Output(component_id='analysis_result', component_property='children'),
    Input(component_id='cirrhosis_basic_value', component_property='value')
)
def display_analysis_result(col):

    select = basic_analysis[basic_analysis['변수'] == col].reset_index(drop = True)

    # 결과 문장 만들기
    div = dbc.Card([
        dbc.CardHeader([
            html.H4("분석 결과", style = {'color':'#18bc9c'}),  # 제목
        ]),
        dbc.CardBody([
            html.P([    
                html.Span(f"{col}", style={"color": "#f39c12", "fontWeight": "bold"}),
                "의 변수타입은 ",
                html.Span(f"{select['변수타입'][0]}", style={"color": "#f39c12", "fontWeight": "bold"}),
                "입니다."
            ]),

            html.P([
                "따라서 분석 검정 방법은",
                html.Span(f"{select['분석방법'][0]}", style={"color": "#f39c12", "fontWeight": "bold"}),
                "이며 간의 Stage 정도에 따라 차이가 없다는 귀무가설에 대한 P-value는 ",
                html.Span(f"{select['P-value'][0]}", style={"color": "#f39c12", "fontWeight": "bold"}),
                "입니다."
            ]),
            
            html.P([
                f"분석 결과에 따라 {col}은(는) Stage 단계를 구분할 수 있는가에 대한",
                html.Span(f"{select['변수유의'][0]}", style={"color": "#f39c12", "fontWeight": "bold"}),
                "라고 할 수 있습니다.",
            ]),
        ])
    ])
    
    return div

# Tukey Graph
@callback(
    Output(component_id='tukey_graph', component_property='figure'),
    Input(component_id='tukey_type', component_property='value')
)
def display_cirrhosis_basic_graph(col):

    return liver_graph.tukey_ci_plot(tukey_analysis, col)