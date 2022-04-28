#include "motor.h"
#include <p33Fxxxx.h>

void motor_init() {
    // Initialize I/O sampling interrupt (every 20ms) on Timer2
    CLEARBIT(T2CONbits.TON); // Disable timer
    CLEARBIT(T2CONbits.TCS); // Use internal 12.8 MHz clock
    CLEARBIT(T2CONbits.TGATE); // Disable gated timer mode
    TMR2 = 0x00; // Clear timer register
    T2CONbits.TCKPS = 0b10; // 1:64 prescaler
    PR2 = 4000; // Period = 20ms
    //IPC1bits.T2IP = 0x02; // Interrupt priority level
    CLEARBIT(IFS0bits.T2IF); // Clear interrupt Flag
    CLEARBIT(IEC0bits.T2IE); // Enable interrupt
    
    CLEARBIT(TRISDbits.TRISD7); //Set OC8 as output
    OC8R = 3700; //initial duty cycle = 1.5ms,
    OC8RS = 3700; //next pwm duty cycle = 1.5ms
    OC8CON = 0x0006;
    
    CLEARBIT(TRISDbits.TRISD6); //Set OC7 as output
    OC7R = 3700; //initial duty cycle = 1.5ms,
    OC7RS = 3700; //next pwm duty cycle = 1.5ms
    OC7CON = 0x0006;
    SETBIT(T2CONbits.TON);
}

void motor_set_duty(uint8_t chan, uint16_t duty_us) {
    // convert duty_us to # of ticks for the output compare
    // note, the logic is inverted
    if (duty_us < MIN_MOTOR_DUTY)
    {
        duty_us = MIN_MOTOR_DUTY;
    }
    else if (duty_us > MAX_MOTOR_DUTY)
    {
        duty_us = MAX_MOTOR_DUTY;
    }
    // convert to timer ticks (timer is 20ms)
    uint16_t ticks = (uint16_t)(4000 - (duty_us * 0.2));
    
    CLEARBIT(T2CONbits.TON); // Stop timer
    if (chan == Y_DIM_MOTOR)
    {
        OC7RS = ticks;
    }
    else if (chan == X_DIM_MOTOR)
    {
        OC8RS = ticks;
    }
    SETBIT(T2CONbits.TON);
}
