/****************************************************/
/*                                                  */
/*   CS-454/654 Embedded Systems Development        */
/*   Instructor: Renato Mancuso <rmancuso@bu.edu>   */
/*   Boston University                              */
/*                                                  */
/*   Description: template file to implement basic  */
/*                macros and functions to interface */
/*                with the analog joystick.         */
/*                                                  */
/****************************************************/

#ifndef __JOYSTICK_H
#define __JOYSTICK_H

#include <p33Fxxxx.h>
#include "types.h"

#ifndef X_DIM_JOYSTICK
#define X_DIM_JOYSTICK 0x00
#endif

#ifndef Y_DIM_JOYSTICK
#define Y_DIM_JOYSTICK 0x01
#endif

void joystick_init(void);

void joystick_selected_dim(uint8_t dimension);

uint16_t joystick_read(void);

#endif /* __JOYSTICK_H */


