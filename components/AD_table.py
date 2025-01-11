#######################################################
# dash
from dash import dash_table
import pandas as pd

#######################################################
# ML성능 table 원소 넣기

## 샘플 데이터프레임 생성
df = pd.DataFrame({
    'Models': ['OCSVM', 'K-means', 'AutoEncoder', 'AutoEncoder + k-means', 'Hard Voting(SVM, K-menas)'],
    'Public': [0.9091, 0.9204, 0.6360, 0.8531, 0.9099],
    'Private': [0.9041, 0.9000, 0.6235, 0.8638, 0.9091]
})

# 테이블 생성
MLtable = dash_table.DataTable(
    id='MLtable',
    columns=[
        {"name": "Models", "id": "Models"},
        {"name": "Public", "id": "Public"},
        {"name": "Private", "id": "Private"}
    ],
    data=df.to_dict('records'),
    style_header={
        'backgroundColor': '#95a5a6',  # Flatly Dark 색상
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
                'filter_query': '{Private} >= 0.905'
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