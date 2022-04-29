/****************************************************/
/*                                                  */
/*   CS-454/654 Embedded Systems Development        */
/*   Instructor: Renato Mancuso <rmancuso@bu.edu>   */
/*   Boston University                              */
/*                                                  */
/*   Description: Lab 5                             */
/*                                                  */
/*                                                  */
/****************************************************/

#include <p33Fxxxx.h>
//do not change the order of the following 3 definitions
#define FCY 12800000UL 
#include <stdio.h>
#include <stdlib.h>
#include <libpic30.h>
#include <uart.h>

#include "types.h"
#include "led.h"
#include "lcd.h"
#include "motor.h"
#include "touch.h"

/* Initial configuration by EE */
// Primary (XT, HS, EC) Oscillator with PLL
_FOSCSEL(FNOSC_PRIPLL);

// OSC2 Pin Function: OSC2 is Clock Output - Primary Oscillator Mode: XT Crystal
_FOSC(OSCIOFNC_OFF & POSCMD_XT); 

// Watchdog Timer Enabled/disabled by user software
_FWDT(FWDTEN_OFF);

// Disable Code Protection
_FGS(GCP_OFF);  

//////////////////////////////////
//////// Butterworth code ////////
//////////////////////////////////
#ifndef BUTTERWORTH_X
#define BUTTERWORTH_X 0x00
#endif

#ifndef BUTTERWORTH_Y
#define BUTTERWORTH_Y 0x01
#endif

// MATLAB code:
//  fs = 50 % 50Hz based on timer interrupt frequency
//  fc = 2 % want cutoff of 2Hz
//  fc_perc = fc*2/fs % cutoff as percentage of Nyquist rate
//  N = 2 % want 2nd order Butterworth filter
//  [b, a] = butter(N, fc_perc) % coefficients
float b[3] = {0.0134,0.0267,0.0134};
float a[2] = {-1.647,0.701};

// previous 3 raw samples
uint16_t xRaw[3] = {0, 0, 0};
uint16_t yRaw[3] = {0, 0, 0};

// previous 2 filtered samples
uint16_t xFilter[2] = {0, 0};
uint16_t yFilter[2] = {0, 0};

float butterworth(uint16_t direction, uint16_t sampleRaw) 
{
    float sampleFilter = 0;

    if (direction == BUTTERWORTH_X)
    {
        // add raw sample to saved raw samples
        xRaw[2] = xRaw[1];
        xRaw[1] = xRaw[0];
        xRaw[0] = sampleRaw;
        
        // calculate filtered sample
        sampleFilter = (b[0] * xRaw[0]) + (b[1] * xRaw[1]) + (b[2] * xRaw[2])
                - (a[0] * xFilter[0]) - (a[1] * xFilter[1]);
        
        // add filtered sample to saved filtered samples
        xFilter[1] = xFilter[0];
        xFilter[0] = sampleFilter;
    }
    else if (direction == BUTTERWORTH_Y)
    {
        // add raw sample to saved raw samples
        yRaw[2] = yRaw[1];
        yRaw[1] = yRaw[0];
        yRaw[0] = sampleRaw;
        
        // calculate filtered sample
        sampleFilter = (b[0] * yRaw[0]) + (b[1] * yRaw[1]) + (b[2] * yRaw[2])
                - (a[0] * yFilter[0]) - (a[1] * yFilter[1]);
        
        // add filtered sample to saved filtered samples
        yFilter[1] = yFilter[0];
        yFilter[0] = sampleFilter;
    }
    return sampleFilter;
}
//////////////////////////////////


////////////////////////////////
//////// Task variables ////////
////////////////////////////////
#define TASK_X_AXIS 0 // balance ball along x axis (setting y to min)
#define TASK_Y_AXIS 1 // balance ball along y axis (setting x to min)
#define TASK_BOTH_AXES 2 // balance ball on both axes

uint8_t task = TASK_BOTH_AXES;
////////////////////////////////


///////////////////////////////
//////// PID variables ////////
///////////////////////////////
#ifndef PID_X
#define PID_X 0x00
#endif

#ifndef PID_Y
#define PID_Y 0x01
#endif

// NOTE: delta_t not used in PID equations and should be accounted for in values of Ki and Kd
//      if we want to use delta_t, add a variable here

// Single side
float x_Kp_single = 0.0017;
float x_Ki_single = 0.000013;
float x_Kd_single = 0.0013;

float y_Kp_single = 0.0015;
float y_Ki_single = 0.00001;
float y_Kd_single = 0.0016;

//float x_Kp = 0.0012;
//float x_Ki = 0.00001;
//float x_Kd = 0.049;
//
//float y_Kp = 0.0004;
//float y_Ki = 0.00003;
//float y_Kd = 0.043;

float x_Kp = .0003;//0.0008;
float x_Ki = 0.000001;
float x_Kd = 0.007;//.09;

float y_Kp = 0.000002;//0.0005;
float y_Ki = 0.00000008; 
float y_Kd = 0.005;//0.09;

// set points
uint16_t x_bar = 0;
uint16_t y_bar = 0;

// previous errors (for derivative calculations)
float x_errorPrev = 0;
float y_errorPrev = 0;

// sum of all previous errors (for integral calculation)
float x_errorSum = 0;
float y_errorSum = 0;

float pid(uint16_t direction, uint16_t sample)
{
    float result;
    
    float error = 0;
    float errorDelta = 0;
    float errorSum = 0;
    
    float Kp = 0;
    float Ki = 0;
    float Kd = 0;
    
    if (direction == PID_X)
    {
        error = (float)sample - x_bar;
        errorDelta = error - x_errorPrev;
        x_errorPrev = error;
        x_errorSum += error;
        errorSum = x_errorSum;
        
        if (task == TASK_X_AXIS)
        {
            Kp = x_Kp_single;
            Ki = x_Ki_single;
            Kd = x_Kd_single;
        }
        else if (task == TASK_BOTH_AXES)
        {
            Kp = x_Kp;
            Ki = x_Ki;
            Kd = x_Kd;
        }
        
    }
    
    else if (direction == PID_Y)
    {
        error = (float)sample - y_bar;
        errorDelta = error - y_errorPrev;
        y_errorPrev=error;
        y_errorSum += error;
        errorSum = y_errorSum;
        
        if (task == TASK_Y_AXIS)
        {
            Kp = y_Kp_single;
            Ki = y_Ki_single;
            Kd = y_Kd_single;
        }
        else if (task == TASK_BOTH_AXES)
        {
            Kp = y_Kp;
            Ki = y_Ki;
            Kd = y_Kd;
        }
    }

    result = (-Kp * error) - (Kd * errorDelta) - (Ki * errorSum);
    result *= MAX_MOTOR_ANGLE;
    
    return result;
}
///////////////////////////////

uint16_t xRawNew = 0;
uint16_t yRawNew = 0;
float xAngle = 0;
float yAngle = 0;
float xDuty = 0;
float yDuty = 0;
float xFilterNew = 0;
float yFilterNew = 0;
uint16_t i = 0;
uint8_t nextTouch= X_DIM_TOUCH;
uint8_t do_x_pid = 0;
uint8_t do_y_pid = 0;
uint8_t yskipped = 0;
uint8_t xskipped = 0;

void __attribute__((__interrupt__, no_auto_psv)) _T1Interrupt(void)
{
    //if y was last sampled, sample x then switch dimensions
    //if x was last sampled, sample y then switch dimensions
    
    if(nextTouch == X_DIM_TOUCH){
        xRawNew = touch_read();
        //do multiple sampling and throw out outliers
        //xFilter[0] is last filtered sample
        
//        while((xRawNew - xFilter[0] > 100 || xRawNew - xFilter[0] < -100) && xskipped < 5){
//            xRawNew = touch_read();
//            xskipped++;
//            //xRawNew = xFilter[0];
//        }
//        xskipped = 0;
        
//        if (do_x_pid) {
//            while(1);
//        }
        
        do_x_pid = 1;
        touch_select_dim(Y_DIM_TOUCH);
        nextTouch = Y_DIM_TOUCH;
    }
    else{
        yRawNew = touch_read();
        //do multiple sampling and throw out outliers
        //xFilter[1] is last filtered sample
        
//        if((yRawNew - yFilter[0] > 100 || yRawNew - yFilter[0] < -100) && (yskipped < 2)){
//            yRawNew = yFilter[0];
//            yskipped++;
//        } else {
//            yskipped = 0;
//        }
        
//        while((yRawNew - yFilter[0] > 100 || yRawNew - yFilter[0] < -100) && yskipped < 5){
//            yRawNew = touch_read();
//            yskipped++;
//            //xRawNew = xFilter[0];
//        }
//        yskipped=0;
        
//        if (do_y_pid) {
//            while(1);
//        }
        
        do_y_pid = 1;
        touch_select_dim(X_DIM_TOUCH);
        nextTouch = X_DIM_TOUCH;
    }
    
    CLEARBIT(IFS0bits.T1IF);
}

int main(){
    /* LCD Initialization Sequence */
	__C30_UART=1;	
	lcd_initialize();
	lcd_clear();
	
    lcd_locate(0,0);
    lcd_printf("--- Lab 07 ---")
    
    // Initialize motors
    motor_init();
    
    // Initialize touchscreen
    touch_init();
        
    // Initialize timer interrupt (20ms) for I/O and motor
    CLEARBIT(T1CONbits.TON); // Disable timer
    CLEARBIT(T1CONbits.TCS); // Use internal 12.8 MHz clock
    CLEARBIT(T1CONbits.TGATE); // Disable gated timer mode
    TMR1 = 0x00; // Clear timer register
    T1CONbits.TCKPS = 0b11; // 1:256 prescaler
    PR1 = 500; // Period: (x * 256) / 12.8MHz = 0.01s => x = 500
    IPC0bits.T1IP = 0x01; // Interrupt priority level
    CLEARBIT(IFS0bits.T1IF); // Clear interrupt Flag
    SETBIT(IEC0bits.T1IE); // Enable interrupt
    
//    // initialize setpoint and orientation
//    if (task == TASK_X_AXIS)
//    {
//        motor_set_duty(Y_DIM_MOTOR, MAX_MOTOR_DUTY);
//        x_bar = TOUCHSCREEN_MID_X;
//        y_bar = TOUCHSCREEN_MAX_Y;
//    }
//    else if (task == TASK_Y_AXIS)
//    {
//        motor_set_duty(X_DIM_MOTOR, MAX_MOTOR_DUTY);
//        x_bar = TOUCHSCREEN_MAX_X;
//        y_bar = TOUCHSCREEN_MID_Y;
//    }
//    else if (task == TASK_BOTH_AXES)
//    {
//        x_bar = TOUCHSCREEN_MID_X;
//        y_bar = TOUCHSCREEN_MID_Y;
//    }

    x_bar = TOUCHSCREEN_MID_X;
    y_bar = TOUCHSCREEN_MID_Y;
    
    SETBIT(T1CONbits.TON); // Start timer
    
    lcd_locate(0,1);
    lcd_printf("X Y");
    lcd_locate(0,2);
    lcd_printf("Kp %.2e %.2e", x_Kp, y_Kp);
    lcd_locate(0,3);
    lcd_printf("Ki %.2e %.2e", x_Ki, y_Ki);
    lcd_locate(0,4);
    lcd_printf("Kd %.2e %.2e", x_Kd, y_Kd);
    lcd_locate(0,5);
    lcd_printf("Setpoint: (%d, %d)", x_bar, y_bar);
    while(1){
        
        if (i == 20)
        {
            lcd_clear();
            lcd_locate(0,6);
            lcd_printf("Current: (%d, %d)", xFilter[0], yFilter[0]);
            lcd_locate(0,7);
            lcd_printf("Raw: (%d, %d)", xRawNew, yRawNew);
        }
        i += 1;

        // Butterworth filter to get filtered values
        
        

        // PID control
        if (do_x_pid) {
            xFilterNew = butterworth(BUTTERWORTH_X, xRawNew);
            xAngle = pid(PID_X, xFilterNew);
            do_x_pid = 0;
            xDuty = (1200 / 180) * (xAngle + 90) + 900;
            motor_set_duty(X_DIM_MOTOR, (uint16_t)xDuty);
        } 
        
        if (do_y_pid) {
            yFilterNew = butterworth(BUTTERWORTH_Y, yRawNew);
            yAngle = pid(PID_Y, yFilterNew);
         
                    // convert angle to duty (us)
        // duty_us = ((2100 - 900) / (90 - -90)(angle - -90) + 90
            
            yDuty = (1200 / 180) * (yAngle + 90) + 900;

            
            motor_set_duty(Y_DIM_MOTOR, (uint16_t)yDuty);
            
            do_y_pid = 0;
        }
    }
        
    return 0;
}


