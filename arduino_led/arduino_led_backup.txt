// ========================================
// AI Music Embedded System
// Arduino + 74HC595 + Interrupt Button
// ========================================


// ========================================
// 74HC595 pins
// ========================================

const int DATA_PIN  = 8;
const int CLOCK_PIN = 12;
const int LATCH_PIN = 11;


// ========================================
// BUTTON
// ========================================

const int BUTTON_PIN = 2;


// ========================================
// LED bit mapping
// ========================================

const byte RED_LED    = 0b00000001;
const byte YELLOW_LED = 0b00000010;
const byte BLUE_LED   = 0b00000100;
const byte GREEN_LED  = 0b00001000;


// ========================================
// timing
// ========================================

unsigned long lastRed    = 0;
unsigned long lastYellow = 0;
unsigned long lastBlue   = 0;
unsigned long lastGreen  = 0;


// ========================================
// LED states
// ========================================

bool redState    = false;
bool yellowState = false;
bool blueState   = false;
bool greenState  = false;


// ========================================
// system state
// ========================================

bool musicMode = false;


// ========================================
// interrupt flag
// ========================================

volatile bool micRequest = false;


// ========================================
// serial char
// ========================================

char c;


// ========================================
// interrupt service routine
// ========================================

void buttonISR()
{
    micRequest = true;
}


// ========================================
// write to 74HC595
// ========================================

void write595(byte value)
{
    digitalWrite(LATCH_PIN, LOW);

    shiftOut(
        DATA_PIN,
        CLOCK_PIN,
        MSBFIRST,
        value
    );

    digitalWrite(LATCH_PIN, HIGH);
}


// ========================================
// startup animation
// ========================================

void startupAnimation()
{
    write595(0b11111111);

    delay(1000);

    write595(0b00000000);

    delay(1000);
}


// ========================================
// setup
// ========================================

void setup()
{
    pinMode(DATA_PIN, OUTPUT);

    pinMode(CLOCK_PIN, OUTPUT);

    pinMode(LATCH_PIN, OUTPUT);

    pinMode(BUTTON_PIN, INPUT_PULLUP);

    Serial.begin(9600);

    attachInterrupt(
        digitalPinToInterrupt(BUTTON_PIN),
        buttonISR,
        FALLING
    );

    write595(0);

    startupAnimation();
}


// ========================================
// loop
// ========================================

void loop()
{
    // ====================================
    // BUTTON INTERRUPT EVENT
    // ====================================

    if (micRequest)
    {
        Serial.println("MIC");

        micRequest = false;
    }


    // ====================================
    // SERIAL EVENTS
    // ====================================

    if (Serial.available())
    {
        c = Serial.read();

        // START MUSIC MODE
        if (c == 'M')
        {
            musicMode = true;
        }

        // STOP MUSIC MODE
        else if (c == 'S')
        {
            musicMode = false;

            write595(0);
        }
    }


    // ====================================
    // IDLE MODE
    // ====================================

    if (!musicMode)
    {
        return;
    }


    // ====================================
    // RHYTHM MODE
    // ====================================

    unsigned long now = millis();


    // RED
    if (now - lastRed >= 120)
    {
        lastRed = now;

        redState = !redState;
    }


    // YELLOW
    if (now - lastYellow >= 250)
    {
        lastYellow = now;

        yellowState = !yellowState;
    }


    // BLUE
    if (now - lastBlue >= 600)
    {
        lastBlue = now;

        blueState = !blueState;
    }


    // GREEN
    if (now - lastGreen >= 1000)
    {
        lastGreen = now;

        greenState = !greenState;
    }


    // rebuild output
    byte ledOutput = 0;


    if (redState)
    {
        ledOutput |= RED_LED;
    }

    if (yellowState)
    {
        ledOutput |= YELLOW_LED;
    }

    if (blueState)
    {
        ledOutput |= BLUE_LED;
    }

    if (greenState)
    {
        ledOutput |= GREEN_LED;
    }


    // update LEDs
    write595(ledOutput);
}