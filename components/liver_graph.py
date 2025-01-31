#######################################################
# plotly
from plotly.subplots import make_subplots
import plotly.express as px
import plotly.graph_objects as go
import os
import pandas as pd

# model
import warnings
warnings.filterwarnings('ignore')

#######################################################
def bar_ani_count(tl, years):

    # Bar Plot 생성
    fig = go.Figure()

    def get_colors_for_year(year, tl):
        colors = ['#e74c3c' if country == 'South Korea' else 'lightslategray' for country in tl[tl["Year"] == year]["Entity"]]
        return colors

    frames = [
        go.Frame(
            data=[go.Bar(x=tl[tl["Year"] == year]["Entity"], y=tl[tl["Year"] == year]["counts/(1000명)"], marker_color=get_colors_for_year(year, tl))],
            name=str(year)
        )
        for year in years
    ]

    fig = go.Figure(
        data=[go.Bar(x=tl[tl["Year"] == years[0]]["Entity"], y=tl[tl["Year"] == years[0]]["counts/(1000명)"], marker_color=get_colors_for_year(1990, tl))],
        layout=go.Layout(
            title="연도별 Entity 데이터 변화",
            xaxis=dict(title="Country"),
            yaxis=dict(title="counts/(1000명)"),
            updatemenus=[{
                "buttons": [
                    {
                        "args": [None, {"frame": {"duration": 750, "redraw": True}, 'fromcurrent':True}],
                        "label": "▶",
                        "method": "animate"
                    },
                    {
                        "args": [[None], {"frame": {"duration": 0, "redraw": False}, "mode": "immediate"}],
                        "label": "❚❚",
                        "method": "animate"
                    }
                ],
                "direction": "left",
                "pad": {"r": 10, "t": 87},
                "showactive": False,
                "type": "buttons",
                "x": 0.1,
                "xanchor": "right",
                "y": 0,
                "yanchor": "top"
            }]
        ),
        frames=frames
    )

    # Y축 범위 고정
    fig.update_yaxes(range=[0, 50])  # 원하는 범위로 수정

    # 그래프 레이아웃 설정
    fig.update_layout(title_text="Top 10 국가 간암 사망자 수 변화",
                    title_x = 0.5,
                    title_xanchor = 'center',
                    title_font_size = 25,
                    title_font_color = 'black',
                    title_font_family = 'NanumSquare',
                    plot_bgcolor='#ffffff',
                    xaxis=dict(title='Country'),
                    yaxis=dict(title='Count/(1000명)'),
                    showlegend=False)

    fig.update_traces(#marker_color= 히스토그램 색, 
                    #marker_line_width=히스토그램 테두리 두깨,                            
                    #marker_line_color=히스토그램 테두리 색,
                    marker_opacity = 0.4,
                    )

    # 🔹 슬라이더 추가
    fig.update_layout(
        sliders=[{
            "steps": [
                {
                    "args": [[str(year)], {"frame": {"duration": 0, "redraw": True}, "mode": "immediate"}],
                    "label": str(year),
                    "method": "animate"
                }
                for year in years
            ],
            "currentvalue": {"prefix": "연도: ", "font": {"size": 20}},
            "len": 0.9,
            "x": 0.1,
            "xanchor": "left",
            "y": -0.3,
            "yanchor": "top"
        }]
    )

    return fig

def bar_ani_perc(tl, years):

    # Bar Plot 생성
    fig = go.Figure()

    def get_colors_for_year(year, tl):
        colors = ['#e74c3c' if country == 'South Korea' else 'lightslategray' for country in tl[tl["Year"] == year]["Entity"]]
        return colors

    frames = [
        go.Frame(
            data=[go.Bar(x=tl[tl["Year"] == year]["Entity"], y=tl[tl["Year"] == year]["death_per_population"], marker_color=get_colors_for_year(year, tl))],
            name=str(year)
        )
        for year in years
    ]

    fig = go.Figure(
        data=[go.Bar(x=tl[tl["Year"] == years[0]]["Entity"], y=tl[tl["Year"] == years[0]]["death_per_population"], marker_color=get_colors_for_year(1990, tl))],
        layout=go.Layout(
            title="연도별 Entity 데이터 변화",
            xaxis=dict(title="Country"),
            yaxis=dict(title="사망자 비율(‰)"),
            updatemenus=[{
                "buttons": [
                    {
                        "args": [None, {"frame": {"duration": 650, "redraw": True}, 'fromcurrent':True}],
                        "label": "▶",
                        "method": "animate"
                    },
                    {
                        "args": [[None], {"frame": {"duration": 0, "redraw": False}, "mode": "immediate"}],
                        "label": "❚❚",
                        "method": "animate"
                    }
                ],
                "direction": "left",
                "pad": {"r": 10, "t": 87},
                "showactive": False,
                "type": "buttons",
                "x": 0.1,
                "xanchor": "right",
                "y": 0,
                "yanchor": "top"
            }]
        ),
        frames=frames
    )

    # Y축 범위 고정
    fig.update_yaxes(range=[0, 100])  # 원하는 범위로 수정

    # 그래프 레이아웃 설정
    fig.update_layout(title_text="Top 10 국가 간암 사망자 비율 변화",
                    title_x = 0.5,
                    title_xanchor = 'center',
                    title_font_size = 25,
                    title_font_color = 'black',
                    title_font_family = 'NanumSquare',
                    plot_bgcolor='#ffffff',
                    xaxis=dict(title='Country'),
                    yaxis=dict(title='사망자 비율(‰)'),
                    showlegend=False)

    fig.update_traces(#marker_color= 히스토그램 색, 
                    #marker_line_width=히스토그램 테두리 두깨,                            
                    #marker_line_color=히스토그램 테두리 색,
                    marker_opacity = 0.4,
                    )

    # 🔹 슬라이더 추가
    fig.update_layout(
        sliders=[{
            "steps": [
                {
                    "args": [[str(year)], {"frame": {"duration": 0, "redraw": True}, "mode": "immediate"}],
                    "label": str(year),
                    "method": "animate"
                }
                for year in years
            ],
            "currentvalue": {"prefix": "연도: ", "font": {"size": 20}},
            "len": 0.9,
            "x": 0.1,
            "xanchor": "left",
            "y": -0.3,
            "yanchor": "top"
        }]
    )

    return fig


# 암으로 사망한 사람들의 비율
def cancer_death_graph(dataframe):

    fig = go.Figure()

    for i in dataframe['암종'].unique():
        fig.add_trace(go.Scatter(x = dataframe[dataframe['암종'] == i]['년도'],
                            y = dataframe[dataframe['암종'] == i]['투병중 사망비율'],
                            marker_color='#e74c3c' if i == '간암' else 'lightslategray',
                            opacity=0.8,
                            name=f'{i}'))

    fig.update_layout(title_text="한국의 암 투병 환자 중 사망 비율",
                    title_x = 0.5,
                    title_xanchor = 'center',
                    title_font_size = 25,
                    title_font_color = 'black',
                    title_font_family = 'NanumSquare',
                    plot_bgcolor='#ffffff',
                    xaxis=dict(title='연도'),
                    yaxis=dict(title='사망비율(%)'))

    fig.update_traces(#marker_color= 히스토그램 색, 
                    #marker_line_width=히스토그램 테두리 두깨,                            
                    #marker_line_color=히스토그램 테두리 색,
                    marker_opacity = 0.4,
                    )
    
    return fig

def cirrhosis_demographic_plot(data, col):

    # 사용자 지정 색상 지정
    custom_colors = {
        "Mild": "#18bc9c", 
        "Moderate": "#F1C40F",  
        "Advanced": "#f39c12", 
        "Cirrhosis": "#e74c3c"  
    }

    if data[col].dtype == 'O':
        
        dt = pd.crosstab(data[col], data['Stage'])

        # Plotly 히트맵 생성
        fig = px.imshow(
            dt,
            text_auto=True,  # 셀 값 표시
            color_continuous_scale='Emrld'
        )

        fig.update_layout(title_text=f"{col}과(와) 간 질환 Stage의 교차 분석",
                            title_x = 0.5,
                            title_xanchor = 'center',
                            title_font_size = 22,
                            title_font_color = 'black',
                            title_font_family = 'NanumSquare',
                            xaxis_title='간 질환 단계',
                            yaxis_title=f'{col}',
                            coloraxis_showscale=False,
                            template='simple_white')

        return fig
    
    else:

        # 연속형일 경우 데이터의 히스토그램을 그리도록 지시
        fig = px.histogram(data_frame=data, x=col, color='Stage', color_discrete_map=custom_colors)
        fig.update_layout(title_text=f"{col}과(와) 간 질환 Stage의 히스토그램",
                        title_x = 0.5,
                        title_xanchor = 'center',
                        title_font_size = 22,
                        title_font_color = 'black',
                        title_font_family = 'NanumSquare',
                        barmode = 'overlay',
                        legend=dict(orientation="h", x=0.5, y=-0.2, xanchor="center", yanchor="top"),
                        showlegend=True,
                        # hovermode='x unified',
                        margin=dict(
                            b=100  # 아래쪽 마진 추가
                        ),
                        template='simple_white')
        fig.update_traces(#marker_color= 히스토그램 색, 
                        #marker_line_width=히스토그램 테두리 두깨,                            
                        #marker_line_color=히스토그램 테두리 색,
                        marker_opacity = 0.2,
                        )
        
        return fig
    

# 튜키 사후검정 그래프
def tukey_ci_plot(data, col):

    d = data[data['val'] == col].reset_index(drop = True)

    # 수직선 기준값 (예: 22)
    threshold = 0

    # 그래프 생성
    fig = go.Figure()

    # 신뢰구간 수평선 및 평균점 추가
    for i, group in enumerate(d['group']):
        # 신뢰구간이 수직선 기준값을 넘었는지 확인
        color = "green" if (d['upper'][i] >= threshold) and (d['lower'][i] <= threshold) else "red"
        
        # 신뢰구간 시작점과 끝점
        x_vals = [d['lower'][i], d['upper'][i], d['meandiff'][i]]
        y_vals = [i, i, i]  # Y축 값 (숫자로 변환)

        # 하나의 trace로 신뢰구간과 평균점 추가
        fig.add_trace(go.Scatter(
            x=x_vals,
            y=y_vals,
            mode="lines+markers",  # 선과 점을 함께 표시
            line=dict(color=color, width=3),  # 선의 색상 및 두께
            marker=dict(size=6, color=color, symbol="square"),  # 평균 점 스타일
            name=f"{group}"
        ))

    # 수직선 추가 (Overlay 방식)
    fig.add_shape(
        type="line",
        x0=threshold, x1=threshold,  # 수직선 X 위치 고정
        y0=0, y1=1,  # Y축 전체를 관통하도록 설정 (0~1, paper 단위)
        xref="x", yref="paper",  # X축 좌표는 실제 데이터 기준, Y축은 전체 그래프 기준
        line=dict(color="black", width=2, dash="dash")
    )

    # 레이아웃 설정
    fig.update_layout(
        title_text=f"{col}변수의 Tukey 사후 검정 신뢰구간 그래프",
        title_x = 0.5,
        title_xanchor = 'center',
        title_font_size = 22,
        title_font_color = 'black',
        title_font_family = 'NanumSquare',
        yaxis=dict(
            tickmode="array",
            tickvals=list(range(len(d['group']))),
            ticktext=d['group'],
            categoryorder="category ascending"
        ),  # 그룹 순서 유지
        xaxis=dict(showgrid=True),  # X축 격자 표시
        legend=dict(orientation="h", x=0.5, y=-0.4, xanchor="center", yanchor="top"),
        showlegend=True,
        # hovermode='x unified',
        margin=dict(
            b=100  # 아래쪽 마진 추가
        ),
        template='simple_white'
    )

    return fig