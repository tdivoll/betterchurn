import streamlit as st
import pandas as pd
import numpy as np
import os, sys
import importlib.util
import matplotlib.pyplot as plt
import pickle
import holoviews as hv
import hvplot
import hvplot.pandas # noqa: F401
from holoviews import opts
hv.extension('bokeh', logo=False)
import bokeh.models as bmo
from bokeh.plotting import figure, show
from bokeh.palettes import PuBu, Spectral5, Spectral6
from bokeh.io import show, output_notebook
from bokeh.models import ColumnDataSource, HoverTool, LabelSet, CategoricalColorMapper
from bokeh.transform import factor_cmap, factor_mark
import altair as alt

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

def load_model(modelName):
  model=pd.read_pickle(os.path.join(folder, 'models', modelName + '.sav'))
  return model

modelName = 'rf_week4'
model = load_model(modelName)

ratings = pd.read_csv('ReviewData.csv')
print(ratings.head())

st.markdown("""<br>""", unsafe_allow_html=True)

st.markdown("""
<style>
body {
    color: #2f4f4f;
    background-color: #b1cdcf;
}
</style>
    """, unsafe_allow_html=True)


st.title('BetterChuRN')
st.header("Predicting RN turnover rates with staffing metrics, patient reviews, employee sentiments, and demographics")
st.markdown('<style>h1{color: teal;}</style>', unsafe_allow_html=True)
st.markdown(
"""
### Compare your employee ratings to the distribution of ratings for each sentement area. Colored density plots indicate the density of all scores in each category and red markers indicate your hospital's score. 
""")

user_select = st.selectbox('Choose your hospital:', ratings['Hosp_Name'].unique())
filt = ratings["Hosp_Name"]==user_select
selected = ratings.loc[filt,'rating_overall'].mean()
selected = pd.to_numeric(selected)
ratings['Overall Rating Score'] = selected
print (selected)

###Give an indication of where the selected hospital stacks up against the others
if selected <3.4187:
    st.markdown(''' ## Your overall rating is ___**lower**___ than average''')
else:
    st.markdown(''' ## Your overall rating is ___**higher**___ than average''')

###Make a figure for the Overall Rating as a baseline
base = alt.Chart(
    ratings, 
    width=185, 
    height=60, 
    title="Overall Rating"
).transform_filter(
    'isValid(datum.rating_overall)'
).transform_density(
    'rating_overall',
    as_=['rating_overall', 'density'],
    extent=[0.5, 5.5],
).mark_area(color='#7ad2f6').encode(    
    x=alt.X('rating_overall:Q', axis=alt.Axis(title='5-star Rating')),
    y='density:Q',
)
rule=alt.Chart(ratings).mark_rule(color='red').encode(
    x='Overall Rating Score',size=alt.value(3)
)
overall = (base + rule)

###Make a figure for Work/Life balance
balfilt = ratings["Hosp_Name"]==user_select
balance = ratings.loc[balfilt,'rating_balance'].mean()
balance = pd.to_numeric(balance)
ratings['Work-life Balance Score'] = balance

base2 = alt.Chart(
    ratings, 
    width=185, 
    height=60, 
    title="Work-life Balance Rating"
).transform_filter(
    'isValid(datum.rating_balance)'
).transform_density(
    'rating_balance',
    as_=['rating_balance', 'density'],
    extent=[0.5, 5.5],
).mark_area(color="#014d64").encode(    
    x=alt.X('rating_balance:Q', axis=alt.Axis(title='5-star Rating')),
    y='density:Q',
)

rule2=alt.Chart(ratings).mark_rule(color='red').encode(
   x='Work-life Balance Score',size=alt.value(3)
)
balancefig = (base2 + rule2)

###Make a figure for Salary/Compensation
salfilt = ratings["Hosp_Name"]==user_select
salary = ratings.loc[balfilt,'rating_comp'].mean()
salary = pd.to_numeric(salary)
ratings['Salary Score'] = salary

base3 = alt.Chart(
    ratings, 
    width=185, 
    height=60, 
    title="          Salary/Benefits Rating      "
).transform_filter(
    'isValid(datum.rating_comp)'
).transform_density(
    'rating_comp',
    as_=['rating_comp', 'density'],
    extent=[0.5, 5.5],
).mark_area(color="#00887d").encode(    
    x=alt.X('rating_comp:Q', axis=alt.Axis(title='5-star Rating')),
    y='density:Q',
)

rule3 = alt.Chart(ratings).mark_rule(color='red').encode(
   x='Salary Score',size=alt.value(3)
)
salfig = (base3 + rule3)

###Make a figure for Management Style
mgmtfilt = ratings["Hosp_Name"]==user_select
management = ratings.loc[mgmtfilt,'rating_comp'].mean()
management = pd.to_numeric(management)
ratings['Management Score'] = management

base4 = alt.Chart(
    ratings, 
    width=185, 
    height=60, 
    title="Management Rating"
).transform_filter(
    'isValid(datum.rating_mgmt)'
).transform_density(
    'rating_mgmt',
    as_=['rating_mgmt', 'density'],
    extent=[0.5, 5.5],
).mark_area(color="#76c0c1").encode(    
    x=alt.X('rating_mgmt:Q', axis=alt.Axis(title='5-star Rating')),
    y='density:Q',
)

rule4 = alt.Chart(ratings).mark_rule(color='red').encode(
   x='Management Score',size=alt.value(3)
)
mgmtfig = (base4 + rule4)

###Make figure for Workplace culture
culturefilt = ratings["Hosp_Name"]==user_select
culture = ratings.loc[culturefilt,'rating_culture'].mean()
culture = pd.to_numeric(culture)
ratings['Workplace Culture Score'] = culture

base5 = alt.Chart(
    ratings, 
    width=185, 
    height=60, 
    title="Workplace Culture Rating"
).transform_filter(
    'isValid(datum.rating_culture)'
).transform_density(
    'rating_culture',
    as_=['rating_culture', 'density'],
    extent=[0.5, 5.5],
).mark_area(color='#6794a7').encode(    
    x=alt.X('rating_culture:Q', axis=alt.Axis(title='5-star Rating')),
    y='density:Q',
)

rule5 = alt.Chart(ratings).mark_rule(color='red').encode(
   x='Workplace Culture Score',size=alt.value(3)
)
culturefig = (base5 + rule5)

###Make figure for Career Advancement
careerfilt = ratings["Hosp_Name"]==user_select
career = ratings.loc[careerfilt,'rating_career'].mean()
career = pd.to_numeric(career)
ratings['Career Advancement Score'] = career

base6 = alt.Chart(
    ratings, 
    width=185, 
    height=60, 
    title="Career Advancement Rating    "
).transform_filter(
    'isValid(datum.rating_career)'
).transform_density(
    'rating_career',
    as_=['rating_career', 'density'],
    extent=[0.5, 5.5],
).mark_area(color='#01a2d9').encode(    
    x=alt.X('rating_career:Q', axis=alt.Axis(title='5-star Rating')),
    y='density:Q',
)

rule6 = alt.Chart(ratings).mark_rule(color='red').encode(
   x='Career Advancement Score',size=alt.value(3)
)
careerfig = (base6 + rule6)

###Print all the figures using pipe command to place side-by-side
st.write(overall | balancefig | salfig)
st.write(mgmtfig | culturefig | careerfig)

##################################################################################
##Modeling Section

#load dataframe
data = pd.read_csv('ModelDF.csv')

data = data.drop(columns = ['Unnamed: 0','Hosp_Name', 'label'], axis=1)

vals = data.iloc[[4]]
vals = np.array(vals).reshape(1, -1)[0]
#vals
##extract sample row for the web app

st.markdown("""  _________________________________________________________________ """)
st.markdown(""" # Churn Prediction from Nurse Staffing Metrics""")
st.markdown(""" ### Enter your staffing metrics in the boxes below to predict RN turnover. Play around with different combinations to get an idea of what changes may lead to lower than average turnover!
""")

#model_in= data.drop(['label'], axis=1)

st.markdown("""## **Nurse to patient ratio for Critical Care Unit (0-100):**""")
RN_patient_critcare = st.number_input('Enter nurse/patient ratio in Critical Care:',min_value=0, max_value=100, value=14)

st.markdown("""<br>""", unsafe_allow_html=True)
st.markdown("""## **Nurse to patient ratio for Medical-Surgical Units (0-100):**""")
RN_patient_medsurg = st.number_input('Enter nurse/patient ratio in Medical-Surgical:',min_value=0, max_value=100, value=10)

st.markdown("""<br>""", unsafe_allow_html=True)
st.markdown("""## **Percent non-contract RN in Critical Care Units (0-100):**""")
PerRNconCC = st.number_input('Enter' '%' 'hospital-employed RN in Critical Care:', min_value=0, max_value=100, value=80)

st.markdown("""<br>""", unsafe_allow_html=True)
st.markdown("""## **Percent non-contract RN in Medical-Surgical Units (0-100):**""")
PerRNconMS = st.number_input('Enter' '%' 'hospital-employed RN in Medical-Surgical:', min_value=0, max_value=100, value=75)

st.markdown("""<br>""", unsafe_allow_html=True)
st.markdown("""## **Percent Critical Care RN relative to LPN and CNA (0-100):**""")
PerRNCC = st.number_input('Enter' '%' 'RN in Critical Care:',min_value=0, max_value=100, value=50)

st.markdown("""<br>""", unsafe_allow_html=True)
st.markdown("""## **Percent Medical-Surgical RN relative to LPN and CNA (0-100):**""")
PerRNMS = st.number_input('Enter' '%' 'RN in Medical-Surgical:',min_value=0, max_value=100, value=50)

vals = [vals[0], vals[1], vals[2], vals[3], vals[4], vals[5], vals[6], vals[7], vals[8], vals[9], vals[10], vals[11], vals[12], PerRNCC, PerRNconCC, PerRNconMS, vals[16], PerRNMS, RN_patient_critcare, RN_patient_medsurg, vals[20], vals[21], vals[22], vals[23], vals[24], vals[25], vals[26], vals[27], vals[28], vals[29], vals[30], vals[31], vals[32], vals[33], vals[34], vals[35], vals[36], vals[37], vals[38], vals[39], vals[40], vals[41], vals[42], vals[43], vals[44], vals[45], vals[46], vals[47], vals[48], vals[49], vals[50], vals[51], vals[52], vals[53], vals[54], vals[55], vals[56], vals[57], vals[58], vals[59], vals[60], vals[61], vals[62], vals[63], vals[64], vals[65], vals[66], vals[67], vals[68], vals[69], vals[70], vals[71], vals[72], vals[73], vals[74], vals[75], vals[76], vals[77], vals[78], vals[79], vals[80], vals[81], vals[82], vals[83], vals[84], vals[85], vals[86], vals[87], vals[88], vals[89], vals[90], vals[91], vals[92], vals[93], vals[94], vals[95], vals[96], vals[97], vals[98], vals[99], vals[100], vals[101], vals[102], vals[103], vals[104], vals[105]]

##Prediction functionality
if st.button('Predict turnover'):
    
    prediction=model.predict(np.array(vals).reshape(1, -1))[0]
    
    if prediction<1:
        st.markdown("""## Turnover at your hospital is ___**lower**___ than average.""")
        st.markdown("""## Consider comparing your employee ratings to the distributions of ratings for all hospitals above. With such insights, you may find employee sentement areas to focus on.""")
    else:
        st.markdown("""## Turnover at your hospital is ___**higher**___ than average.""")
        st. markdown("""## Consider comparing your employee ratings to the distributions of ratings for all hospitals above. With such insights, you may find  employee sentement areas to focus on.""")
st.markdown("""<br>""", unsafe_allow_html=True)


st.markdown(
"""
Created by Timothy Divoll, Data Science Fellow at Insight in Boston, MA.
"""
)
