library(shiny)
library(leaflet)
library(DT)



# Choices for drop-downs
vars <- c(
  "ALL CRIMES" = "all",
  "BURGLARY" = "BURGLARY",
  "FELONY ASSAULT" = "FELONY ASSAULT",
  "GRAND LARCENY" = "GRAND LARCENY",
  "GRAND LARCENY OF MOTOR VEHICLE" = "GRAND LARCENY OF MOTOR VEHICLE",
  "MURDER" = "MURDER & NON-NEGL. MANSLAUGHTE",
  "RAPE" = "RAPE",
  "ROBBERY" = "ROBBERY"
)



shinyUI(navbarPage("Crime Data", id="nav",
                   
                   tabPanel("NYC map",
                            div(class="outer",
                                
                                tags$head(
                                  # Include our custom CSS
                                  includeCSS("styles.css"),
                                  includeScript("gomap.js")
                                ),
                                
                                leafletOutput("NY_map", width="100%", height="100%"),
                                
                                # Shiny versions prior to 0.11 should use class="modal" instead.
                                absolutePanel(id = "controls", class = "panel panel-default", fixed = TRUE,
                                              draggable = TRUE, top = 60, left = "auto", right = 20, bottom = "auto",
                                              width = 330, height = "auto",
                                              h2("NYPD Crime Data"),
                                              
                                              dateRangeInput("NY_daterange", "Date range:",
                                                             start = "2014-01-01",
                                                             end   = "2015-12-31",
                                                             min = as.Date(min(nyc$DATE)),
                                                             max = as.Date(max(nyc$DATE))
                                                             ),
                                              checkboxInput("NY_cluster", "Add Cluster", value = TRUE),
                                              selectInput("NY_crime", "Show Just type", vars, selected = ''),
                                              plotOutput("NY_plot", click = "plot1_click")
                                ),
                                
                                tags$div(id="cite",
                                         'Data from: ', tags$em('NYPD Motor Vehicle Collisions'), '  | NYC Open Data. 
                                         Details of Motor Vehicle Collisions in New York City provided by the 
                                         Police Department (NYPD).'
                                )
                             )
                   ),
                   tabPanel("Chicago map",
                            div(class="outer",
                                
                                tags$head(
                                  # Include our custom CSS
                                  includeCSS("styles.css"),
                                  includeScript("gomap.js")
                                ),
                                
                                leafletOutput("CH_map", width="100%", height="100%"),
                                
                                # Shiny versions prior to 0.11 should use class="modal" instead.
                                absolutePanel(id = "controls", class = "panel panel-default", fixed = TRUE,
                                              draggable = TRUE, top = 60, left = "auto", right = 20, bottom = "auto",
                                              width = 330, height = "auto",
                                              
                                              h2("CHICAGO Crime Data"),
                                              dateRangeInput("CH_daterange", "Date range:",
                                                             start = "2012-01-01",
                                                             end   = "2015-12-31"),
                                              checkboxInput("CH_cluster", "Add Cluster", value = TRUE),
                                              radioButtons("CH_crime", "Show Just type", vars, selected = '')
                                ),
                                
                                tags$div(id="cite",
                                         'Data from: ', tags$em('Chicago Police Department'), '  | Chicago Open Data. 
                                         Details of Crime in Chicago provided by the Police Department.'
                                )
                                )
                                ),
                   tabPanel("Baltimore map",
                            div(class="outer",
                                
                                tags$head(
                                  includeCSS("styles.css"),
                                  includeScript("gomap.js")
                                ),
                                
                                leafletOutput("BA_map", width="100%", height="100%"),
                                absolutePanel(id = "controls", class = "panel panel-default", fixed = TRUE,
                                              draggable = TRUE, top = 60, left = "auto", right = 20, bottom = "auto",
                                              width = 330, height = "auto",
                                              
                                              h2("BALTIMORE Crime Data"),
                                              dateRangeInput("BA_daterange", "Date range:",
                                                             start = "2012-01-01",
                                                             end   = "2015-12-31"),
                                              checkboxInput("BA_cluster", "Add Cluster", value = TRUE),
                                              radioButtons("BA_crime", "Show Just type", vars, selected = '')
                                ),
                                
                                tags$div(id="cite",
                                         'Data from: ', tags$em('Baltimore Police Department'), '  | Baltimore Open Data. 
                                         Details of Crime in Baltimore provided by the Police Department.'
                                )
                                )
                            ),
                   tabPanel("Analysis",
                            h4("Compare Data between cities (dummy)"),
                            br(),
                            plotOutput("ANA_plot", click = "plot1_click"),
                            absolutePanel(id = "controls", class = "panel panel-default", fixed = TRUE,
                                          draggable = TRUE, top = 60, left = "auto", right = 20, bottom = "auto",
                                          width = 330, height = "auto",
                                          
                                          dateRangeInput("ANA_daterange", "Date range:",
                                                         start = "2012-01-01",
                                                         end   = "2015-12-31")
                            )
                   ),
                   tabPanel("About",
                            br(),
                            h4("Data Source"),
                            p("Source: ",a("NYPD Crime Data | NYC Open Data.",href=
                                    "https://data.cityofnewyork.us/Public-Safety/NYPD-Motor-Vehicle-Collisions/h9gi-nx95")),
                            p("Description: ","Data Details of Crime Data in 
                              New York City provided by the Police Department (NYPD)."),
                            p("Usage: ","Original dataset was downloaded on 07/07/2015, 
                              containing 618,358 accident records from 07/01/2012 to 07/05/2015. 
                              Because of the loading speed concern, this app uses only 10,000 random records 
                              from the original dataset."),
                            br(),
                            h4("Author Information"),
                            p("Allison, Gary Allimu"),
                            p("Website:", a("http://www.website.com",href="http://www.fangzhoucheng.com")),
                            p("Github:", a("http://www.github.com/",href="http://www.github.com/funjo")),
                            br(),
                            br(),
                            p("Allison, Gary Allimu - Copyright @ 2015, All Rights Reserved")
                   ),
                   
                   conditionalPanel("false", icon("crosshair"))
))
