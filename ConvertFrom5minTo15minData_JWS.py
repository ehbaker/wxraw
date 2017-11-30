'''
convert weather station data from 5 minute to 15 minute
'''
import pandas as pd
import numpy as np


glacier='gulkana'
elevation='1920'

#Set constants
date_format='%Y-%m-%d %H:%M:%S' #input date format (change if yours is different)
out_date_format='%Y/%m/%d %H:%M'
timezone='America/Anchorage' #choose from pytz.all_timezones

#Location of output for ConcatenateRawData_JWS.py script
pth=r"Q:/Project Data/GlacierData/Benchmark_Program/Data/" + glacier.capitalize()+ "/AllYears/Wx/Raw/" + glacier+ elevation+ "_5min_all.csv"
out_pth=r"Q:/Project Data/GlacierData/Benchmark_Program/Data/" + glacier.capitalize()+ "/AllYears/Wx/Raw/" + glacier+ elevation+ "_15min_all.csv"


#Read in data
dat=pd.read_csv(pth)
dat.loc[:,'DateTime']=pd.to_datetime(dat['TIMESTAMP'], format=date_format) #set to date-time from string
dat['DateTime']=dat['DateTime'].dt.round('5min') #round time to the nearest 5 minute value

#Set time as index
dat=dat.set_index('DateTime')

#Create 15 min values from the logger 5 min values
average_val_cols=['AirTempC_Avg', 'BP_inHg_Avg', 'BattV_Avg', 'RH', 'WS_ms_S_WVT']
cumulative_val_cols=['PyrgDnT_Avg', 'PyrgDn_Avg', 'PyrgUpT', 'PyrgUpT_Avg','PyrgUp_Avg', 'PyrnDn_Avg', 'PyrnUp_Avg']
wind_dir_columns=['WindDir_D1_WVT', 'WindDir_SD1_WVT']

#Create empty dataframe to store 15min data
fifteenmin_dat=pd.DataFrame() #create empty dataframe

#Create 15-min average values
for col in average_val_cols:
    fifteenmin_dat[col]=dat[col].resample('15min').mean()
#create 15-min vumulative values 
for col in cumulative_val_cols:
    fifteenmin_dat[col]=dat[col].resample('15min').sum()
#Wind Direction - this process is for data that is logged as vector-averaged 
for wd_col in wind_dir_columns:
#Convert to raidans
    dat['wind_dir_cos']=np.cos(dat[wd_col]*(np.pi/180))
    dat['wind_dir_sin']=np.sin(dat[wd_col]*(np.pi/180))

    #Calculate mean of x and y directions in radian space
    fifteenmin_dat['wind_dir_cos']=dat.wind_dir_cos.resample('15min').mean()
    fifteenmin_dat['wind_dir_sin']=dat.wind_dir_sin.resample('15min').mean()

    #Convert back to 0-360 coordinates
    fifteenmin_dat[wd_col]=(np.arctan2(fifteenmin_dat.wind_dir_sin, fifteenmin_dat.wind_dir_cos) * 180/np.pi)
    fifteenmin_dat.loc[fifteenmin_dat[wd_col]<0, wd_col]+=360 #add 360 where hourly dat less than 0
    
#Create new format of time for saved version
fifteenmin_dat['DateTime']=fifteenmin_dat.index.strftime(date_format)

#Reshape so that is in long (v wide) format, to mirror Sutron logger output
fifteenmin_dat_long=pd.melt(fifteenmin_dat, id_vars='DateTime')

#Sort with oldest first
fifteenmin_dat_long=fifteenmin_dat_long.sort_values(by='DateTime', axis=0)

fifteenmin_dat_long.to_csv(out_pth, index=False)
print("Saved data to " + out_pth)

    