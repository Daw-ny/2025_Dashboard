#######################################################
# plotly
from plotly.subplots import make_subplots
import plotly.express as px
import plotly.graph_objects as go

# model
import warnings
warnings.filterwarnings('ignore')

#######################################################
# 두 변수의 상관관계를 그린 그래프
def plot_pairs(dataframe, corrdata, first_var, second_var):

        # 특정 위치 상관계수 구하기
    correlation_value = corrdata[first_var][corrdata['Unnamed: 0'] == second_var]

    # 두 변수간의 관계를 확인하기 위해 
    subfig = make_subplots(specs=[[{"secondary_y": True}]])
    
    fig1 = px.line(dataframe[first_var])
    fig2 = px.line(dataframe[second_var])
    fig2.update_traces(yaxis="y2")

    subfig.layout.yaxis.title="index"
    subfig.layout.yaxis.title= first_var
    subfig.layout.yaxis2.title= second_var
    subfig.layout.title = f"Correlation : {float(correlation_value):.4f}" 
    subfig.add_traces(fig1.data + fig2.data)
        # 첫 번째 trace와 두 번째 trace의 색상 변경
    subfig.data[0].update(line=dict(color='#18bc9c'))  # 첫 번째 변수 색상: 연두
    subfig.data[1].update(line=dict(color='#95a5a6'))  # 두 번째 변수 색상: 남색
    subfig.update_layout(
        template='simple_white',
        legend=dict(orientation="h"),
        showlegend=True,
        hovermode='x unified'
    )

    return subfig


# top 5 변수 비교 그래프 그리기
def effective_value_top_5(df_normal, df_anomaly, col_chooser):
    # top 5 그래프 그리기
    ffig = go.Figure()

    ffig.add_trace(go.Scatter(x = df_normal['sample'],
                            y=df_normal[col_chooser],
                            name=col_chooser + ' normal',
                            marker = {'color':'#18bc9c'}))

    ffig.add_trace(go.Scatter(x = df_anomaly['sample'],
                            y=df_anomaly[col_chooser],
                            name=col_chooser + ' anomaly',
                            marker = {'color':'#e74c3c'}))
    
    ffig.add_vline(x=160,line_width=3, line_dash="dash",
              line_color="#2c3e50",
              annotation_text="변화 시작점", 
              annotation_position="top left",
              annotation_font_size=15,
              annotation_font_color="#2c3e50",
              annotation_font_family="NanumSquare")

    # Edit the layout
    ffig.update_layout(title=f'k-means로 추론한 test set의 {col_chooser}평균값의 차이',
                    xaxis_title='sampleNum',
                    yaxis_title=f'means of {col_chooser}',
                    legend=dict(orientation="h"),
                    showlegend=True,
                    hovermode='x unified',
                    template='simple_white'
                    )

    return ffig