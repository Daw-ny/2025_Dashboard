#######################################################
# packages
import dash_bootstrap_components as dbc
from dash import html, dcc, callback, Output, Input
import pandas as pd
import os
import io
import base64
import pickle
import matplotlib.pyplot as plt
import shap
import matplotlib
import gc

import matplotlib
import matplotlib.font_manager as fm

# font_location = '/usr/share/fonts/truetype/nanum/NanumGothicOTF.ttf'
font_location = './assets/NanumSquareB.ttf' # For Windows

font_name = fm.FontProperties(fname=font_location).get_name()
matplotlib.rc('font', family=['NanumGothic', 'DejaVu Sans'])

plt.rcParams['axes.unicode_minus'] = False

# 수식 폰트를 DejaVu Sans로 설정
plt.rcParams['mathtext.fontset'] = 'custom'
plt.rcParams['mathtext.rm'] = 'DejaVu Sans'

matplotlib.use("Agg")  # GUI 백엔드 비활성화

#######################################################
# file imports
from components.Baby_preprocessing import preprocessing
from components.Baby_dtype import DI, IVF, BLASTOCYST, AH

#######################################################
# load data
dir = os.getcwd()

#######################################################
# 데이터 업로드 함수
def sample_file_upload(contents, filename):
    if not contents:
        return "CSV 형식으로된 진단 목록 파일을 업로드 해주세요", {"color": "#95a5a6"}, None, None

    try:
        # 파일이 CSV인지 확인
        if not filename.endswith(".csv"):
            return "CSV 형식으로 다시 업로드 해주세요", {"color": "#e74c3c"}, None, None

        # 데이터 읽기
        content_type, content_string = contents.split(",")
        decoded = io.StringIO(io.BytesIO(base64.b64decode(content_string)).read().decode('utf-8'))
        df = pd.read_csv(decoded)
        preprocessed_df = preprocessing(df)

        # `stored_data`에 데이터 저장, `preprocessed_store_data`에 전처리 데이터 저장
        return "파일 업로드 성공!", {"color": "#18bc9c"}, df.to_dict("records"), preprocessed_df.to_dict("records")

    except Exception as e:
        return "파일 처리 중 오류가 발생했습니다.", {"color": "#e74c3c"}, None, None
    

# 병력 추가하기 리스트
def patient_illness(data):

    ls = []
    for i in ['남성 주 불임 원인', '남성 부 불임 원인', '여성 주 불임 원인', '여성 부 불임 원인','부부 주 불임 원인', '부부 부 불임 원인', '불명확 불임 원인', '불임 원인 - 난관 질환',
        '불임 원인 - 남성 요인', '불임 원인 - 배란 장애', '불임 원인 - 여성 요인', '불임 원인 - 자궁경부 문제', '불임 원인 - 자궁내막증', '불임 원인 - 정자 농도', '불임 원인 - 정자 면역학적 요인',
        '불임 원인 - 정자 운동성', '불임 원인 - 정자 형태']:

        if data[i] == 1:
            ls.append(html.Div([i]))

    return ls


# di 확률 구하기
def di_prob_cal(index, data):

    # 데이터 index에 해당하는 번호 픽
    dt = pd.DataFrame(data)
    row = dt.loc[[index], :]

    di_dt, _ = DI(row)

    dir = './models/'
    
    # XGBoost, LightGBM, CatBoost, Ensemble Modeling
    with open(dir + "xgb_best_model_DI.pkl", "rb") as f:
        xgb_di = pickle.load(f)

    with open(dir + "lgbm_best_model_DI.pkl", "rb") as f:
        lgbm_di = pickle.load(f)

    with open(dir + "cat_best_model_DI.pkl", "rb") as f:
        cat_di = pickle.load(f)   

    # prob with data
    xgb_prob = round(float(xgb_di.predict_proba(di_dt)[:, 1][0]*100), 2) 
    lgbm_prob = round(lgbm_di.predict_proba(di_dt)[:, 1][0]*100, 2) 
    cat_prob = round(cat_di.predict_proba(di_dt)[:, 1][0]*100, 2) 

    # ensemble prob
    w1 = 1
    w2 = 1
    w3 = 1
    ensemble_prob = round((xgb_prob * w1 + lgbm_prob * w2 + cat_prob * w3) / (w1 + w2 + w3), 2)

    # 결과 표시
    xgb_result = [html.Span(f"{xgb_prob}", style={"fontWeight": "bold", "color": "#2C3E50", "fontSize": "25px"}), "%"]
    lgbm_result = [html.Span(f"{lgbm_prob}", style={"fontWeight": "bold", "color": "#2C3E50", "fontSize": "25px"}), "%"]
    cat_result = [html.Span(f"{cat_prob}", style={"fontWeight": "bold", "color": "#2C3E50", "fontSize": "25px"}), "%"]
    ensemble_result = [html.Span(f"{ensemble_prob}", style={"fontWeight": "bold", "color": "#2C3E50", "fontSize": "25px"}), "%"]
    total_result = [
        html.Span(f"환자 {row['ID'].values[0]}님의 임신 성공 확률은 ", style={"fontWeight": "bold", "color": "#2C3E50", "fontSize": "30px"}),
        html.Span(f"{ensemble_prob}%", style={"fontWeight": "bold", "color": "#e74c3c", "fontSize": "30px"}),
        html.Span("입니다.", style={"fontWeight": "bold", "color": "#2C3E50", "fontSize": "30px"})
    ]
    
    return xgb_result, lgbm_result, cat_result, ensemble_result, total_result


def ivf_prob_cal(index, data):

    # 데이터 index에 해당하는 번호 픽
    dt = pd.DataFrame(data)
    row = dt.loc[[index], :]

    dir = './models/'
    
    if row['특시유_AH'].values:

        ivf_dt = AH(row)
        
        # XGBoost, LightGBM, CatBoost, Ensemble Modeling
        with open(dir + "xgb_best_model_AH.pkl", "rb") as f:
            xgb_ivf = pickle.load(f)

        with open(dir + "lgbm_best_model_AH.pkl", "rb") as f:
            lgbm_ivf = pickle.load(f)

        with open(dir + "cat_best_model_AH.pkl", "rb") as f:
            cat_ivf = pickle.load(f)   


    elif row['특시유_BLASTOCYST'].values:
        
        ivf_dt = BLASTOCYST(row)

        # XGBoost, LightGBM, CatBoost, Ensemble Modeling
        with open(dir + "xgb_best_model_BLASTOCYST.pkl", "rb") as f:
            xgb_ivf = pickle.load(f)

        with open(dir + "lgbm_best_model_BLASTOCYST.pkl", "rb") as f:
            lgbm_ivf = pickle.load(f)

        with open(dir + "cat_best_model_BLASTOCYST.pkl", "rb") as f:
            cat_ivf = pickle.load(f)   

    else:
        ivf_dt, _ = IVF(row)

        # XGBoost, LightGBM, CatBoost, Ensemble Modeling
        with open(dir + "xgb_best_model_IVF.pkl", "rb") as f:
            xgb_ivf = pickle.load(f)

        with open(dir + "lgbm_best_model_IVF.pkl", "rb") as f:
            lgbm_ivf = pickle.load(f)

        with open(dir + "cat_best_model_IVF.pkl", "rb") as f:
            cat_ivf = pickle.load(f)   

    # prob with data
    xgb_prob = round(float(xgb_ivf.predict_proba(ivf_dt)[:, 1][0]*100), 2) 
    lgbm_prob = round(lgbm_ivf.predict_proba(ivf_dt)[:, 1][0]*100, 2) 
    cat_prob = round(cat_ivf.predict_proba(ivf_dt)[:, 1][0]*100, 2) 

    # ensemble prob
    w1 = 1
    w2 = 1
    w3 = 1
    ensemble_prob = round((xgb_prob * w1 + lgbm_prob * w2 + cat_prob * w3) / (w1 + w2 + w3), 2)
    
    # 결과 표시
    xgb_result = [html.Span(f"{xgb_prob}", style={"fontWeight": "bold", "color": "#2C3E50", "fontSize": "25px"}), "%"]
    lgbm_result = [html.Span(f"{lgbm_prob}", style={"fontWeight": "bold", "color": "#2C3E50", "fontSize": "25px"}), "%"]
    cat_result = [html.Span(f"{cat_prob}", style={"fontWeight": "bold", "color": "#2C3E50", "fontSize": "25px"}), "%"]
    ensemble_result = [html.Span(f"{ensemble_prob}", style={"fontWeight": "bold", "color": "#2C3E50", "fontSize": "25px"}), "%"]
    total_result = [
        html.Span(f"환자 {row['ID'].values[0]}님의 임신 성공 확률은 ", style={"fontWeight": "bold", "color": "#2C3E50", "fontSize": "30px"}),
        html.Span(f"{ensemble_prob}%", style={"fontWeight": "bold", "color": "#e74c3c", "fontSize": "30px"}),
        html.Span("입니다.", style={"fontWeight": "bold", "color": "#2C3E50", "fontSize": "30px"})
    ]

    return xgb_result, lgbm_result, cat_result, ensemble_result, total_result

def fig_to_uri(fig):
    if 'buf' in globals():
        try:
            globals()['buf'].close()
        except Exception:
            pass
        del globals()['buf']
    if 'buf' in locals():
        try:
            buf.close()
        except Exception:
            pass
        del buf
    
    gc.collect()
    
    buf = io.BytesIO()
    fig.savefig(buf, format="png", bbox_inches='tight')
    buf.seek(0)
    encoded = base64.b64encode(buf.read()).decode('utf-8')
    
    buf.close()
    del buf 
    gc.collect()
    
    plt.close(fig)
    return f'data:image/png;base64,{encoded}'

def shap_to_uri(explainer, data):
    
    # 데이터 받아오기
    target = data.iloc[0, :]

    # shap_values 계산
    shap_values = explainer.shap_values(target)

    # 기댓값
    expected_value = explainer.expected_value

    # waterfall 형성
    explanation = shap.Explanation(values=shap_values,
                                    base_values=expected_value,
                                    data=target,
                                    feature_names=data.columns)
    
    fig = plt.figure()
    shap.plots.waterfall(explanation, show=False)
    uri = fig_to_uri(fig)
    return uri

def make_force(explainer, data):

    uri = shap_to_uri(explainer, data)

    return html.Img(src=uri, style={'width':'100%'})