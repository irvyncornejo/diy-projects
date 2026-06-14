
class Nextion{
  /*
   * Display
  */  
};

//Auxiliar Functions
void defineAction(byte displayResponse[8]){
  byte byte1 = displayResponse[1];  // Botón->Error | Slider -> Identificador de memoria 
  byte byte2 = displayResponse[2];  // boton->Página desde donde llega la información desde la pantalla | slider-> Valor del componente
  byte byte3 = displayResponse[3];  // Identificación del componente que ha enviado la información desde la pantalla
  byte byte4 = displayResponse[4];  // Evento del componente que se ha enviado
  byte byte5 = displayResponse[5];  // fin de envío FF
  byte byte6 = displayResponse[6];  // "
  byte byte7 = displayResponse[7];  // "
  if(byte1==113){
    servoMotor.write(byte2);
    delay(50);
  }  
  if(byte2==0 && byte3==2 && flagRelay1==false){
    relay1.changeState(true);
    flagRelay1=true;
    byte3=0;
    delay(5);                                       
  }
  if(byte2==0 && byte3==2 && flagRelay1==true){
    relay1.changeState(false);
    flagRelay1 = false;                          
    delay(5);                                 
  }
  if(byte2==0 && byte3==3 && flagMotorA==false){
    motorA.toTurn(false, true);
    flagMotorA=true;
    byte3=0;                         
    delay(5);                                 
  }
  if(byte2==0 && byte3==3 && flagMotorA==true){
    motorA.toStop();
    flagMotorA=false;                  
    delay(5);                                 
  }
}
