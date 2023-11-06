//bueno
int sensorPin = A0;   
float valorsensor;
//float valorsensor2;
char readed;
String fill;
int fillint;
bool wait;
String ok;
bool test;

void setup() 
{
  Serial.begin(9600);
  pinMode(13, OUTPUT);
  wait = false;
  ok = "False";
  test=false;
}

void loop() 
{
  //delay(50);
  if (Serial.available() || test==true) 
  {
    readed = Serial.read();
    fill +=readed;
    if(readed=='\n' || test==true)
    {
       fillint=fill.toInt();
       if(test==true){
        fillint=11;
       }
       if(fillint == 10 || fillint == 11){
       valorsensor= analogRead(sensorPin);
        if(valorsensor < 155){
        valorsensor=155;
       }
        if(valorsensor > 520){
        valorsensor=520;
       }
       if(test==true){
        Serial.println(valorsensor);
       }
       valorsensor=map(valorsensor, 520, 155, 0, 100);
       Serial.print(wait);
       Serial.print(",");

       Serial.println(valorsensor);
          if(wait){
            digitalWrite(13, HIGH);
            if (valorsensor > 95){
              wait = false;
              ok = "False";
            }
          }

          else if(valorsensor < 80){
            digitalWrite(13, HIGH);
            wait = true;
            ok = "True";
          }
        
          else if(fillint == 11){
            digitalWrite(13, HIGH);
          }
          else {
          digitalWrite(13, LOW);
          }
        }
        else{
          digitalWrite(13, LOW);
        }

        
        fill="";
    }
   }
}
