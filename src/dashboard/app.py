"""Streamlit dashboard."""
import streamlit as st
import pandas as pd
import sqlite3
from ..config import SQLITE_DB

st.set_page_config(page_title='Trading Bot Dashboard', layout='wide')

st.title('Trading Bot Dashboard')

# Portfolio summary
st.header('Portfolio')
conn = sqlite3.connect(SQLITE_DB)
try:
    positions = pd.read_sql('SELECT * FROM paper_positions', conn)
    st.dataframe(positions)
except:
    st.info('No positions yet.')

orders = pd.read_sql('SELECT * FROM paper_orders ORDER BY timestamp DESC LIMIT 20', conn)
st.dataframe(orders)
conn.close()

# Backtest results
st.header('Backtest Results')
st.info('Run backtests from CLI first.')
