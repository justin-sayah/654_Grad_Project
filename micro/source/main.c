//do not change the order of the following 3 definitions
#define FCY 12800000UL 
#include <stdio.h>
#include <libpic30.h>

#include <p33Fxxxx.h>
#include "types.h"
#include "uart.h"
#include "crc16.h"
#include "lab3.h"
#include "lcd.h"
#include "timer.h"
#include "touch.h"
#include "motor.h"
#include "sort.h"

// Primary (XT, HS, EC) Oscillator without PLL
_FOSCSEL(FNOSC_PRIPLL);
// OSC2 Pin Function: OSC2 is Clock Output - Primary Oscillator Mode: XT Crystanl
_FOSC(OSCIOFNC_ON & POSCMD_XT);
// Watchdog Timer Enabled/disabled by user software
_FWDT(FWDTEN_OFF);
// Disable Code Protection
_FGS(GCP_OFF);   

//Define global vars
uint8_t nextTouch = TOUCH_READ_Y;
uint8_t dimReadLast = TOUCH_READ_Y;

/*
 * Interrupt = control cycle (every 10 ms)
 * 
 * Data Format: 1 byte chunks as smallest units (lab 3)
 * start byte = 1
 * dimension byte: 0 = x, 1 = y
 * 1st data byte: low bytes for dimension duty (us)
 * 2nd data byte: high bytes for dimension duty (us)
 * stop word (unnecessary?): 1 for stop
 * 
 * 1) Read message (motor command)
 * 
 * 2) Perform motor command
 * 
 * 3) Sample ball position
 * 
 * 4) Change touch board dimension
 * 
 * 5) Send message (ball position)
 * 
 */
void __attribute__((__interrupt__)) _U2RXInterrupt(void){
    ///////////////////////////
    ///// 1. Read message /////
    ///////////////////////////

    // Read start bit
    uint8_t startBit = 0;
    while(U2STAbits.URXDA == 0);
    uart2_recv(&startBit);
    
    // Read dimension (x = 0x0, y = 0x1)
    uint8_t dimension = 0;  
    while(U2STAbits.URXDA == 0);
    uart2_recv(&dimension);
    
    lcd_locate(0, 1);
    lcd_printf("Dimension: %d", dimension);
        
    // Read motor duty (microseconds)
    uint8_t dutyLowBits = 0;
    while(U2STAbits.URXDA == 0);
    uart2_recv(&dutyLowBits);
    
    uint8_t dutyHighBits = 0;
    while(U2STAbits.URXDA == 0);
    uart2_recv(&dutyHighBits);
        
    uint16_t duty = (dutyLowBits << 8) | dutyHighBits;
        
    lcd_locate(0, 2);
    lcd_printf("Duty: %d", duty);
    
    ////////////////////////////////////
    ///// 2. Perform motor command /////
    ////////////////////////////////////

    motor_set_duty(dimension, (uint16_t)duty);

    ///////////////////////////////////
    ///// 3. Sample ball position /////
    ///////////////////////////////////

    // Sample numPositionsSampled raw positions
    uint8_t numPositionsSampled = 5;
    uint16_t positions[numPositionsSampled];
    uint8_t i;
    for (i = 0; i < numPositionsSampled; i++)
    {
        positions[i] = touch_read();
    }

    // Sort raw positions
    selection_sort(&positions, numPositionsSampled);

    // Use median of raw positions as position value
    uint16_t position = positions[numPositionsSampled / 2];

    ///////////////////////////////////////////
    ///// 4. Change touch board dimension /////
    ///////////////////////////////////////////
    
    if(nextTouch == TOUCH_READ_X)
    {
        touch_select_dim(TOUCH_READ_Y);
        nextTouch = TOUCH_READ_Y;
        dimReadLast = TOUCH_READ_X;
    }
    else
    {
        touch_select_dim(TOUCH_READ_X);
        nextTouch = TOUCH_READ_X;
        dimReadLast = TOUCH_READ_Y;
    }

    ///////////////////////////
    ///// 5. Send message /////
    ///////////////////////////

    uint8_t positionLowBits = (position >> 8) & 0xFF;
    uint8_t positionHighBits = position && 0xFF;
    
    uart2_send_8(positionLowBits);
    uart2_send_8(positionLowBits);
    
    U2RXREG = 0;
    CLEARBIT(IFS1bits.U2RXIF);
}


int main(void){
    
    //Initialze UART
    uart2_init(BAUD_9600);
    
    // Initialize motors
    motor_init();
    
    // Initialize touchscreen
    touch_init();
    
    /* LCD Initialization Sequence */
	__C30_UART=1;	
	lcd_initialize();
	lcd_clear();
    
    // Print screen header
    lcd_locate(0, 0);
    lcd_printf("-- Grad Project --");
    
    while(1);
}


