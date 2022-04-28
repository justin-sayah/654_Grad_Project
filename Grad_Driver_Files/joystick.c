#include "joystick.h"

uint8_t selected_dim_joystick = X_DIM_JOYSTICK;

void joystick_init(void) {
    // Configuration pins for joystick
    
    // ADC Conversion for sampling voltages
    //  - AN4 (for sampling X voltage) is pin RB4
    //  - AN5 (for sampling Y voltage) is pin RB5
    
    // disable ADC
    CLEARBIT(AD2CON1bits.ADON);
    
    //initialize PIN
    SETBIT(TRISBbits.TRISB4); // set TRISE RB4 to input
    SETBIT(TRISBbits.TRISB5); // set TRISE RB5 to input
    CLEARBIT(AD2PCFGLbits.PCFG4); // set AD2 RB4 input pin as analog
    CLEARBIT(AD2PCFGLbits.PCFG5); // set AD2 RB5 input pin as analog
    
    // Configure AD2CON1
    CLEARBIT(AD2CON1bits.AD12B); // set 10 bit Operation Mode
    AD2CON1bits.FORM = 0; // set integer output
    AD2CON1bits.SSRC = 0x7; // set automatic conversion
    
    //Configure AD2CON3
    CLEARBIT(AD2CON3bits.ADRC); // Select system 12.8 MHz clock source
    AD2CON3bits.SAMC = 0b11111; // sample-to-conversion T_samc is 31*T_ad = 7254
    AD2CON3bits.ADCS = 0x02; // T_ad = 3*T_cy hence T_ad ~= 234 ns (75 ns min)

    //enable ADC
    SETBIT(AD2CON1bits.ADON);
}

void joystick_selected_dim(uint8_t dimension) {
    if (dimension == X_DIM_JOYSTICK) {
        selected_dim_joystick = X_DIM_JOYSTICK;
    }
    else if (dimension == Y_DIM_JOYSTICK) {
        selected_dim_joystick = Y_DIM_JOYSTICK;
    }
}

uint16_t joystick_read(void) {
    uint16_t joystick_value = 0;
    if (selected_dim_joystick == X_DIM_JOYSTICK) {
        AD2CHS0bits.CH0SA = 0x4; // set ADC to sample AN4 pin
        SETBIT(AD2CON1bits.SAMP); // start the sample
        while(!AD2CON1bits.DONE); // wait for conversion to finish
        CLEARBIT(AD2CON1bits.DONE); // MUST HAVE! clear conversion done bit
        joystick_value = ADC2BUF0;
    }
    
    else if (selected_dim_joystick == Y_DIM_JOYSTICK) {
        AD2CHS0bits.CH0SA = 0x5; // set ADC to sample AN5 pin
        SETBIT(AD2CON1bits.SAMP); // start the sample
        while(!AD2CON1bits.DONE); // wait for conversion to finish
        CLEARBIT(AD2CON1bits.DONE); // MUST HAVE! clear conversion done bit
        joystick_value = ADC2BUF0;
    }
    return joystick_value;
}
