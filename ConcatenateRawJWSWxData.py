'''
    concatenate all existing raw wx data for the JWS stations	
	
	no processing of the data occurs, only combination to a single file
'''
#Import neccessary libraries
import pandas as pd
import glob

glacier= r'gulkana'
elevation='1920'

#List existing raw data files
datadir = r'Q:/Project Data/GlacierData/WeatherStations/JWS/JWS_stations/'
yrfiles=glob.glob(datadir + glacier + '*.csv')

#store column names, set # header rows
header_rws=3

#Loop through raw data files and append all
AllDat=pd.DataFrame() #Initiate empty dataframe
for fl in yrfiles:
    print(" concatinating " + fl)
    #import data
    dat=pd.read_csv(fl, header=header_rws, na_values=['NAN', '#Name?', '#NAME?', '7999','-7999', 'inf', 'INF'])                                                  
    col_nms=pd.read_csv(fl, header=1, nrows=10, warn_bad_lines=False).columns
    dat.columns= col_nms#Name columns
    dat.TIMESTAMP=pd.to_datetime(dat.TIMESTAMP) #overwrite with a date-time format to standardize
    
    AllDat=AllDat.append(dat) #Add the new data to all existing

#reset index numbering
AllDat=AllDat.reset_index(drop=True)

#Strip whitespace from all string-type columns
for col in list(AllDat):
    print ("stripping whitespace from " + col) #print column name    
    if type(AllDat[col].values[0]).__name__ =='str': #if column is a string, strip white space
        AllDat[col]=AllDat[col].str.strip()
        
UnqDat=AllDat.drop_duplicates().copy() #Keeps only unique rows
#need combo date-time column for 990 only

UnqDat=UnqDat.sort_values(by='TIMESTAMP', axis=0).copy()

                             
#Write to file
UnqDat.to_csv(r"Q:/Project Data/GlacierData/Benchmark_Program/Data/" + glacier.capitalize()+ "/AllYears/Wx/Raw/" + glacier+ elevation+ "_5min_all.csv", index=False)
