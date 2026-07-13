char t = 'S';
int frontIr = A4;
int backIr = A5;

void setup() {
pinMode(13,OUTPUT);   //left motors forward
pinMode(12,OUTPUT);   //left motors reverse
pinMode(11,OUTPUT);   //right motors forward
pinMode(10,OUTPUT);   //right motors reverse
pinMode(9,OUTPUT);    //hand 1 front
pinMode(8,OUTPUT);    //HAND 1 REV
pinMode(7,OUTPUT);    //HAND 2 FRONT
pinMode(6,OUTPUT);    // HAND 2 REV
pinMode(5,OUTPUT);    //Head FRONT
pinMode(4,OUTPUT);    // Head REV
pinMode(frontIr,INPUT);    // left ir
pinMode(backIr,INPUT);    // right ir
Serial.begin(9600);
 
}
 
void loop() {
int  frontSen = analogRead(frontIr);
int  backSen = analogRead(backIr);
 
//  long duration, distance;
//  digitalWrite(trig,HIGH);
//  delayMicroseconds(1000);
//  digitalWrite(trig,LOW);
//  duration = pulseIn(echo,HIGH);
//  distance = (duration/2)/29.1;
//  Serial.print(distance);
//  Serial.println("CM");
//  delay(10);
  if(Serial.available()){
    t = Serial.read();
    Serial.println(t);
  }

  if(frontSen<35 || backSen<35){ 
    legStop();
    t="S";
  };

  if(t == 'L'){            //MOVE LEFT
    digitalWrite(13,HIGH);
    digitalWrite(11,HIGH);
  }
   
  else if(t == 'R'){      //MOVE RIGHT
    digitalWrite(12,HIGH);
    digitalWrite(10,HIGH);
  }
   
  else if(t == 'B'){      //MOVE BACKWARD
    digitalWrite(12,HIGH);
    digitalWrite(11,HIGH);
  }
  
  else if(t == 'F'){      //MOVE FORWARD
    digitalWrite(13,HIGH);
    digitalWrite(10,HIGH);
  }
  
  else if(t == 'S'){      //STOP (all legs motors stop)
    digitalWrite(13,LOW);
    digitalWrite(12,LOW);
    digitalWrite(11,LOW);
    digitalWrite(10,LOW);
  }
  
  else if(t == 'J'){      //hand 1 front
    digitalWrite(9,HIGH);
  }
  
  else if(t == 'N'){      //hand 1 rev
    digitalWrite(8,HIGH);
  }
  
  else if(t == 'K'){      //hand 2 front
    digitalWrite(7,HIGH);
  }
  
  else if(t == 'q'){      //hand 2 front
    digitalWrite(7,HIGH);
    delay(500);
    digitalWrite(7,LOW);
  }
  
  else if(t == 'M'){      //hand 2 rev
    digitalWrite(6,HIGH);
  }
  
  else if(t == 'X'){      //STOP (all hand motors stop)
    digitalWrite(6,LOW);
    digitalWrite(7,LOW);
    digitalWrite(8,LOW);
    digitalWrite(9,LOW);
  }
  
  else if(t == 'o'){      //head right
    digitalWrite(5,HIGH);
  }
  
  else if(t == 'p'){      // head left
    digitalWrite(4,HIGH);
  }
  
  else if(t == 'u'){      //head stop
    digitalWrite(5,LOW);
    digitalWrite(4,LOW);
  }
  
  
  delay(100);
}

void legStop(){
  digitalWrite(13,LOW);
  digitalWrite(12,LOW);
  digitalWrite(11,LOW);
  digitalWrite(10,LOW);
}
