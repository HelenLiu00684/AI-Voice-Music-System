const int DATA_PIN  = 8;
const int CLOCK_PIN = 9;
const int LATCH_PIN = 10;
const int BUTTON_PIN = 2;

volatile bool mic_request=false;

uint16_t led_state = 0;

void setup()
{
    pinMode(DATA_PIN,OUTPUT);
    pinMode(CLOCK_PIN,OUTPUT);
    pinMode(LATCH_PIN,OUTPUT);
    pinMode(BUTTON_PIN,INPUT_PULLUP);
    attachInterrupt(
// Register an interrupt handler that executes
// buttonISR() when BUTTON_PIN transitions
// from HIGH to LOW.
    digitalPinToInterrupt(
        BUTTON_PIN
    ),

    buttonISR,

    FALLING
);


    Serial.begin(115200);

    update595();
}

void loop()
{
    /*
       interrupt event

       button pressed

       send MIC event
    */

    if(mic_request)
    {
        mic_request=false;

        Serial.println(
            "MIC"
        );
    }
    /*
       serial LED command
    */
    if(Serial.available())
    {
        String cmd=
        Serial.readStringUntil('\n');

        cmd.trim();

        parseCommand(cmd);
    }
}

void buttonISR()
{
    mic_request=true;
}

void parseCommand(String cmd)
{
    // ===================== 
    // CLEAR ALL LEDS 
    // ===================== 
    if(cmd=="C") 
    { 
        led_state=0; 
        update595(); 
        return; 
        }
    if(cmd.length()<2)
        return;

    char color=
    toupper(cmd.charAt(0));

    int level=
    cmd.substring(1).toInt();

    if(level<0)
        level=0;

    if(level>4)
        level=4;

    clearGroup(color);

    setGroup(color,level);

    update595();
}

void clearGroup(char color)
{
    int start=
    groupStart(color);

    if(start<0)
        return;
/*
Turn off the target LED bit without affecting other bits
start = 4 ；i =2 Note: one parameters color to clear this level
1<<(start+i) == i<<6 == 1000000
~1<<(start+i) == 1111111110111111
led_state = 0000000000000000
led_state & ~1<<(start+i) == 0000000000000000
*/ 
    for(int i=0;i<4;i++)
    {
        led_state &=
        ~(1<<(start+i));
    }
}
/*
Turn on LEDs from the beginning of a color group
according to the requested level. Note: two parameters color and level
start = 4 ；i =2
1<<(start+i) == i<<6 == 0000000001000000
led_state = 0000000000000000
led_state || 1<<(start+i) == 0000000001000000

start = 4 ；i =0
jump out of the loop "for(int i=0;i<level;i++)"------all light is still shutdown
*/
void setGroup(char color,int level)
{
    int start=
    groupStart(color);

    if(start<0)
        return;

    for(int i=0;i<level;i++)
    {
        led_state |=
        (1<<(start+i));
    }
}

// Return the starting bit position of a color group
// used for mapping LEDs inside led_state.
int groupStart(char color)
{
    switch(color)
    {
        case 'R':

            return 0;

        case 'Y':

            return 4;

        case 'G':

            return 8;

        case 'B':

            return 12;

        default:

            return -1;
    }
}

void update595()
{
    digitalWrite(
        LATCH_PIN,
        LOW
    );

    shiftOut(
        DATA_PIN,
        CLOCK_PIN,
        MSBFIRST,
        highByte(led_state)
    );

    shiftOut(
        DATA_PIN,
        CLOCK_PIN,
        MSBFIRST,
        lowByte(led_state)
    );

    digitalWrite(
        LATCH_PIN,
        HIGH
    );
}