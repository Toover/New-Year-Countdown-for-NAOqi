# New-Year-Countdown-for-NAOqi
A NAOqi Application for announcing the next year from time to time, until the final countdown.

## Packaging from source
Use [Choregraphe](https://developer.softbankrobotics.com/us-en/downloads/pepper "Choregraphe download") to open "choregraphe-project/New Year Countdown.pml".
Use File > Build Application Package... and follow the steps to package it.

## Structure
The application consists in:
* an activity to announce the time left before the next year
* an activity to perform the final countdown for the new year
* an HTML page to display a countdown (for Pepper only)
* a service to track the time before the next year and give the focus to the activities at the right times

## TODO
This is a work in progress, most of the elements are not implemented yet.
