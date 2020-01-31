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

modelName = 'lm_week3'
model = load_model(modelName)

#load data
data = pd.read_csv('ModelData.csv')


##extract sample row for the web app



st.title('BetterChuRN')
st.header("Predicting RN turnover rates with staffing metrics, patient reviews, and employee sentiments")

model_input = data.iloc[15]

user_select = st.selectbox('Choose your hospital', data['Hosp_Name'].unique())
st.write('Your selection:' , user_select)
##Prediction
if st.button('Predict turnover'):

    #prediction = model.predict(np.array(data['RN Turnover']).reshape(1, -1))[0] 
    st.success(f'Turnover at this hospital is 14 +/- 11 %') 
 

"""
## Employee sentiments
#### Manipulate slider bars to see the effect on turnover rate
"""
#overall_rating = st.slider('Overall rating', 0.0, 5.0, 3.4)
career_rating = st.slider('Career advancement rating', 0.0, 5.0, 3.1)
salary_rating = st.slider('Salary and benefits rating', 0.0, 5.0, 3.8)
mgmt_rating = st.slider('Management rating', 0.0, 5.0, 3.2)
balance_rating = st.slider('Work/life balance rating', 0.0, 5.0, 2.4)
culture_rating = st.slider('Workplace culture rating', 0.0, 5.0, 2.1)

#data[data.Hosp_Name == model_input]

#data2 = pd.read_csv('TurnoverRates.csv')
#columns = data2[['RN Turnover Rate in the Medical-Surgical Unit','RN Turnover Rate in the Critical Care Unit', 'RN #Turnover Rate in the NICU', 'RN Turnover Rate in the Mother/Baby Unit']]

#fig, ax=plt.subplots(figsize=(14,3))
#ax.set_xlim([0,100])
#st.bar_chart(data2[column], width = 7)


#st.dataframe(pd.read_csv('RelevantSurvey.csv'))
