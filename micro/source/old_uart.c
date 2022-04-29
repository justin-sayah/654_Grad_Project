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

// Primary (XT, HS, EC) Oscillator without PLL
_FOSCSEL(FNOSC_PRIPLL);
// OSC2 Pin Function: OSC2 is Clock Output - Primary Oscillator Mode: XT Crystanl
_FOSC(OSCIOFNC_ON & POSCMD_XT);
// Watchdog Timer Enabled/disabled by user software
_FWDT(FWDTEN_OFF);
// Disable Code Protection
_FGS(GCP_OFF);   

int recv_fail = 0;
int timeout = 0;

void __attribute__((__interrupt__)) _T1Interrupt(void){
    //assume troll has corrupted msg len
    uart2_send_8(MSG_NACK);
    recv_fail += 1;
    timeout = 1;
    CLEARBIT(IFS0bits.T1IF);
}

int main(void)
{
    uart2_init(BAUD_9600);
    
    /* LCD Initialization Sequence */
	__C30_UART=1;	
	lcd_initialize();
	lcd_clear();
    
    // Print screen header
    lcd_locate(0, 0);
    lcd_printf("-- Lab 3 (RM v2.5) --");
    
    //init timer 1 for 1s interrupts
    __builtin_write_OSCCONL (OSCCONL | 2);
    T1CONbits.TON = 0;
    T1CONbits.TCS = 1;
    T1CONbits.TSYNC = 0;
    T1CONbits.TCKPS = 0b11;
    TMR1 = 0x00;
    PR1 = 128;
    IPC0bits.T1IP = 0x01;
    IFS0bits.T1IF = 0;
    IEC0bits.T1IE = 1;
    //DO NOT TURN ON TIMER HERE, TURN ON IN LOOP
    
    while(1)
    {
        lcd_locate(0, 1);
        lcd_printf("Recv fail: %d times", recv_fail);
        
        uint8_t data = 0;
        
        // wait for start of the message
        while(U2STAbits.URXDA == 0);
     
        uart2_recv(&data);
        if(data != MSG_START)
        {
            continue;
        }  
        //turn on the timeout timer
        T1CONbits.TON = 1;
        TMR1 = 0x0;
        timeout = 0;
        
        
        // wait for crc of the message
        uint8_t message_crc_1 = 0;        
        while(U2STAbits.URXDA == 0)
        {
            if (timeout == 1)
            {
                goto timerjump;
            }
        };
        uart2_recv(&data);
        message_crc_1 = data;
        
        uint8_t message_crc_2 = 0;        
        while(U2STAbits.URXDA == 0){
        if (timeout == 1)
        {
            goto timerjump;
        }
        };
        uart2_recv(&data);
        message_crc_2 = data;
        
        uint16_t message_crc = (message_crc_1 << 8) | message_crc_2;
        
        lcd_locate(0, 2);
        lcd_printf("CRC: 0x%x", message_crc)
        
        // wait for size of the message
        uint8_t message_N = 0;
        while(U2STAbits.URXDA == 0){
        if (timeout == 1)
        {
            goto timerjump;
        }
        };
        uart2_recv(&data);
        message_N = data;
        if (message_N >= MSG_BYTES_MSG)
        {
            uart2_send_8(MSG_NACK);
            recv_fail += 1;
            continue;
        }
        
        // wait for body of the message
        uint16_t crc = 0;
        uint8_t i;
        for (i = 0; i < message_N; i++)
        {
            while(U2STAbits.URXDA == 0){
            if (timeout == 1)
            {
                goto timerjump;
            }
            };
            uart2_recv(&data);
            crc = crc_update(crc, data);
            lcd_locate(i, 3);
            lcd_printf("%c", data);
        }
        
        //assume we have received the whole message and turn off timer
        T1CONbits.TON = 0;
     
        // if crc is the same, send ACK
        
        if (message_crc == crc)
        {
            uart2_send_8(MSG_ACK);
        }
        
        // if crc is not the same, send NACK
        else
        {
            recv_fail += 1;
            uart2_send_8(MSG_NACK);
        }
        
        timerjump:
            if (timeout == 1){
                timeout = 0;
                T1CONbits.TON = 0;
                TMR1 = 0x0;
            }
    }
}	

