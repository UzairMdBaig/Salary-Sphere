import streamlit as st
from prediction import show_predict_page
from exploration import show_exploration_page

choice = st.sidebar.selectbox("explore or predict",("explore","predict"))
if choice == "predict":
    show_predict_page()
else:
    show_exploration_page()
    