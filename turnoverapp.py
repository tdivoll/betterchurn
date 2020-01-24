import streamlit as st
import pandas as pd
import numpy as np
from sklearn.externals import joblib
import matplotlib.pyplot as plt




st.title('Low-flow Nursing')
st.header("Predicting RN turnover rates with staffing metrics, patient reviews, and employee sentiments")


#load pickled model
file = open('/home/tjd/InsightFiles/turnover-app/betterchurn/randomfor_week2.sav', 'rb')
pred_data = pd.read_pickle(file, compression=None)


data2 = pd.read_csv('/home/tjd/InsightFiles/turnover-app/betterchurn/TurnoverRates.csv')
columns = data2[['RN Turnover Rate in the Medical-Surgical Unit','RN Turnover Rate in the Critical Care Unit', 'RN Turnover Rate in the NICU', 'RN Turnover Rate in the Mother/Baby Unit']]


column = st.multiselect('Choose your unit(s) of interest', data2.columns)

fig, ax=plt.subplots(figsize=(14,3))
ax.set_xlim([0,100])
st.bar_chart(data2[column], width = 7)


st.dataframe(pd.read_csv('/home/tjd/InsightFiles/turnover-app/betterchurn/RelevantSurvey.csv'))
