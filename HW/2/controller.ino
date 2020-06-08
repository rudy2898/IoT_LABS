#include <LiquidCrystal_PCF8574.h>

LiquidCrystal_PCF8574 lcd(0x27);

const int FAN_PIN = 5;
const int TEMP_PIN = A0;
const int LED_PIN = 9;
const int PIR_PIN = 7;
const int SOUND_PIN = 4;
const int LIGHT_PIN = 12;

const int B = 4275;
const long int R0 = 100000;

const int timeout_pir = 10000;
const int timeout_sound = 60000; //se l'ultima rilevazione risale a più di 1 minuto fa non c'è nessuno
const int sound_interval = 500; //campionamento sensore
const int minutes5 = 300000;


//variabili per n_sound_events
boolean first_half = true;
int n_events_first = 0;
int n_events_second = 0;
unsigned long int camp = 0; //ultimo istante di campionamento 

//valori dal seriale e anche i set points
int fan_values[4];
int led_values[4];

//fan setpoints
int fan_min = 20;
int fan_max = 25;


//led setpoints
int led_min = 15;
int led_max = 25;

//lampadina smart
unsigned long int c;
int light_time = 500; //periodo campionamento pir
int value = LOW; //stato led


unsigned long int last; //ultimo istante in cui si è registrato un interrupt del PIR
unsigned long int ss;
unsigned long int sound_event;

int v_max = 255; //valore massimo di tensione del led e del motore DC

float temp;
int current_speed = 0;
int current_light = 0;
int sound_is_present = 0;
int pir_is_present = 0;
int is_present = 0;
int n_sound_events;
unsigned long int s = 0; //conteggio 10 minuti

void setSpeed(float temp);
void setLight(float temp);
void PIRisr();
float readTemp();
void printLCD();
void turnLightOn();

void setup() {

  //lcd init
  lcd.begin(16, 2);
  lcd.setBacklight(255);
  lcd.home();
  lcd.clear();

  Serial.begin(9600);
  Serial.print("Starting...");
  last=millis();
  ss=millis();
  sound_event=0;

  pinMode(LED_PIN, OUTPUT);
  pinMode(FAN_PIN, OUTPUT);
  pinMode(PIR_PIN, INPUT);
  pinMode(SOUND_PIN, INPUT);
  pinMode(LIGHT_PIN, OUTPUT);

  analogWrite(FAN_PIN, (int) current_speed); //velocità fan parte da 0
  analogWrite(LED_PIN, (int) current_light); //luminosità led parte da 0

  attachInterrupt(digitalPinToInterrupt(PIR_PIN), PIRisr, FALLING);
}

void changeSetPoints(){
    if (is_present == 0) {
        fan_min = fan_values[2];
        fan_max = fan_values[3];
        led_min = led_values[2];
        led_max = led_values[3];
    } else {
        fan_min = fan_values[0];
        fan_max = fan_values[1];
        led_min = led_values[0];
        led_max = led_values[1];
    }
}

void event(){
  if(first_half == true){
    n_events_first++;
  } else n_events_second++;
}

void readSound() {
  
  if(millis() - sound_event >= timeout_sound){ //60 minuti set is_present
    sound_is_present = 0;
    is_present = pir_is_present | sound_is_present;
    changeSetPoints();
    sound_event = millis();
  }

  if(millis() - ss >= minutes5){//cambio prima e seconda metà
    if(first_half == true){
      n_events_second = 0;
    } else {
      n_events_first = 0;
    }
    first_half=!first_half;
  }

  if(millis() - camp >= sound_interval){ //campionamento 500ms
      if(digitalRead(SOUND_PIN) == LOW) {
      Serial.println(n_sound_events);
      event();
      camp = millis();
    }
  }
  
  if(millis() - s >= sound_interval){ //intervallo da 10 minuti
    n_sound_events = n_events_first + n_events_second;
    if(n_sound_events > 50) {
        sound_event = millis();
        sound_is_present = 1;
//        Serial.println(n_sound_events);
    }
//    Serial.println(n_sound_events);
    s = millis();
   } 
}

void loop() {
    temp = readTemp();
//    Serial.print(temp);
//    setSpeed(temp);
//    setLight(temp);
    readSound();
    printLCD();

    

}

void PIRtimeout(){
      if(millis() - last >= timeout_pir){
      pir_is_present = 0;
      is_present = pir_is_present | sound_is_present;
      changeSetPoints();
      Serial.println("Nessuno.");
//        Serial.println(last);
      last = millis();
    }
}
void setSpeed(float temp){
  int current_speed;
  if(temp > fan_min && temp < fan_max){ //temperatura in range
      current_speed = v_max * temp / fan_max;
  } else if(temp < fan_min) {
      current_speed = 0;
  } else {
      current_speed = 255;
  }
    analogWrite(FAN_PIN, (int) current_speed);
}

void setLight(float temp){
    if(temp > led_min && temp < led_max) { //temperatura in range
        current_light = v_max * (1 - (temp / led_max));
//    Serial.print(current_light);
//   Serial.print('\n');
    } else if(temp < led_min){
        Serial.println("min");
        current_light = 255;
    } else {
        current_light = 0;
    }
    analogWrite(LED_PIN, (int) current_light);
}

void PIRisr(){
    pir_is_present = 1;
//    Serial.println("Movimento rilevato.");
    last = millis();
//    return pir!=0;
}

float readTemp(){
    int sig = analogRead(TEMP_PIN);
    float R = ((1023.0/sig) - 1.0);
    R = (float) R * R0;
    float log_sig = log(R/R0);
    float temp = 1/((log_sig/B) + 1/298.15) - 273.15;
    return temp;
}

void insertSetPoints(){
  Serial.println("Inserire valori per Riscaldamento (prima valori per presente): ");
  int i=0;
  while(i<4){
    if(Serial.available()>0){
      int inByte = Serial.read();
      fan_values[i]=inByte;
      i++;
    }
  }

  Serial.println("Inserire valori per Condizionamento (prima valori per presente): ");
  i=0;
  while(i<4){
    if(Serial.available()>0){
      int inByte = Serial.read();
      led_values[i]=inByte;
      i++;
    }
  }
}

void printLCD(){
  lcd.home();
  lcd.print("Temp:");
  lcd.print(temp);
  lcd.print("Pres:");
  lcd.print(is_present);
  lcd.setCursor(0,1);
  int fan = current_speed / 255 * 100;
  int led = current_light / 255 * 100;
  lcd.print("AC:");
  lcd.print(fan);
  lcd.print("HT:");
  lcd.print(led);
  delay(5000);
  lcd.clear();
  lcd.home();
  lcd.print("AC m:");
  lcd.print(fan_min);
  lcd.print("M:");
  lcd.print(fan_max);
  lcd.setCursor(0,1);
  lcd.print("HT m:");
  lcd.print(led_min);
  lcd.print("M:");
  lcd.print(led_max);
}

void turnLightOn(){
    int n=0;
  if(millis() - c >= light_time){
      for(int i=0; i < 4; i++){
          if(digitalRead(SOUND_PIN) == LOW){
              delay(400);
              n++;
          }
      }
      if(n == 2){
          value=!value;
          digitalWrite(LIGHT_PIN, value);
      }
      c = millis();
  }
}
