import subprocess

# Dash 앱 실행
subprocess.Popen(["python", "app.py"])

# Streamlit 메인 페이지 (필요하면 수정 가능)
import streamlit as st
st.title("Dash App via Streamlit")
st.write("Your Dash app is running in the background.")
