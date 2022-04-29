#ifndef __MOTOR_H__
#define __MOTOR_H__
#include "types.h"

#ifndef X_DIM_MOTOR
#define X_DIM_MOTOR 0x00
#endif

#ifndef Y_DIM_MOTOR
#define Y_DIM_MOTOR 0x01
#endif

#ifndef MIN_MOTOR_DUTY // 900us = 0.9ms
#define MIN_MOTOR_DUTY 900
#endif

#ifndef MAX_MOTOR_DUTY // 2100us = 2.1ms
#define MAX_MOTOR_DUTY 2100
#endif

#ifndef MID_MOTOR_DUTY // 1500us = 1.5ms
#define MID_MOTOR_DUTY 1500
#endif

#ifndef MIN_MOTOR_ANGLE
#define MIN_MOTOR_ANGLE -90
#endif

#ifndef MAX_MOTOR_ANGLE
#define MAX_MOTOR_ANGLE 90
#endif

// Perform any necessary initialization of the specified motor channel.
// Use Timer2 for the duty cycle.
void motor_init();

// Set the duty cycle of the specified motor channel using the provided duty in microseconds.
// Use Timer2 for the duty cycle.
void motor_set_duty(uint8_t chan, uint16_t duty_us);

#endif //__MOTOR_H__
