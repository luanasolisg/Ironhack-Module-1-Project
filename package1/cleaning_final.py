import pandas as pd
import datetime
from functools import reduce

#Convert name columns from both data frames in upper case letter so we can merge forbes web json with pur df
#Function
def upper_case(dataframe , column):
    return dataframe[column].str.upper()

#function for data adquisition:
#import extra data from forbes web json
#https://www.forbes.com/ajax/list/data?year=2018&uri=billionaires&type=person

def merge_df (list_df , column):
    return reduce(lambda left,right: pd.merge(left,right,on=column), list_df)

#Function to separate columns
def separate_columns(dataframe , column, split_ch, T_F):
    return dataframe[column].str.split(split_ch, n = 1, expand = T_F)


#Drop columns
def drop_columns(dataframe , column, T_F):
    return dataframe.drop(column, axis=1,inplace=T_F)

def cleaning(df):
    df_json = pd.read_json('https://www.forbes.com/ajax/list/data?year=2018&uri=billionaires&type=person',
                           orient='records')
    df_forbesjson = df_json[['realTimePosition', 'name', 'age', 'country', 'gender']]
    df_total = [df, df_forbesjson]
    df['name'] = upper_case(df, 'name')
    df_forbesjson['name'] = upper_case(df_forbesjson, 'name')
    df_ppl2 = merge_df(df_total, 'name')
    df_ppl2['Sector'] = separate_columns(df_ppl2, 'Source', '==>', True)[0]
    df_ppl2['Company'] = separate_columns(df_ppl2, 'Source', '==>', True)[1]
    # Worth is billion USD column we will change to millions
    df_ppl2.worth.replace('[ BUSD]+$', '', regex=True, inplace=True)
    df_ppl2['worth(M.USD)'] = df_ppl2['worth'].astype(float) * 1000
    # WorthChange is million USD column we will change to millions and change na to 0.0
    df_ppl2.worthChange.replace('[ millions USD]+$', '', regex=True, inplace=True)
    df_ppl2.worthChange.replace('[na]+$', '0.0', regex=True, inplace=True)
    df_ppl2['worthChange(M.USD)'] = df_ppl2['worthChange'].astype(float)
    # Age without years old
    df_ppl2.age_x.replace('[ years old]+$', '', regex=True, inplace=True)
    df_ppl2.age_x.replace('NaN', '0', regex=True, inplace=True)
    # Unificate age column
    current_year = datetime.datetime.today().year
    age = []
    for i in df_ppl2['age_x'].astype(float):
        if i > 150:
            age.append(str(current_year - int(i)))
        else:
            age.append(i)
    df_ppl2['age_x'] = age
    df_ppl2.gender_x.replace('Male', 'M', regex=True, inplace=True)
    df_ppl2.gender_x.replace('Female', 'F', regex=True, inplace=True)
    df_ppl3 = drop_columns(df_ppl2,['realTimeWorth', 'Unnamed: 0_y', 'Unnamed: 0_x', 'Unnamed: 0', 'lastName', 'Source','worth', 'worthChange'], False)
    df_final = df_ppl3[['realTimePosition_x', 'name', 'age_x', 'Sector', 'Company', 'worth(M.USD)', 'country_y', 'gender_y']]
    df_final = df_final.rename(columns={'realTimePosition_x': 'Position','name': 'Name','age_x': 'Age','worth(M.USD)': 'Worth(M.USD)','country_y': 'Country','gender_y': 'Gender'})
    return df_final


cleaning(df)