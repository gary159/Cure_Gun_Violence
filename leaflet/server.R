library(shiny)
library(leaflet)
library(RColorBrewer)
library(scales)
library(lattice)
library(dplyr)


draw <- nyc

shinyServer(function(input, output, session) {
  
## Interactive Map ###########################################
  
  # Create the map
  output$NY_map <- renderLeaflet({
    leaflet() %>%
      addTiles(
        urlTemplate = "//{s}.tiles.mapbox.com/v3/jcheng.map-5ebohr46/{z}/{x}/{y}.png",
        attribution = 'Maps by <a href="http://www.mapbox.com/">Mapbox</a>'
      ) %>%
      setView(lng = -73.97, lat = 40.75, zoom = 13)
  })
  

  
  # Choose just one crime
  drawvalue <- reactive({if (input$NY_crime == ''){
    t <- filter(draw, DATE > input$NY_daterange[1], DATE < input$NY_daterange[2])
    return(t)}
    else{
    t <- filter(draw, OFFENSE == input$NY_crime)
    return(t)
  }})
  
  # This observer is responsible for maintaining the circles and legend,
  # according to the variables the user has chosen to map to color and size.
  observe({
    draw <- drawvalue()
    colorData <- draw$OFFENSE
    radius <- 30
    pal <- colorFactor("Set1", colorData)
    if (input$NY_cluster == TRUE){
      leafletProxy("NY_map", data = draw) %>%
        clearShapes() %>%
        showGroup('Cluster') %>%
        addCircles(~LONGITUDE, ~LATITUDE, radius=radius, group = "Circle",
                   stroke=FALSE, fillOpacity=0.8, fillColor=pal(colorData), popup = nyc$OFFENSE) %>%
        clearMarkerClusters() %>%
        addCircleMarkers(~LONGITUDE, ~LATITUDE, radius = 0, group = "Cluster",
                         clusterOptions = markerClusterOptions())%>%
        addLegend("bottomleft", pal=pal, values=colorData,
                  layerId="colorLegend")
    }else{
      leafletProxy("NY_map", data = draw) %>%
        clearShapes() %>%
        hideGroup('Cluster') %>%
        addCircles(~LONGITUDE, ~LATITUDE, radius=radius, group = "Circle",
                   stroke=FALSE, fillOpacity=0.8, fillColor=pal(colorData), popup = nyc$OFFENSE) %>%
        addLegend("bottomleft", pal=pal, values=colorData,
                  layerId="colorLegend")
    }
  })
  
  #Create plot 
  output$NY_plot <- renderPlot({
    #g <- ggplot(filter(nyc, DATE< input$NY_daterange[2], DATE > input$NY_daterange[1]), aes(OFFENSE))
    #g + geom_bar()
    filter_nyc = filter(nyc, DATE< input$NY_daterange[2], DATE > input$NY_daterange[1])
    qplot(OFFENSE, data=filter_nyc, geom="bar", fill=OFFENSE)+ 
      scale_fill_brewer(palette="Set1", guide=FALSE) + 
      ggtitle("Number of crime by type")+
      theme(axis.title.x=element_blank(),
            axis.text.x=element_blank(),
            axis.ticks.x=element_blank())
  })
  ## CHICAGO Interactive Map ###########################################
  
  # Create the map
  output$CH_map <- renderLeaflet({
    leaflet() %>%
      addTiles(
        urlTemplate = "//{s}.tiles.mapbox.com/v3/jcheng.map-5ebohr46/{z}/{x}/{y}.png",
        attribution = 'Maps by <a href="http://www.mapbox.com/">Mapbox</a>'
      ) %>%
      setView(lng = -87.62, lat = 41.87, zoom = 14)
  })
  
  ## BALTIMORE Interactive Map ###########################################
  
  # Create the map
  output$BA_map <- renderLeaflet({
    leaflet() %>%
      addTiles(
        urlTemplate = "//{s}.tiles.mapbox.com/v3/jcheng.map-5ebohr46/{z}/{x}/{y}.png",
        attribution = 'Maps by <a href="http://www.mapbox.com/">Mapbox</a>'
      ) %>%
      setView(lng = -76.61, lat = 39.29, zoom = 14)
  })
  
  ## ANALYSIS ############################################################
  
  output$ANA_plot <- renderPlot({
    g <- ggplot(filter(nyc, DATE< input$ANA_daterange[2], DATE > input$ANA_daterange[1]), aes(OFFENSE))
    g + geom_bar()
  })
  
  
  })




