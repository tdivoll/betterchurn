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

#@st.cache
def load_model(modelName):
  model=pd.read_pickle(os.path.join(folder, 'models', modelName + '.sav'))
  return model

modelName = 'rf_week4'
model = load_model(modelName)


#load data
data = pd.read_csv('ModelDF.csv')

data = data.drop(columns = ['Unnamed: 0','Hosp_Name', 'label'], axis=1)
#data.iloc[[4]]
vals = data.iloc[[4]]
vals = np.array(vals).reshape(1, -1)[0]
#vals

##extract sample row for the web app

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

st.markdown(""" ### Enter your staffing metrics in the boxes below to predict RN turnover. Play around with different combinations to get an idea of what changes may lead to lower than average turnover!""")



#model_in= data.drop(['label'], axis=1)

st.markdown("""<br>""", unsafe_allow_html=True)
st.markdown("""## **Nurse to patient ratio for Critical Care Unit (0-100):**""")
RN_patient_critcare = st.number_input('Enter CC ratio:',min_value=0, max_value=100, value=14)

st.markdown("""<br>""", unsafe_allow_html=True)
st.markdown("""## **Nurse to patient ratio for Medical-Surgical Units (0-100):**""")
RN_patient_medsurg = st.number_input('Enter MS ratio',min_value=0, max_value=100, value=10)

st.markdown("""<br>""", unsafe_allow_html=True)
st.markdown("""## **Percent non-contract RN in Critical Care Units (0-100):**""")
PerRNconCC = st.number_input('Enter %/ hospital-employed in CC:', min_value=0, max_value=100, value=80)

st.markdown("""<br>""", unsafe_allow_html=True)
st.markdown("""## **Percent non-contract RN in Medical-Surgical Units (0-100):**""")
PerRNconMS = st.number_input('Enter %/ hospital-employed in MS:', min_value=0, max_value=100, value=75)

st.markdown("""<br>""", unsafe_allow_html=True)
st.markdown("""## **Percent Critical Care RN relative to LPN and CNA (0-100):**""")
PerRNCC = st.number_input('Enter %/ RN in CC:',min_value=0, max_value=100, value=50)

st.markdown("""<br>""", unsafe_allow_html=True)
st.markdown("""## **Percent Medical-Surgical RN relative to LPN and CNA (0-100):**""")
PerRNMS = st.number_input('Enter %/ RN in MS:',min_value=0, max_value=100, value=50)

vals = [vals[0], vals[1], vals[2], vals[3], vals[4], vals[5], vals[6], vals[7], vals[8], vals[9], vals[10], vals[11], vals[12], PerRNCC, PerRNconCC, PerRNconMS, vals[16], PerRNMS, RN_patient_critcare, RN_patient_medsurg, vals[20], vals[21], vals[22], vals[23], vals[24], vals[25], vals[26], vals[27], vals[28], vals[29], vals[30], vals[31], vals[32], vals[33], vals[34], vals[35], vals[36], vals[37], vals[38], vals[39], vals[40], vals[41], vals[42], vals[43], vals[44], vals[45], vals[46], vals[47], vals[48], vals[49], vals[50], vals[51], vals[52], vals[53], vals[54], vals[55], vals[56], vals[57], vals[58], vals[59], vals[60], vals[61], vals[62], vals[63], vals[64], vals[65], vals[66], vals[67], vals[68], vals[69], vals[70], vals[71], vals[72], vals[73], vals[74], vals[75], vals[76], vals[77], vals[78], vals[79], vals[80], vals[81], vals[82], vals[83], vals[84], vals[85], vals[86], vals[87], vals[88], vals[89], vals[90], vals[91], vals[92], vals[93], vals[94], vals[95], vals[96], vals[97], vals[98], vals[99], vals[100], vals[101], vals[102], vals[103], vals[104], vals[105]]
#turn = data[(data['RN Turnover'].isin(user_select))]
##Prediction
if st.button('Predict turnover'):
    #prediction = model.predict(np.array(model_in).loc[user_select].values.reshape(1, -1))[0]
    
    prediction=model.predict(np.array(vals).reshape(1, -1))[0]
    #st.success(f'Turnover at your hospital is:' )
    if prediction<1:
        st.markdown("""## Turnover at your hospital is ___**lower**___ than average.""")
        st.markdown("""## Consider comparing your employee ratings to the distributions of ratings for all hospitals below. With such insights, you may find employee sentement areas to focus on.""")
    else:
        st.markdown("""## Turnover at your hospital is ___**higher**___ than average.""")
        st. markdown("""## Consider comparing your employee ratings to the distributions of ratings for all hospitals below. With such insights, you may find  employee sentement areas to focus on.""")
st.markdown("""<br>""", unsafe_allow_html=True)   
st.markdown("""<br>""", unsafe_allow_html=True)
st.markdown(
"""
# Employee sentiment areas
### Choose your hospital from the dropdown to see where your ratings compare to the rest of the hospitals that submit data to the Illinois Hospital Report Cards. The boundary of yellow coloring indactes your mean employee rating.
""")

ratings = pd.read_csv('ReviewData.csv')



#if rowLoc:

#fig=go.Figure()
#fig
#fig.add_histogram(x=hist_data)

#py.iplot(fig, filename = 'Overall Rating by Employees')
    #fig2, ax = plt.subplots()
    #fig2 = px.histogram(ratings, x='rating_overall')
    #h = rowLoc
    #ax.axvline(h, color='black', linewidth=2)
    #st.plotly_chart(fig2)
user_select = st.selectbox('Choose your hospital:', ratings['Hosp_Name'].unique())
filt = ratings["Hosp_Name"]==user_select
#print(user_select)
#print(filt)
selected = ratings.loc[filt,'rating_overall'].mean()
print (selected)

if selected <3.5:
    st.markdown(''' ## Your average rating is ___**lower**___ than average''')
else:
    st.markdown(''' ## Your average rating is ___**higher**___ than average''')


#hist_data = [ratings['rating_overall']]
#group_labels = ['Rating Score']
#fig = ff.create_distplot(hist_data, group_labels, show_hist=False, show_curve=True, bin_size=.5)
#fig.layout.update(width=800, bargap=0.01, xaxis_range= [0.5,5.5])
#fig
fig, ax = plt.subplots()
colors=['blue','blue','red', 'red', 'red']
bins=5
#fig2 = ax.hist(x=ratings['rating_overall'])
h = selected
N, bins, patches = ax.hist(x=ratings['rating_overall'], edgecolor='white', bins=bins, linewidth=1)


for i in range(0, int(h)):
    patches[i].set_facecolor('y')    
for i in range(int(h),int(h)):
    patches[i].set_facecolor('black')
for i in range(int(h), 5):
    patches[i].set_facecolor('black')
#ax.axvline(h, color='red', linewidth=3)
#st.plotly_chart(fig2)
st.pyplot(fig)
#ax.axvline(x=selected)
#rowLoc = ratings[ratings['Hosp_Name']==user_select].index.values.astype(int)[0]
#ratings["Hospital Selected"] = 'No'
#ratings["Hospital Selected"][rowLoc] = 'Yes'
#if ratings["Hospital Selected"] == 'Yes':
#ratings["Hospital"] = ratings['Hospital Selected']

#ratings['rating_overall'] = ratings['rating_overall'].round()
#ratings = ratings.sort_values(by ='rating_overall', ascending=True)

#plot_opts = dict(show_legend=False, color_index='Hospital Selected', title="Overall Glassdoor Ratings", width=600, xlabel='Hospital', 
#ylabel='Count in Class', ylim=(0, 8), xrotation=0)

#style_opts = dict(box_color=hv.Cycle(['#30b2da', '#fd4f70']))


#hist = hv.Histogram(ratings['rating_overall'])

#bars = hv.Bars(ratings, hv.Dimension('Hospital'), ['rating_overall','Hospital Selected'])
#bars = bars.opts(plot=plot_opts, style=style_opts)
#hist * bars).opts(plot=plot_opts, style=style_opts)

#st.write(hv.render(bars))


#st.write('"Your hospital:" user_select')



#ax.hist(ratings['rating_overall'], color='blue', alpha=0.5, histtype='stepfilled')
#h = ratings['Hosp_Name'].iloc[0]


#overall_rating = st.sidebar.slider('Overall rating', 0.0, 5.0, 3.4)
#career_rating = st.sidebar.slider('Career advancement rating', 0.0, 5.0, 3.1)
#salary_rating = st.sidebar.slider('Salary and benefits rating', 0.0, 5.0, 3.8)
#mgmt_rating = st.sidebar.slider('Management rating', 0.0, 5.0, 3.2)
#balance_rating = st.sidebar.slider('Work/life balance rating', 0.0, 5.0, 2.4)
#culture_rating = st.sidebar.slider('Workplace culture rating', 0.0, 5.0, 2.1)



#fig, ax=plt.subplots(figsize=(14,3))
#ax.set_xlim([0,100])
#st.bar_chart(data2[column], width = 7)


#st.dataframe(pd.read_csv('RelevantSurvey.csv'))
st.markdown(
"""
Created by Timothy Divoll, Data Science Fellow at Insight in Boston, MA.
"""
)