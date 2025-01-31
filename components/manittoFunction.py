from dash import html, dash_table
import pandas as pd
import numpy as np
import warnings
from collections import deque
import smtplib
from email.mime.text import MIMEText
import dash_bootstrap_components as dbc
import base64
import io
warnings.filterwarnings('ignore')

##################################################
### functions

# bfs로 랜덤 번호 뽑기
def bfs_for_manitto(k, manittodict):
    q = deque([[0, 1]])
    visit = [0 for _ in range(k)]
    while q:
        sample_num, cnt = q.popleft()
        visit[sample_num] = 1
        next_num = manittodict[sample_num]
        if visit[next_num] == 0:
            q.append([next_num, cnt+1])

    return cnt

# 섬 형태 생기지 않게 적용
def manitto_select_complete_shuffle(n):
    num = [c for c in range(n)]
    # reset = 0
    while True:
        # reset += 1
        sample = np.random.choice(num, size=n, replace = False)
        manittodict = {n:s for n, s in zip(num, sample)}
        k = bfs_for_manitto(n, manittodict)
        if k == n:
            break
            
    return list(manittodict.values())

# 섬 형태 생겨도 됨
def manitto_select(n):
    num = [c for c in range(n)]
    # reset = 0
    while True:
        # reset += 1
        sample = np.random.choice(num, size=n, replace = False)
        if all(s != n for s, n in zip(sample, num)):
            break
            
    manittodict = {n:s for n, s in zip(num, sample)}
    
    return list(manittodict.values())

# 최종적으로 섬 형태 포함 적용
def manitto_option(names, complete):
    n = len(names)
    if 1 in complete:
        angel = manitto_select_complete_shuffle(n)
        
    else:
        angel = manitto_select(n)
    
    select_manitto = [names[k] for k in angel]
    
    return select_manitto

# 데이터 생성 함수
def create_dataset(load_data, namecol, comp):
    load_data['manitto'] = manitto_option(load_data[namecol], complete = comp)
    return load_data

# 메일 보내기 함수
def mail_sending(sendEmail, password, host, price, titles, buttons, design, data):
    
    # email
    email = sendEmail + '@naver.com'

    # 데이터 불러오기
    load_data = pd.DataFrame(data) # 데이터 프레임으로 만들기
    col = load_data.columns # 열 이름 가져오기 (꼭 이름이 0번째, 이메일이 1번째로 올 수 있도록)

    # 데이터 만들기
    dataset = create_dataset(load_data, col[0], buttons)
    col = dataset.columns

    # 네이버 포트
    smtpName = "smtp.naver.com"
    smtpPort = 587
    
    for i in range(len(dataset)):
        # 메일 내용
        title = titles
        content = design_sample_text(host, price, design, dataset[col[0]][i], dataset[col[2]][i])
        msg = MIMEText(content)
        msg['From'] = email
        msg['To'] = dataset[col[1]][i]
        msg['Subject'] = title

        s = smtplib.SMTP(smtpName, smtpPort)
        s.starttls() # 오류나는 위치
        s.login(email, password)
        s.sendmail(email, load_data[col[1]][i], msg.as_string())
        s.close()

# 파일 업로더
def handle_file_upload(contents, filename):
    if not contents:
        return "CSV 형식으로된 예시처럼 만들어진 명단 파일을 업로드 해주세요", {"color": "#95a5a6"}, None

    try:
        # 파일이 CSV인지 확인
        if not filename.endswith(".csv"):
            return "CSV 형식으로 다시 업로드 해주세요", {"color": "#e74c3c"}, None

        # 데이터 읽기
        content_type, content_string = contents.split(",")
        decoded = io.StringIO(io.BytesIO(base64.b64decode(content_string)).read().decode('utf-8'))
        df = pd.read_csv(decoded)

        # `stored-data`에 데이터 저장
        return "파일 업로드 성공!", {"color": "#18bc9c"}, df.to_dict("records")

    except Exception as e:
        return "파일 처리 중 오류가 발생했습니다.", {"color": "#e74c3c"}, None
    

# 저장되어 있는 데이터 보여주기
def retrieve_from_store(data):
    if data is not None:
        
        # 데이터 셋
        dataset = pd.DataFrame(data)

        dash_div = dbc.Row([
            # 테이블 생성
            dash_table.DataTable(
                columns=[{"name": col, "id": col} for col in data[0].keys()],
                data=data[:5],
                style_table={'overflowX': 'auto'},
                style_cell={
                    'textAlign': 'left',
                    'padding': '10px',
                    'fontSize': '12px',
                    'fontFamily': 'NanumSquare'
                },
                style_header={
                    'backgroundColor': 'rgb(230, 230, 230)',
                    'fontWeight': 'bold'
                }
            ),

            # 테이블 정보 전달
            html.Div(f"총 {dataset.shape[0]}명이 참여합니다.", style = {"color": "#95a5a6"})
        ])

        # 저장된 데이터를 dash_table로 렌더링
        return dash_div
    return "No data to display. Please upload a file."

# 디자인 도안 넣기
def design_sample_text(host, price, design, reader, mt):

    if design == 'Christmas' and host and price:

        contents = f"""
        =============================================
                        스포 방지선
        =============================================

        ############################################# 
        host __{host}__: __{reader}__님! 마니또 선물 교환식 참여에  
        응해주셔서 감사합니다. 저희 마니또 진행 방식의 규칙은  
        다음과 같습니다.  

                        ! Rule !

        1. 해당되는 사람에게 없을 것 같은 물건
        2. 가격대는 __{str(price)}__원 이하로 선정
        3. 만약, 해당되는 사람이 가지고 있는 물건일 경우 벌칙을
        받습니다.

        host __{host}__: 참가자1님은 다음과 같은 사람의 마니또로 
                    선정되셨습니다. 심사숙고하셔서 벌칙을 면해봅시다!

                
        ********************************************
                    준비해야 하는 상대       
                        {mt}   
        ********************************************
                                    
                            ★
                            **        
                           ****
                          ******
                         ********
                        **********
                       ************
                      **************
                     ****************
                            ||
                            ||
                            ||
                
                #   Merry Christmas!   #
        #############################################
        """
        return contents
    return ""