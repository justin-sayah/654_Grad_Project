#ifndef __TOUCH_H__
#define __TOUCH_H__

#include "types.h"

#ifndef X_DIM_TOUCH
#define X_DIM_TOUCH 0x00
#endif

#ifndef Y_DIM_TOUCH
#define Y_DIM_TOUCH 0x01
#endif

#ifndef TOUCHSCREEN_MIN_X
#define TOUCHSCREEN_MIN_X 130 //250
#endif

#ifndef TOUCHSCREEN_MAX_X
#define TOUCHSCREEN_MAX_X 700//2400
#endif

#ifndef TOUCHSCREEN_MIN_Y
#define TOUCHSCREEN_MIN_Y 115//250
#endif

#ifndef TOUCHSCREEN_MAX_Y
#define TOUCHSCREEN_MAX_Y 600//2800
#endif

#ifndef TOUCHSCREEN_MID_X
#define TOUCHSCREEN_MID_X 400//1500
#endif

#ifndef TOUCHSCREEN_MID_Y
#define TOUCHSCREEN_MID_Y 400//1500
#endif

// Perform any necessary initialization for the touchscreen and associated ADC pins.
void touch_init(void);

// Configure pins and associated ADC to sample on either the x- or y-dimension.
void touch_select_dim(uint8_t dimension);

// Acquire a position sample from the touchscreen on the dimension selected with the previous touch_select_dim(...) command.
uint16_t touch_read(void);

#endif //__TOUCH_H__
