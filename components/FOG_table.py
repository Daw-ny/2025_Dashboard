#######################################################
# dash
from dash import dash_table
import pandas as pd

#######################################################
# ML성능 table 원소 넣기

## 샘플 데이터프레임 생성
df = pd.DataFrame({
    'Models': ['Catboost', 'Catboost', 'Catboost', 'Catboost', 'Catboost'],
    'Method': ['Baseline', 'TimeSeriesSplit', '이상치 후처리', '푸리에변환 + StratifiedSplit', '푸리에변환 + Holdout 8:2'],
    'CIS score': [0.051, 0.067, 0.096, 0.118, 0.123]
})

# 테이블 생성
MLtable = dash_table.DataTable(
    id='MLtable',
    columns=[
        {"name": "Models", "id": "Models"},
        {"name": "Method", "id": "Method"},
        {"name": "CIS score", "id": "CIS score"}
    ],
    data=df.to_dict('records'),
    style_header={
        'backgroundColor': '#34495e',  
        'color': 'white',
        'fontWeight': 'bold',
        'textAlign': 'center'
    },
    # 기본 스타일
    style_data={
        'backgroundColor': '#ecf0f1',  # 기본 배경색 (Flatly의 기본 Light 색)
        'color': 'black',  # 기본 텍스트 색상 (Flatly Primary 색)
        'textAlign': 'center'
    },
    style_data_conditional=[
        # Highlight가 'Yes'인 경우 Success 색상 강조
        {
            'if': {
                'filter_query': '{CIS score} >= 0.121'
            },
            'backgroundColor': '#18bc9c',  # Success 색상
            'color': 'white',
            'textAlign': 'center'
        }
    ],
    style_table={'overflowX': 'auto'},  
    style_cell={'textAlign': 'center', 'padding': '10px'}
)


# Primary	#2c3e50	주 색상
# Light	#ecf0f1	밝은 배경 색상
# Success	#18bc9c	성공 상태 색상
# Danger	#e74c3c	오류 상태 색상
# Warning	#f39c12	경고 상태 색상
# Info	#3498db	정보 상태 색상
# Dark	#34495e	어두운 색상
# Secondary	#95a5a6	보조 색상