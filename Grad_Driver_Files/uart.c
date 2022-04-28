/****************************************************/
/*                                                  */
/*   CS-454/654 Embedded Systems Development        */
/*   Instructor: Renato Mancuso <rmancuso@bu.edu>   */
/*   Boston University                              */
/*                                                  */
/*   Description: lab3 UART2 init,TX,RX functions   */
/*                                                  */
/****************************************************/

#include "uart.h"

inline void uart2_init(uint16_t baud)
{
	/* Implement me please. */
    
    // Stop UART port
    CLEARBIT(U2MODEbits.UARTEN); // Disable UART for configuration
    
    // Set IO pins
    TRISFbits.TRISF4 = 1; // Set UART2 RX pin as input
    TRISFbits.TRISF5 = 0; // Set UART2 TX pin as output
    
    // Baud rate
    U2MODEbits.BRGH = 0; // Set low speed baud rate
    U2BRG = (uint32_t)800000 / baud - 1; // Set the baudrate
    
    // Operation settings and start port
    U2MODE = 0; // 8-bit, no parity, and 1 stop bit
    U2MODEbits.RTSMD = 0; // Select simplex mode
    U2MODEbits.UEN = 0; // Select simplex mode
    U2MODE |= 0x00;
    
    U2STAbits.URXISEL0 = 0; //set interrupt size
    IPC7bits.U2RXIP = 1; //set priority (7 = max)
    U2STAbits.URXISEL = 0; //set interrupt mode (1 char guaranteed)
            
    // Enable Interrupts
    IEC1bits.U2RXIE = 1;
    IEC1bits.U2TXIE = 0;
    
    // Clear interrupt flag bits
    IFS1bits.U2RXIF = 0;
    IFS1bits.U2TXIF = 0;
    
    U2MODEbits.UARTEN = 1; // Enable UART
    U2STA = 0; //zero out control register
    U2STAbits.UTXEN = 1; // Enable UART TX
    
    
}

void uart2_send_8(int8_t data)
{
	/* Implement me please. */
    while (U2STAbits.UTXBF);
    U2TXREG = data;
    while (!U2STAbits.TRMT);
}

int8_t uart2_recv(uint8_t* data)
{
	/* Implement me please. */
    if (U2STAbits.OERR)
    {
        U2STAbits.OERR = 0;
    }
    if (U2STAbits.URXDA)
    {
        *data = U2RXREG & 0x00FF;
        return 0;
    }
    return -1;
}
