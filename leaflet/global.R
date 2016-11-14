library(dplyr)
library(RColorBrewer)
library(ggplot2)
# Data cleaning to get rid of records with no geo info

# Import truncate data
#setwd("/Users/garyair/Code/columbia/Cure_Gun_Violence/")
#df <- read.csv('data/nyc/NYPD_7_Major_Felony_Incident_Map_2012.csv')
#df$DATE = as.Date(df$Occurrence.Date,format="%m/%d/%Y %T")
#df = rename(df,X=OBJECTID, BOROUGH=Borough,UNIQUE.KEY=Identifier, LOCATION=Location.1, DAY=Day.of.Week, MONTH=Occurrence.Month)
#names(df) <- toupper(names(df))
#dfl <- read.table(text=gsub('[()]', '', df$LOCATION), 
#                  sep=",", col.names=c('Latitute', 'Longitude'))
#df$LATITUDE <- dfl$Latitute
#df$LONGITUDE <- dfl$Longitude
#df = select(df, X, DATE , LATITUDE,LONGITUDE,OFFENSE, PRECINCT,BOROUGH, JURISDICTION, DAY, MONTH)
#head(df,5)
#write.csv(df, file = 'data/nyc/NYPD_7_Major_Felony_Incident_Map_2012_clean.csv', row.names=FALSE)


#set.seed(100)
#df_small <- df[sample.int(nrow(df), 1000),]
#head(df_small,2)
#write.csv(df_small, file = 'data/nyc/NYPD_7_Major_Felony_Incident_Map_2012_clean(1000 obs).csv', row.names=FALSE)
nyc <- read.csv('data/NYPD_7_Major_Felony_Incident_Map_2012_clean(1000 obs).csv', stringsAsFactors=FALSE)

