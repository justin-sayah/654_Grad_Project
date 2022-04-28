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

// Primary (XT, HS, EC) Oscillator without PLL
_FOSCSEL(FNOSC_PRIPLL);
// OSC2 Pin Function: OSC2 is Clock Output - Primary Oscillator Mode: XT Crystanl
_FOSC(OSCIOFNC_ON & POSCMD_XT);
// Watchdog Timer Enabled/disabled by user software
_FWDT(FWDTEN_OFF);
// Disable Code Protection
_FGS(GCP_OFF);   

//Define global vars
uint8_t nextTouch = Y_DIM_TOUCH;
uint8_t dimReadLast = Y_DIM_TOUCH;

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
 * 1) Read data waiting in buffer
 * 
 * 2) Poll ball position
 * 
 * 3) Change touch board dimension
 * 
 * 4) Set new motor duty
 * 
 * 5) Send position data back to server
 * 
 */
void __attribute__((__interrupt__)) _U2RXInterrupt(void){
    //lcd_locate(0,1);
    //lcd_printf("interrupt triggered")
    
    lcd_clear();
    lcd_locate(0, 0);
    lcd_printf("-- Grad Project --");
    
    //1) Read data waiting in buffer
    uint8_t data = 0;
    
    //wait for start bit
    while(U2STAbits.URXDA == 0);
    uart2_recv(&data);
    
    // wait for dimension, receive it
    //x = 0x0, y = 0x1
    uint8_t incoming_dim = 0;  
    while(U2STAbits.URXDA == 0);
    uart2_recv(&data);
    incoming_dim = data;
    
    lcd_locate(0, 1);
    lcd_printf("Dimension: %d", incoming_dim);
        
    //wait for low bits of motor duty in microseconds
    uint8_t motor_low = 0;
    while(U2STAbits.URXDA == 0);
    uart2_recv(&data);
    motor_low = data;
    
    //wait for high bits of motor duty in microseconds
    uint8_t motor_high = 0;
    while(U2STAbits.URXDA == 0);
    uart2_recv(&data);
    motor_high = data;
        
    uint16_t incoming_duty = (motor_low << 8) | motor_high;
        
    lcd_locate(0, 2);
    lcd_printf("Duty Rec: %d", incoming_duty)
    
    //TEMP FOR DRIVER
    //uart2_send_8(MSG_ACK);
    
    // 2) Poll ball position, 3) Change Dimension
    uint16_t lastPos = 0;
    //lastPos holds the most recent position read
    //dimReadLast holds the dimension of the last read
    //nextTouch preps the next dimension to read on next interrupt
    lastPos = touch_read(); 
    if(nextTouch == X_DIM_TOUCH){
        touch_select_dim(Y_DIM_TOUCH);
        nextTouch = Y_DIM_TOUCH;
        dimReadLast = X_DIM_TOUCH;
    }
    else{
        touch_select_dim(X_DIM_TOUCH);
        nextTouch = X_DIM_TOUCH;
        dimReadLast = Y_DIM_TOUCH;
    }
    
    //4) Set new motor duty
    motor_set_duty(incoming_dim, (uint16_t)incoming_duty);
    
    //5) Send position data back to server
    //TBD
    
//    // wait for size of the message
//    uint8_t message_N = 0;
//    while(U2STAbits.URXDA == 0);
//    uart2_recv(&data);
//    message_N = data;
//    if (message_N >= MSG_BYTES_MSG)
//    {
//        uart2_send_8(MSG_NACK);
//    }
        
//    //wait for body of the message
//    uint16_t crc = 0;
//    uint8_t i;
//    for (i = 0; i < message_N; i++)
//    {
//        while(U2STAbits.URXDA == 0);
//        uart2_recv(&data);
//        crc = crc_update(crc, data);
//        lcd_locate(i, 3);
//        lcd_printf("%c", data);
//    }
//     
//    // if crc is the same, send ACK
//        
//    if (message_crc == crc)
//    {
//        uart2_send_8(MSG_ACK);
//    }
    
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


