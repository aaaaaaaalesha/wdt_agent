// Copyright 2022 Alexandrov Alexey (IU8-74)
#include <main.h>
#include <ctype.h>

const char HEARTBEAT = 'h';
int timeout_error = 0;

char recieved = 0;
char second = 0;
unsigned int wdt_counter = 0;
unsigned int critical_time = 5; // 3 seconds by default

char timed_getc() {
    long timeout;
    timeout_error=FALSE;
    timeout = 0;
    while (!kbhit() && (++timeout < 50000)) // 1/2 second
      delay_us(10);
   if (kbhit()) {
     return (getc());
   } else {
     timeout_error=TRUE;
     return (0);
 }
}


unsigned int try_cast_integer(char first, char second) {
    if (isdigit((unsigned char)first) == 0) return -1;
    if (isdigit((unsigned char)second) == 0) return -1;
    
    return (first - '0') * 10 + (second - '0');
}

// Handles heartbeats and configuration from wdt_agent.
void UART_handler() {
      unsigned int time = 0;
      recieved = timed_getc();
      if (timeout_error == TRUE) {
       return;
      }
      putc(recieved);
      if (recieved != HEARTBEAT) {
         second = getc();
         putc(' ');
         putc(recieved);
         putc(second);
         putc(' ');
         
         time = try_cast_integer(recieved, second);
         if (time == -1) {
           puts("Îøèáêà!");
           return;
         }
         // Configure critical time from agent.
         critical_time = time;
         return;
      }
      // If heartbeat has been recieved, update wdt.
      wdt_counter = 0;
}

// Activates relay and restarts the system.
void reset() {
    output_high(PIN_D0);
    delay_ms(600);
    output_low(PIN_D0);
}

void main() {
   output_low(PIN_D0);
   // Initial heartbeat for starting process.
   for (getc(); TRUE; ++wdt_counter) {
     if (input(PIN_C7)) {
       UART_handler();
     }
     delay_ms(750);
     if (wdt_counter > critical_time) {
       reset();
       wdt_counter = 0;
       delay_ms(60000); // wait a minute, system restarts...
     }
   }
}
