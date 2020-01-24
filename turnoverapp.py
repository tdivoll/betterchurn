import streamlit as st
import pandas as pd
import numpy as np
import os, sys
import importlib.util
import matplotlib.pyplot as plt
import pickle

if len(sys.argv) > 1:
    folder = os.path.abspath(sys.argv[1])
else:
    folder = os.path.abspath(os.getcwd())
    
# Get filenames for all python files in this path, excluding this script
thisFile = os.path.abspath(__file__)
fileNames = []
for baseName in os.listdir(folder):
	fileName = os.path.join(folder, baseName)
	if (fileName.endswith(".py")) and (fileName != thisFile):
		fileNames.append(fileName)
  
# Filename formatter to display a nicer url (instead of the whole github path)
def format_url(s):
	els = s.split("/")[-1].split(".")[0].split("_")
	return " ".join(el for el in els).capitalize()

@st.cache
def load_model(modelName):
  model=pd.read_pickle(os.path.join(folder, 'models', modelName + '.sav'))
  return model

modelName = 'randomfor_week2'
model = load_model(modelName)
#
st.title('Low-flow Nursing')
st.header("Predicting RN turnover rates with staffing metrics, patient reviews, and employee sentiments")


#load pickled model
#file = open('/home/tjd/InsightFiles/turnover-app/betterchurn/randomfor_week2.sav', 'rb')
#pred_data = pd.read_pickle(file, compression=None)


data2 = pd.read_csv('/home/tjd/InsightFiles/turnover-app/betterchurn/TurnoverRates.csv')
columns = data2[['RN Turnover Rate in the Medical-Surgical Unit','RN Turnover Rate in the Critical Care Unit', 'RN Turnover Rate in the NICU', 'RN Turnover Rate in the Mother/Baby Unit']]


column = st.multiselect('Choose your unit(s) of interest', data2.columns)

fig, ax=plt.subplots(figsize=(14,3))
ax.set_xlim([0,100])
st.bar_chart(data2[column], width = 7)


st.dataframe(pd.read_csv('/home/tjd/InsightFiles/turnover-app/betterchurn/RelevantSurvey.csv'))
