// ========================================
// 74HC595 SINGLE LED TEST
// Hardware Debug Program
// ========================================


// ========================================
// 74HC595 PINS
// ========================================

const int DATA_PIN  = 8;
const int CLOCK_PIN = 12;
const int LATCH_PIN = 11;


// ========================================
// SINGLE TEST LED
// ========================================
//
// 0b00000001
// = QA HIGH
//
// QA = pin15
//
// ========================================

const byte TEST_LED = 0b00000001;


// ========================================
// WRITE TO 74HC595
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
// SETUP
// ========================================

void setup()
{
    pinMode(DATA_PIN, OUTPUT);

    pinMode(CLOCK_PIN, OUTPUT);

    pinMode(LATCH_PIN, OUTPUT);

    write595(0b00000000);
}


// ========================================
// LOOP
// ========================================

void loop()
{
    // LED ON
    write595(TEST_LED);

    delay(1000);

    // LED OFF
    write595(0b00000000);

    delay(1000);
}