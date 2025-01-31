#######################################################
# plotly
import plotly.express as px
import plotly.graph_objects as go

# model
import warnings
warnings.filterwarnings('ignore')

#######################################################
# 안개 건수 그래프 그리기
def fog_cnt_line_plot(dataframe, time_type):
    # Figure  생성
    fig = px.line(dataframe,
                    x = time_type,
                    y = 'cnt',
                    color = "지형종류",
                    markers=True)

    fig.update_layout(title_text=f"{time_type}에 따른 지역별 안개 발생 횟수",
                        title_x = 0.5,
                        title_xanchor = 'center',
                        title_font_color = 'black',
                        title_font_family = 'NanumSquare',
                        xaxis_title=f'{time_type}',
                        yaxis_title='안개 발생 횟수 (회)',
                        legend=dict(orientation="h", x=0.5, y=-0.2, xanchor="center", yanchor="top"),
                        showlegend=True,
                        # hovermode='x unified',
                        margin=dict(
                            b=100  # 아래쪽 마진 추가
                        ),
                        template='simple_white')

    return fig


# 안개 규모 그래프 그리기
def fog_size_line_plot(dataframe, time_type):
    # Figure  생성
    fig = px.line(dataframe,
                    x = time_type,
                    y = 'mean_last',
                    color = "안개 정도",
                    markers=True)

    fig.update_layout(title_text=f"{time_type}별 안개 규모에 따른 평균 지속시간",
                        title_x = 0.5,
                        title_xanchor = 'center',
                        title_font_color = 'black',
                        title_font_family = 'NanumSquare',
                        xaxis_title=f'{time_type}',
                        yaxis_title='평균 안개 지속시간 (minutes)',
                        legend=dict(orientation="h", x=0.5, y=-0.2, xanchor="center", yanchor="top"),
                        showlegend=True,
                        # hovermode='x unified',
                        margin=dict(
                            b=100  # 아래쪽 마진 추가
                        ),
                        template='simple_white')

    return fig


# 파생변수 종류에 따른 연속형 변수 그래프
def derive_value_continuous_plot(dataframe, columns):

    # 범례 이름 지정
    legend_labels = {
        1: '짙음',
        2: '중간',
        3: '옅음',
        4: '없음'
    }

    # Plotly Figure 객체 생성
    fig = go.Figure()

    # 그룹별로 Boxplot 추가
    for _, row in dataframe[dataframe['변수 종류'] == columns].iterrows():
        fig.add_trace(go.Box(
            q1 = [row['q1']],  # 1사분위수
            median = [row['median']],  # 중앙값
            q3 = [row['q3']],  # 3사분위수
            lowerfence = [row['lower_whisker']],  # 최소값
            upperfence = [row['upper_whisker']],  # 최대값
            name = legend_labels.get(row['class'], row['class']),  # 그룹 이름
            boxpoints = False     # 데이터 포인트 제외
        ))

    # 레이아웃 설정
    fig.update_layout(title_text=f"{columns}의 안개 농도 구간별 boxplpot",
                        title_x = 0.5,
                        title_xanchor = 'center',
                        title_font_color = 'black',
                        title_font_family = 'NanumSquare',
                        xaxis_title='안개 농도 구간',
                        yaxis_title=f'{columns}',
                        legend=dict(orientation="h", x=0.5, y=-0.2, xanchor="center", yanchor="top"),
                        showlegend=True,
                        # hovermode='x unified',
                        margin=dict(
                            b=100  # 아래쪽 마진 추가
                        ),
                        template='simple_white',
                        boxmode = 'group'
                        )

    return fig

# 파생변수 종류에 따른 범주형 변수 그래프
def derive_value_category_plot(dataframe):

    # Plotly 히트맵 생성
    fig = px.imshow(
        dataframe,
        text_auto=True,  # 셀 값 표시
        color_continuous_scale='Emrld'
    )

    fig.update_layout(title_text=f"AWS 위험 지수와 안개 생성 정도의 교차 분석",
                        title_x = 0.5,
                        title_xanchor = 'center',
                        title_font_color = 'black',
                        title_font_family = 'NanumSquare',
                        xaxis_title='AWS 안개 위험 지수(%)',
                        yaxis_title='안개의 농도 구간',
                        coloraxis_showscale=False,
                        template='simple_white')

    return fig

# SHAP summary plot
def get_shap_values(dataframe):

    fig_shap = px.bar(dataframe,
                        x='SHAP',
                        y='Variable',
                        color='class')
    
    fig_shap.update_layout(title_text="SHAP을 활용한 주요 요인 확인",
        title_x = 0.5,
        title_xanchor = 'center',
        title_font_color = 'black',
        title_font_family = 'NanumSquare',
        xaxis_title='판정 가능도',
        yaxis_title='요인',
        legend=dict(orientation="h", x=0.5, y=-0.2, xanchor="center", yanchor="top"),
        showlegend=True,
        hovermode='x unified',
        margin=dict(
            b=100  # 아래쪽 마진 추가
        ),
        template='simple_white')

    # 색상조절
    fig_shap.update_traces(# marker_color = 히스토그램 색, 
                        # marker_line_width = 히스토그램 테두리 두깨,                            
                        # marker_line_color = 히스토그램 테두리 색,
                        marker_opacity = 0.4,
                        )
    
    return fig_shap

# shap to plotly
def get_shap_values_pick(dataframe):

    # 하나씩 짤라서 읽기
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=dataframe['SHAP'],
        y=dataframe['Variable'],
        orientation='h'
    ))
    
    fig.update_layout(title_text="SHAP을 활용한 주요 요인 확인",
        title_x = 0.5,
        title_xanchor = 'center',
        title_font_color = 'black',
        title_font_family = 'NanumSquare',
        xaxis_title='변수 중요도(절댓값)',
        yaxis_title='요인',
        template='simple_white')

    # 색상조절
    fig.update_traces(# marker_color = 히스토그램 색, 
                        # marker_line_width = 히스토그램 테두리 두깨,                            
                        # marker_line_color = 히스토그램 테두리 색,
                        marker_opacity = 0.4,
                        )
    
    return fig