import subprocess

# Dash 앱 실행
subprocess.Popen(["python", "app.py"])

# Streamlit 메인 페이지 (필요하면 수정 가능)
import streamlit as st
st.title("Dash App via Streamlit")
st.write("Your Dash app is running in the background.")

# Dash 앱 임베드 (iframe 사용)
st.components.v1.iframe("http://127.0.0.1:8050", width=1000, height=600)