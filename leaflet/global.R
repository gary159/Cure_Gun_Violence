library(dplyr)

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
nyc <- read.csv('NYPD_7_Major_Felony_Incident_Map_2012_clean(1000 obs).csv')#, stringsAsFactors=FALSE)


previewColors(colorFactor("Set1", domain = nyc$OFFENSE), nyc$OFFENSE)


nycColors <- brewer.pal(7,"Set1")
names(nycColors) <- levels(nyc$OFFENSE)
colScale <- scale_fill_manual(name = "OFFENSE",values = nycColors)
qplot(OFFENSE, data=nyc, geom="bar")+colScale
ggplot(nyc, aes(OFFENSE, fill = OFFENSE)) + geom_bar() +colScale

nycColors
pal <- colorFactor("Set1", nyc$OFFENSE)

previewColors(colorFactor("Set1", domain = nyc$OFFENSE), nyc$OFFENSE)
qplot(OFFENSE, data=nyc, geom="bar", fill=OFFENSE)+ scale_fill_brewer(nycColors) + ggtitle("Number of crime by type")

qplot(OFFENSE, data=nyc, geom="bar", fill=OFFENSE)+ scale_fill_brewer(palette="Set2", guide=FALSE) + ggtitle("Number of crime by type")




dat <- data.frame(x=runif(10),y=runif(10),
                  grp = rep(LETTERS[1:5],each = 2),stringsAsFactors = TRUE)

#Create a custom color scale
library(RColorBrewer)
myColors <- brewer.pal(6,"Set1")
myColors

names(myColors) <- levels(dat$grp)
colScale <- scale_colour_manual(name = "OFFENSE",values = nycColors)
#One plot with all the data
p <- ggplot(dat,aes(x,y,colour = grp)) + geom_point()
p1 <- p + colScale

#A second plot with only four of the levels
p2 <- p %+% droplevels(subset(dat[4:10,])) + colScale

