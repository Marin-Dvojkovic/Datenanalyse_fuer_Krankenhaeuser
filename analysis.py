import pandas as pd
import matplotlib.pyplot as plt

pd.set_option('display.max_columns', 8)
plt.close()

# read the csv files and save them into variables
general = pd.read_csv('data/general.csv', encoding='utf-8')
prenatal = pd.read_csv('data/prenatal.csv', encoding='utf-8')
sports = pd.read_csv('data/sports.csv', encoding='utf-8')

# print the first 20 rows of them in the order : general, prenatal, sports
# print(general.head(20))
# print(prenatal.head(20))
# print(sports.head(20))

# prepare column names for later merge
prenatal.rename(columns={'HOSPITAL': 'hospital', 'Sex': 'gender'}, inplace=True)
sports.rename(columns={'Male/female': 'gender', 'Hospital': 'hospital'}, inplace=True)

# merge dataframes into one
all_hospitals = pd.concat([general, prenatal, sports], ignore_index=True)

# delete Unnamed: 0 column
all_hospitals.drop(columns={'Unnamed: 0'}, inplace=True)

# delete all empty rows
# detect which rows only contain NaN's and drop them
all_hospitals.dropna(axis=0, how='all', inplace=True)

# further data preparation
# the data contains man, woman, male and female
# the merged data should only contain m or f
all_hospitals['gender'].replace('male', 'm', inplace=True)
all_hospitals['gender'].replace('man', 'm', inplace=True)
all_hospitals['gender'].replace('female', 'f', inplace=True)
all_hospitals['gender'].replace('woman', 'f', inplace=True)

# prental has only female patients so set gender of prenatal patients to f
all_hospitals.loc[all_hospitals.hospital == 'prenatal', 'gender'] = 'f'

# replace NaN values with 0
fillna_columns = ['bmi', 'diagnosis', 'blood_test', 'ecg', 'ultrasound', 'mri', 'xray', 'children', 'months']
for i in fillna_columns:
    all_hospitals[i].fillna(0, inplace=True)

# print the shape of the dataframe
# print(all_hospitals.shape)

# print the merged dataframe
# print(all_hospitals.sample(n=20,random_state=30))

# answer 5 questions about the data
# 1. Which hospital has the highest number of patients?
x = all_hospitals.hospital.value_counts().idxmax()
# print('The answer to the 1st question is ' + x)

# 2. What share of the patients in the general hospital suffers from stomach-related issues? Round the result to the third decimal place.
all_general = all_hospitals.loc[all_hospitals.hospital == 'general']
all_diags = all_general['diagnosis'].shape[0]
all_stom = all_general['diagnosis'].loc[all_hospitals.diagnosis == 'stomach'].shape[0]
share = round((all_stom / all_diags), 3)
# print('The answer to the 2nd question is ' + str(share))

# 3. What share of the patients in the sports hospital suffers from dislocation-related issues? Round the result to the third decimal place.
all_sports = all_hospitals.loc[all_hospitals.hospital == 'sports']
all_sports_disloc = all_sports.loc[all_sports.diagnosis == 'dislocation']
share1 = round((all_sports_disloc.shape[0] / all_sports.shape[0]), 3)
# print('The answer to the 3rd question is ' + str(share1))

# 4. What is the difference in the median ages of the patients in the general and sports hospitals?
median_ages = all_hospitals[['hospital', 'age']].groupby('hospital').agg('median')
dif = abs(median_ages.loc['general'] - median_ages.loc['sports'])
dif = dif.iloc[0]
# print('The answer to the 4th question is ' + str(dif))

# 5. After data processing at the previous stages, the blood_test column has three values: t= a blood test was taken, f= a blood test wasn't taken, and 0= there is no information.
# In which hospital the blood test was taken the most often (there is the biggest number of t in the blood_test column among all the hospitals)? How many blood tests were taken?
bt_hospital = all_hospitals[['hospital', 'blood_test']].loc[all_hospitals.blood_test == 't'].groupby('hospital').agg(
    'count').idxmax().iloc[0]
bt_count = all_hospitals[['hospital', 'blood_test']].loc[all_hospitals.blood_test == 't'].groupby('hospital').agg(
    'count').max().iloc[0]
# print(f'The answer to the 5th question is {bt_hospital}, {bt_count} blood tests')


# answer 3 more questions about the data
# 1. What is the most common age of a patient among all hospitals? Plot a histogram and choose one of the following age ranges: 0-15, 15-35, 35-55, 55-70, or 70-80
plt.figure()
plt.hist(all_hospitals['age'], edgecolor='white', bins=[0, 15, 35, 55, 70, 80], )
plt.title('age distribution of patients')
plt.xlabel('age')
plt.ylabel('number of patients')
plt.show()
print('The answer to the 1st question: 15-35')

# 2. What is the most common diagnosis among patients in all hospitals? Create a pie chart
plt.figure()
all_hospitals.diagnosis.value_counts().plot(kind='pie', autopct='%1.0f%%')
plt.title('distribution of diagnoses')
plt.show()
print('The answer to the 2nd question: pregnancy')

# 3. Build a violin plot of height distribution by hospitals. Try to answer the questions.
# What is the main reason for the gap in values?
# Why there are two peaks, which correspond to the relatively small and big values?
plt.figure()
plt.violinplot(all_hospitals['height'])
plt.title('height distribution')
plt.show()
print(
    "The answer to the 3rd question: It's because the height of the patients from the sports hospital was measured in feet, and the height of the patients from the general and prenatal hospital were measured in meters")
