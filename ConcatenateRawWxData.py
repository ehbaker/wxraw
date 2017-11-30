'''
	script to concatenate all existing raw wx data files for the Wolverine 990m station
	
	no processing of the data occurs, only combination to a single file
'''
#Import neccessary libraries
import pandas as pd
import glob
import ntpath

#For Wolverine 990 - station='wolverine990'
#For Wolv 1420 (aka JWS), station = 'wolverine1420'
station= r'wolverine990'
#station=r'wolverine1420'

#output base name
file_label="15min"


#List existing raw data files
#Wolv990 is text; wolv1420 is csv, slight difference
datadir = r'Q:/Project Data/GlacierData/Benchmark_Program/Data/Wolverine/*/Wx/'
if station== r'wolverine990':
    yrfiles=glob.glob(datadir + station + '*.txt')
    header_rws=2 #number of header rows to not read in
    col_nms=["Date", "Time", "Instrument", "Value", "Unit", "Flag"]
if station==r'wolverine1420':
    header_rws=4 #number of header rows to not read in
    yrfiles=glob.glob(datadir + station + '*.csv')
    #Grab correct column names (a few rows up in Campbell Logger output)
    coltable=pd.read_csv(yrfiles[0], header=1)
    col_nms=coltable.columns
#Loop through raw data files and append
AllDat=pd.DataFrame() #Initiate empty dataframe
for fl in yrfiles:
    print(" concatinating " + fl)
	#One raw data file is saved as tab-separated text, so must be imported with slight difference
    if ntpath.basename(fl) == station + r"_2010_0707.txt":
        dat=pd.read_csv(fl, header=header_rws, sep='\t')
    else:
        dat=pd.read_csv(fl, header=header_rws)
    dat.columns= col_nms#Name columns
    
    #Standardize Date Format for Wolv1420
    if station==r'wolverine1420':
        dat.TIMESTAMP=pd.to_datetime(dat.TIMESTAMP) #overwrite with a date-time format to standardize
    
    AllDat=AllDat.append(dat) #Add the new data to all existing

#Strip whitespace from all string-type columns
for col in list(AllDat):
    print ("stripping whitespace from " + col) #print column name    
    if type(AllDat[col].values[0]).__name__ =='str': #if column is a string, strip white space
        AllDat[col]=AllDat[col].str.strip()
        
UnqDat=AllDat.drop_duplicates().copy() #Keeps only unique rows
#need combo date-time column for 990 only
if station== r'wolverine990':
    UnqDat["DateTime"]= UnqDat.Date + " " + UnqDat.Time #create new Date + Time column
                             
#Write to file
UnqDat.to_csv(r"Q:/Project Data/GlacierData/Benchmark_Program/Data/Wolverine/AllYears/Wx/Raw/" + station.capitalize() + "_" + file_label +"_all.csv", index=False)

#ID MIssing Dates
#alldates = UnqDat['TIMESTAMP'].dt.strftime('%Y/%m/%d')
#alldates=alldates.drop_duplicates().copy()
#alldates.to_csv(r"C:\Users\ehbaker\Desktop\alldates.csv")