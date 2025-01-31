#######################################################
# packages
import dash_bootstrap_components as dbc
from dash import html, dcc, callback, Output, Input, State, ctx
import os

#######################################################
# file imports
from style.pagestyle import CONTAINER_FIX, MANITTO_CARDS
from components import manittoFunction
from components.Manitto_values import design_sampels

#######################################################
# load data
dir = os.getcwd()

#######################################################
# 화면 구성 레이아웃
layout = dbc.Container([

    # 대시보드 제목
    html.Br(), # 띄어쓰기
    dbc.Row([
        html.H3(children='마니또 게임하기', style={"textAlign": "center"})
    ]),

    dbc.Row([
        html.Hr(), # 구분선
    ]),

    # 본문 내용
    dbc.Row([

        # 알고리즘 그림 넣기
        dbc.Col([
            dbc.Alert("샘플링 알고리즘 입니다.", color="primary"),
            html.Img(src = '/assets/Sampling_mindmap.png',
                        style={
                            "maxWidth": "2000px",  # 최대 너비
                            "maxHeight": "800px",  # 최대 높이
                            "display": "block",  # block 요소로 처리
                            "margin": "0 auto"  # 수평 가운데 정렬
                        }
            ),
        ], width = 4),
        
        # input 반영하기
        dbc.Col([
            dbc.Row([
                dbc.Alert("번호 순서대로 입력하신 후 오른쪽의 예시문을 확인하시고 전송 버튼을 누르면 전송됩니다.", color="primary"),
            ]),
            dbc.Row([

                # 주 입력칸
                dbc.Col([

                    # 1. login    
                    dbc.Row([
                        html.H4("1. 네이버 로그인", style = {'color':'#18bc9c'}), # 제목
                        html.Br(),
                        dbc.Col([
                            dbc.InputGroup(
                                [
                                    dbc.InputGroupText("ID", style={"width": "60px"}),
                                    dbc.Input(id="id_input", placeholder="아이디 입력"),
                                    dbc.InputGroupText("@naver.com"),
                                ],
                                className="mb-3",
                            ),
                            dbc.InputGroup(
                                [
                                    dbc.InputGroupText("PW", style={"width": "60px"}),
                                    dbc.Input(id="password_input", type="password", placeholder="비밀번호 입력"),
                                ],
                                className="mt-3"
                            ),
                        ]),
                    ]),

                    dbc.Row([
                        html.Br(),
                    ]),

                    # 2. data upload
                    dbc.Row([
                        html.Hr(), # 구분선
                        html.H4("2. 데이터 업로드", style = {'color':'#18bc9c'}), # 제목
                    ]),

                    dbc.Row([
                        dbc.Card(
                            dbc.CardBody([
                                dcc.Upload(
                                    id='upload_data',
                                    children=html.Div([
                                        'Drag and Drop 또는 ',
                                        html.A('파일 선택', style={'color': '#18bc9c'}),
                                    ]),
                                    style=MANITTO_CARDS,
                                    multiple=False
                                ),
                            ]), style={'boxShadow': '0 4px 8px rgba(0, 0, 0, 0.1)', 'borderRadius': '10px', 'width': '480px'}
                        ),
                    ]),

                    dbc.Row([
                        html.Div(id = "upload_feedback"),
                        # 데이터를 저장할 Store
                        dcc.Store(id='stored_data'),
                    ]),

                    dbc.Row([
                        html.Br(),
                    ]),

                    # 3. options
                    dbc.Row([
                        html.Hr(), # 구분선
                        html.H4("3. 옵션", style = {'color':'#18bc9c'}), # 제목
                    ]),

                    dbc.Row([
                        dbc.InputGroup(
                            [
                                dbc.InputGroupText("메일 제목"),
                                dbc.Input(id="title_input", placeholder="필수로 작성해주세요"),
                            ],
                            className="mb-3",
                        ),

                        dbc.InputGroup(
                            [
                                dbc.InputGroupText("호스트 이름"),
                                dbc.Input(id="host_name", placeholder="필수로 작성해주세요"),
                            ],
                            className="mb-3",
                        ),

                        dbc.InputGroup(
                            [
                                dbc.InputGroupText("가격 상한선"),
                                dbc.Input(id="price_input", placeholder="필수로 작성해주세요"),
                            ],
                            className="mb-3",
                        ),
                        

                        dbc.Row([
                            html.Br(),
                        ]),

                        html.H6('▣ 디자인 선택하기 ▣',
                            style={"textAlign": "center", "fontfamily": "NanumSquare"}
                        ),
                        dbc.Select(design_sampels,
                                    value = 'Christmas',
                                    id = 'design_samples'
                                ),

                        dbc.Row([
                            html.Br(),
                        ]),
                        html.H6('▣ 선택 옵션 ▣',
                            style={"textAlign": "center", "fontfamily": "NanumSquare"}
                        ),

                        dbc.Checklist(
                            options=[
                                {"label": "섬 없애기", "value": 1},
                            ],
                            value=[1],
                            id="island_yn",
                            switch=True,
                        ),
                    ]),

                ], width = 6),

                # 입력에 대한 확인
                dbc.Col([
                    dbc.Row([
                        html.H4("4. 업로드 데이터 확인", style = {'color':'#18bc9c'}), # 제목
                    ]),
                    
                    # 데이터 미리보기
                    dbc.Row([
                        dbc.Card(
                            [
                                dbc.CardHeader("▣ 업로드 된 데이터 미리보기 ▣"),
                                dbc.CardBody(
                                    html.Div(
                                        id="output_area",
                                        className="text-muted"
                                    )
                                ),
                            ],
                            className="shadow-sm rounded",
                            style={
                                "width": "480px",  # 고정 너비
                                "height": "300px",  # 고정 높이
                                "border": "1px solid #ddd",  # 테두리 추가 (선택 사항)
                                "padding": "10px",  # 내부 여백
                                "overflow": "hidden",  # 내용이 넘칠 경우 숨김
                                'margin': '10px',
                            },
                        ),
                    ]),

                    dbc.Row([
                        html.Div("최대 5행까지 보여집니다.", style = {"color": "#95a5a6"})
                    ]),

                    dbc.Row([
                            html.Br(),
                        ]),
                    
                    dbc.Row([
                        html.Hr(), # 구분선
                        html.H4("5. 내용 미리보기", style = {'color':'#18bc9c'}), # 제목
                    ]),

                    # 내용 미리보기
                    dbc.Row([
                        dbc.Card(
                            [
                                dbc.CardHeader("▣ 선택한 도안 내용 미리보기 ▣"),
                                dbc.CardBody(
                                    id = 'upload_contents', style={"maxHeight": "300px", "overflowY": "auto"}
                                ),
                            ],
                            className="shadow-sm rounded",
                            style={
                                "width": "480px",  # 고정 너비
                                "height": "300px",  # 고정 높이
                                "border": "1px solid #ddd",  # 테두리 추가 (선택 사항)
                                "padding": "10px",  # 내부 여백
                                "overflow": "hidden",  # 내용이 넘칠 경우 숨김
                                'margin': '10px',
                            },
                        ),
                    ]),

                    dbc.Row([
                        html.Br(),
                    ]),
                    
                    dbc.Row([
                        html.Hr(), # 구분선
                        html.H4("6. 전송하기", style = {'color':'#18bc9c'}), # 제목
                    ]),

                    dbc.Row([
                        dbc.Button('Submit', id='submit_value', n_clicks=0, color="secondary", className="me-1")    
                    ]),

                    dbc.Row([
                        html.Div(id='select_submit')
                    ]),

                ], width = 6),


            ]),
        ], width = 8),

        # output 관리하기 및 이메일 전송


    ]),
], style=CONTAINER_FIX
)

#######################################################
### 콜백 그래프 구성 함수

# 데이터 업로드
@callback(
    [Output("upload_feedback", "children"),
     Output("upload_feedback", "style"),
     Output("stored_data", "data")],
    [Input("upload_data", "contents")],
    [State("upload_data", "filename")]
)
def upload_csvfile(contents, filename):

    return manittoFunction.handle_file_upload(contents, filename)

# 업로드 된 데이터 확인
@callback(
    Output("output_area", "children"),
    Input("stored_data", "data")
)
def display_stored_data(data):
    
    return manittoFunction.retrieve_from_store(data)

# 마니또 내용 미리보기
@callback(
    Output("upload_contents", "children"),
    [
        Input("host_name", "value"),
        Input("price_input", "value"),
        Input("design_samples", "value"),
    ],
)
def select_design(host, price, design):
    
    return dcc.Markdown(manittoFunction.design_sample_text(host, price, design, '아담', '이브'))

# 이메일 전송하기
@callback(
    Output('select_submit', 'children'),
    Output('select_submit', 'style'),
    Input('submit_value', 'n_clicks'),
    Input('id_input', 'value'),
    Input('password_input', 'value'),
    Input('host_name', 'value'),
    Input('price_input', 'value'),
    Input('title_input', 'value'),
    Input('island_yn', 'value'),
    Input("design_samples", "value"),
    Input("stored_data", "data"),
)
def send_email_yesno(send, sendEmail, password, host, price, titles, buttons, design, data):
    
    if "submit_value" == ctx.triggered_id:
        try:
            manittoFunction.mail_sending(sendEmail, password, host, price, titles, buttons, design, data)

            return '메일 전송을 완료하였습니다!', {'color': '#18bc9c'}
    
        except Exception as e:
            return f'메일 전송에 실패하였습니다...{e}', {'color': '#e74c3c'}
        
    else:
        return 'submit 버튼을 눌러주세요', {'color': '#95a5a6'}