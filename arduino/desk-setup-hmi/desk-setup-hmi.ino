#if 1

#include <Adafruit_GFX.h>
#include <MCUFRIEND_kbv.h>
MCUFRIEND_kbv tft;
#include <TouchScreen.h>
#define MINPRESSURE 200
#define MAXPRESSURE 1000

#include <Fonts/FreeSans9pt7b.h>
#include <Fonts/FreeSans12pt7b.h>
#include <Fonts/FreeSerif12pt7b.h>

#include <FreeDefaultFonts.h>

struct Button {
    Adafruit_GFX_Button object;
    int x_position;
    int y_position;
    int button_h;
    int button_w;
    String digit;
};

// ALL Touch panels and wiring is DIFFERENT
// copy-paste results from TouchScreen_Calibr_native.ino
const int XP=6,XM=A2,YP=A1,YM=7; //240x320 ID=0x9340
const int TS_LEFT=171,TS_RT=907,TS_TOP=946,TS_BOT=225;


int led_red = 44;
int led_green = 45;
int led_blue = 46;

TouchScreen ts = TouchScreen(XP, YP, XM, YM, 300);

Adafruit_GFX_Button zero_btn, one_btn, two_btn, tree_btn, four_btn, five_btn, six_btn, seven_btn, eight_btn, nine_btn;

#define BLACK   0x0000
#define BLUECOOL 0x10C6
#define BLUE    0x001F
#define RED     0xF800
#define GREEN   0x07E0
#define CYAN    0x0637
#define MAGENTA 0xF81F
#define YELLOW  0xFFE0
#define WHITE   0xFFFF

#define NUMBERBUTTONS 11

/*{five_btn, 30, 295, 40, 40, "5"},
    {six_btn, 75, 295, 40, 40, "6"},
    {seven_btn, 120, 295, 40, 40, "7"},
    {eight_btn, 165, 295, 40, 40, "8"},
    {nine_btn, 210, 295, 40, 40, "9"}*/
Button buttons[] = {
    {zero_btn, 30, 250, 40, 40, "0"},
    {one_btn, 75, 250, 40, 40, "1"},
    {two_btn, 120, 250, 40, 40, "2"},
    {tree_btn, 165, 250, 40, 40, "3"},
    {four_btn, 210, 250, 40, 40, "4"}
};

int pixel_x, pixel_y;     //Touch_getXY() updates global vars

bool Touch_getXY(void) {
    TSPoint p = ts.getPoint();
    pinMode(YP, OUTPUT);      //restore shared pins
    pinMode(XM, OUTPUT);
    digitalWrite(YP, HIGH);   //because TFT control pins
    digitalWrite(XM, HIGH);
    bool pressed = (p.z > MINPRESSURE && p.z < MAXPRESSURE);
    if (pressed) {
        pixel_x = map(p.x, TS_LEFT, TS_RT, 0, tft.width()); //.kbv makes sense to me
        pixel_y = map(p.y, TS_TOP, TS_BOT, 0, tft.height());
    }
    return pressed;
}

void createMatrixButtons(void){
  for(int i=0; i<NUMBERBUTTONS; i++){
    Button *button = &buttons[i]; 
    button->object.initButton(&tft, button->x_position, button->y_position, button->button_h, button->button_w, WHITE, CYAN, BLUECOOL, button->digit.c_str(), 2);
    button->object.drawButton(false);
  }
}

void setup(void){
  pinMode(led_red, OUTPUT);
  pinMode(led_blue, OUTPUT);
  pinMode(led_green, OUTPUT); 
  Serial.begin(9600);
  uint16_t ID = tft.readID();
  Serial.print("TFT ID = 0x");
  Serial.println(ID, HEX);
  Serial.println("Calibrate for your Touch Panel");
  if (ID == 0xD3D3) ID = 0x9486; // write-only shield
  tft.begin(ID);
  tft.setRotation(0);            //PORTRAIT
  tft.fillScreen(BLUECOOL);
  createMatrixButtons();
  tft.fillRect(40, 80, 160, 80, BLUECOOL);
}

void showmsgXY(int x, int y, int sz, const GFXfont *f, const char *msg){
  int16_t x1, y1;
  uint16_t wid, ht;
  tft.setFont(f);
  tft.setCursor(tft.width()/3, y);
  tft.setTextColor(WHITE);
  tft.setTextSize(sz);
  tft.fillRect(0, y, tft.width(), 24, BLUECOOL);
  tft.print(msg);
}

void select_color(int option){
  switch (option) {
    case 0:
      tft.fillRect(40, 80, 160, 80, MAGENTA);
      break;
    case 1:
      tft.fillRect(40, 80, 160, 80, BLUE);
      break;
    case 2:
      tft.fillRect(40, 80, 160, 80, CYAN);
      break;
    case 3:
      tft.fillRect(40, 80, 160, 80, GREEN);
      break;
    default:
      break;
  }
} 

void loop(void)
{
  bool down = Touch_getXY();
  int digit;
      
  for (int i=0; i<NUMBERBUTTONS; i++){
    Button *button = &buttons[i]; 
    button->object.press(down && button->object.contains(pixel_x, pixel_y));
    if (button->object.justReleased()) button->object.drawButton();
    if(button->object.justPressed()){
      button->object.drawButton(true);
      digit = button->digit.toInt();
      String msg = "";
      msg = "Opcion " + String(digit);
      showmsgXY(20, 180, 2, NULL, msg.c_str());
      select_color(digit);
    }
  }
  /*for (int i=0; i <= 255; i++) {
    analogWrite(led_red, i);
    analogWrite(led_blue, i);
    analogWrite(led_green, i);
    delay(30);
  }*/
}
#endif