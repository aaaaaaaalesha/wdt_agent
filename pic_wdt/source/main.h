// Copyright 2022 Alexandrov Alexey (IU8-74)
#include <18F46K22.h>
#device ADC=10

#FUSES NOWDT //No Watch Dog Timer
#use delay(crystal=8MHz,restart_wdt)
#use FIXED_IO(D_outputs=PIN_D0)

#use rs232(baud=9600, xmit=PIN_C6, rcv=PIN_C7, bits=8, parity=N)
