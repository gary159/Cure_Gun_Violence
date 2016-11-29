// Import libraries
import processing.pdf.*;

// Global Objects
Table crime, gun;
PFont font;

void setup(){
  size(700,1000);
  noLoop();
  loadData();
  beginRecord(PDF, "hour_violence_NYCHIBA.pdf");
  background(0, 0, 20);
  legend();
  createGraph(crime, 90, 80, 2368*2/3, -2035*2/3);
  createGraph(gun, 550, 80, 1623*2/3,-2053*2/3);
  drawing();
  endRecord();
  }

void legend(){
  font = createFont("NeutraTextLight.otf", 2, true);
  textFont(font);
  textSize(25);
  text("CRIME AND GUN VIOLENCE HOURLY", 80,30);
  
  textSize(12);
  text("NUMBER OF CRIMES BELOW THE MEAN", 80,50);                               
  text("ABOVE THE MEAN", 410,50);
  textSize(10);
  text("SOURCE : NYC, CHICAGO AND BALTIMORE OPEN DATA: 2010-2016", 310,980);
  
  textSize(12);
  colorMode(HSB, 360, 100, 100);
  fill(0, 0,100, 300);
  rect(78, 67, 118, 13);
  fill(0, 0, 0);
  text("ALL TYPES OF CRIME", 80,78);
  fill(0, 0, 100); 
  
  colorMode(HSB, 360, 100, 100);
  fill(0, 0,100, 300);
  rect(78, 520, 90, 13);
  fill(0, 0, 0);
  text("GUN VIOLENCE", 80,531);
  fill(0, 0, 100); 
  
  textSize(10);
  pushMatrix();
  translate(25,240);
  rotate(-HALF_PI);
  text("CHICAGO",0,0);
  text("NEW YORK",-150,0);
  text("BALTIMORE",-230,0);
  popMatrix();
  pushMatrix();
  translate(25,700);
  rotate(-HALF_PI);
  text("CHICAGO",0,0);
  text("NEW YORK",-150,0);
  text("BALTIMORE",-230,0);
  popMatrix(); 
}

void createGraph(Table thetable, int start_pixel_x, int start_pixel_y, int max, int min){
  
  colorMode(HSB, 360, 100, 100);
  font = createFont("NeutraTextLight.otf", 2, true);
  textFont(font);
  fill(0, 0, 100);
  textSize(8);
  String stationName;
  textAlign(RIGHT);
  noStroke();
  // WRITE HOURS


  String t, pday;
  for (int k=0; k<24; k++){
    println(k);
   if (k == 0){
   text("12 AM", start_pixel_y+32 +25*k,start_pixel_x);
   }
   else if (k == 12){
   text("12 PM", start_pixel_y+32 +25*k,start_pixel_x);
   }
   else if (k<12){
     pday = " AM";
     t = k + pday; 
     text(t, start_pixel_y+32 +25*k,start_pixel_x);
   }
   else {
     pday = " PM";
     t = k-12 + pday;
     println(t);
     text(t, start_pixel_y+32+25*k,start_pixel_x);     
   }
  }
  
  // MATRIX
  for (int i=0; i<thetable.getRowCount(); i++){
    stationName = thetable.getString(i, "District");
    fill(0, 0, 100);
    text(stationName, start_pixel_y+5, start_pixel_x+10+i*11);
    for (int j=0; j<24; j++){
      float hourValue = thetable.getInt(i, (j+1)); 
      float alphaValue;
      //println(hourValue);
      if (hourValue >= 0){
        alphaValue = map(hourValue, 0, max, 0, 100);
        //println(alphaValue);
        fill(10, 100, 100, alphaValue);
      }
      else{
        alphaValue = map(hourValue, 0, min, 0, 100);
        //println(alphaValue);
        fill(200, 50, 100, alphaValue);
      }
      rect(start_pixel_y+10 + j*25, start_pixel_x + 3.5 + i*11, 24.5, 10.5);
    }
  }
}

void loadData(){
  crime = loadTable("NY_CHI_BA_perhour_norm.csv", "header");
  gun = loadTable("NY_CHI_BA_perhour_gun_norm.csv", "header");
  println("ok");
}

void drawing(){
  colorMode(HSB, 360, 100, 100);
  for (int i=0; i<50; i++){
      fill(10, 100,100, 2*i);
      rect(350+i, 40, 5, 10);
      fill(200, 50,100, 2*i);
      rect(350-i, 40, 5, 10);
  }
}