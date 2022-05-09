#include "sort.h"

void selection_sort(uint16_t * list[], uint8_t length)
{
    uint8_t i;
    for (i = 0; i < length - 1; i++)
    {
        uint16_t j;
        uint16_t jMin = i;
        /* test against elements after i to find the smallest */
        for (j = i + 1; j < length; j++)
        {
            if (list[j] < list[jMin])
            {
                jMin = j;
            }
        }

        if (jMin != i) 
        {
            uint16_t temp = list[j];
            list[j] = list[jMin];
            list[jMin] = temp;
        }
    }
}
