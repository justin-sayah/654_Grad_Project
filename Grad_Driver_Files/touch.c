#include "touch.h"
#include <p33FJ256MC710.h>

uint8_t selected_dim = X_DIM_TOUCH;

void touch_init(void) {
    // Configuration pins for touchscreen
    
    // set up the I/O pins E1, E2, and E3 to be output pins
    CLEARBIT(TRISEbits.TRISE1);
    CLEARBIT(TRISEbits.TRISE2);
    CLEARBIT(TRISEbits.TRISE3);
    
    // initialize pins to standby mode
    SETBIT(LATEbits.LATE1);
    SETBIT(LATEbits.LATE2);
    CLEARBIT(LATEbits.LATE3);
    
    // ADC Conversion for sampling voltages
    //  - AN15 (for sampling X voltage) is pin RB15
    //  - AN9 (for sampling Y voltage) is pin RB9
    
    // disable ADC
    CLEARBIT(AD1CON1bits.ADON);
    
    //initialize PIN
    SETBIT(TRISBbits.TRISB15); // set TRISE RB15 to input
    SETBIT(TRISBbits.TRISB9); // set TRISE RB9 to input
    CLEARBIT(AD1PCFGLbits.PCFG15); // set AD1 RB15 input pin as analog
    CLEARBIT(AD1PCFGLbits.PCFG9); // set AD1 RB9 input pin as analog
    
    // Configure AD1CON1
    SETBIT(AD1CON1bits.AD12B); // set 10 bit Operation Mode
    AD1CON1bits.FORM = 0; // set integer output
    AD1CON1bits.SSRC = 0x7; // set automatic conversion
    
    //Configure AD1CON3
    CLEARBIT(AD1CON3bits.ADRC); // Select system 12.8 MHz clock source
    AD1CON3bits.SAMC = 0b11111; // sample-to-conversion T_samc is 31*T_ad = 7254
    AD1CON3bits.ADCS = 0x02; // T_ad = 3*T_cy hence T_ad ~= 234 ns (75 ns min)

    //enable ADC
    SETBIT(AD1CON1bits.ADON);
}

void touch_select_dim(uint8_t dimension) {
    if (dimension == X_DIM_TOUCH) {
        selected_dim = X_DIM_TOUCH;
        CLEARBIT(LATEbits.LATE1);
        SETBIT(LATEbits.LATE2);
        SETBIT(LATEbits.LATE3);
    }
    else if (dimension == Y_DIM_TOUCH) {
        selected_dim = Y_DIM_TOUCH;
        SETBIT(LATEbits.LATE1);
        CLEARBIT(LATEbits.LATE2);
        CLEARBIT(LATEbits.LATE3);
    }
}

uint16_t touch_read(void) {
    uint16_t touch_value = 0;
    if (selected_dim == X_DIM_TOUCH) {
        AD1CHS0bits.CH0SA = 0xF; // set ADC to sample AN15 pin
        SETBIT(AD1CON1bits.SAMP); // start the sample
        while(!AD1CON1bits.DONE); // wait for conversion to finish
        CLEARBIT(AD1CON1bits.DONE); // MUST HAVE! clear conversion done bit
        touch_value = ADC1BUF0;
        if (touch_value < TOUCHSCREEN_MIN_X)
        {
            touch_value = TOUCHSCREEN_MIN_X;
        }
        if (touch_value > TOUCHSCREEN_MAX_X)
        {
            touch_value = TOUCHSCREEN_MAX_X;
        }
      }
    
    
    else if (selected_dim == Y_DIM_TOUCH) {
        AD1CHS0bits.CH0SA = 0x9; // set ADC to sample AN9 pin
        SETBIT(AD1CON1bits.SAMP); // start the sample
        while(!AD1CON1bits.DONE); // wait for conversion to finish
        CLEARBIT(AD1CON1bits.DONE); // MUST HAVE! clear conversion done bit
        touch_value = ADC1BUF0;
        if (touch_value < TOUCHSCREEN_MIN_Y)
        {
            touch_value = TOUCHSCREEN_MIN_Y;
        }
        if (touch_value > TOUCHSCREEN_MAX_Y)
        {
            touch_value = TOUCHSCREEN_MAX_Y;
        }
    }
    return touch_value;
}
