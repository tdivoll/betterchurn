# betterchuRN

### Insight Data Science Fellow Project - Boston 2020A

This project uses a machine learning approach to predict turnover of registered nurses (RN) at 184 Illinois hospitals. The national average of nurse churn is 17% per year, and it costs an estimated $40-85k and 3 months time to replace a nurse. The general factors related to turnover in hospitals are salary, management style, workplace culture, and patient loads, but the interactions of these factors makes it hard for hospitals to assess the importance of each in this highly complex problem. Combining data sources on hospital and staffing metrics, patient survey responses, and employee sentiments, users can get predicted turnover rates and see how changes in staffing metrics and employee sentiments may change estimated turnover. With such insights, hospital administrators can learn about the importance of each focal area when turnover is an issue. The project is deployed as a streamlit [website application](https://betterchurn.herokuapp.com/) via heroku.

## 1. Datasets

*~20,000 rows of data on hospital and staffing metrics and patient review responses from the 2017--2018 Medicare Hospital Consumer Assessment of Healthcare Providers and Systems (HCAHPS) survey downloaded and collated from Illinois Hospital Report Cards

*~5,800 hospital employee review ratings scraped from Glassdoor; a small number of ratings were filled in from Indeed for       smaller hospitals without Glassdoor reviews

*County-level opioid OD data from the Illinois Opioid Data Dashboard, Illinois Department of Public Health

*County-level homicide data from the Illinois State Police website

## 2. Hospital metrics and patient response processing

Data from the Illinois Hospital Reports Cards were downloaded as .csv files and combined into one pandas dataframe with glob in python. The dataframe was pivoted so that metrics for each hospital were representd by unique rows. Features were then selected based on the potential to influence working conditions for RNs and data were cleaned to numeric values. To account for differences in reported turnover rates across hospitals, the maximum rate among Critical Care, Medical-Surgical, Maternity, and Neonatal medical units was selected for each hospital. Features were also engineered to account for hospitals under umbrella organizations and the number of hospitals per county. 

## 3. Employee review rating processing

Reviews were scraped from Glassdoor as .csv files and combined into one pandas dataframe with glob. Employees encoded their workplace sentements into the following 5-start rating categories: overall, workplace culture, salary and benfits, management style, career advancement, and work-life balance. Significant data cleaning was necessary to account for hospital name changes with recent umbrella organization acquisitions. For several smaller hospitals without reviews on glassdoor, missing data were filled in with ratings from Indeed.

## 4. Random forest classification

Random forest classification was used to predict turnover as a binary class either less than or greater than the Illinois state-wide average churn rate of RNs (19%). Modeling was performed with scikit-learn in python using an 80:20 split for training and testing sets. Feature importance was assessed using drop-column cross-validation on model variance, resulting in 5 of the top 6 features related to RN patient loads, the percentage of RNs relative to LPN and CNA, and the percentage of hospital-employed relative to contract RN in the Critical Care and Medical-Surgical Units. The cost of false-negatives (predicting a hospital has low turnover when in fact it is high), could potentially cost aeach hospital hundreds of thousands of dollars, thus recall was used as the metric to assess model performance. At 0.8, the model performed reasonably well. Hospitals can get a sense of which employee sentements may lead to turnover at the their hospital and play around with different staffing ratios to see what may contribute to lower than average turnover on the [web app](https://betterchurn.herokuapp.com/).

## 5. Acknowledgments

Glassdoor scraper was forked from [sericson0](https://github.com/sericson0).
Many Insight Fellows, Program Directors, Alumni, and Staff helped this project along.
