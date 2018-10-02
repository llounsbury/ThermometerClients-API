# ThermometerClients-API

This package contains three pieces of software and is intended for use with a web enabled thermometer.

1. API: The API is written in python and powered by the FLASK and REQUEST libraries. 
It includes functionality for getting and setting: temperature data, max and min alert
temperatures, phone number, and LED status. Functionality is also included to send 
SMS messages if temperatures exceed the set range. For optimal performance post temperture 
reading from thermometer at < 1 sec intervals (POST /temp/:temp). To enable display on/off
functionality, have the thermometer (GET /LED). Value of 0 is off, 1 is on.

2. Graph: The graph is also written in python and is powered by the MATPLOTLIB library.
The graph scrolls from right to left, displaying the last 300 seconds of temperature data
in degrees C. The range of the graph is 10-50 degrees C.

3. WebApp: The web app is written in typescript and powered by angular 6. The web app has
basic functionality to interact with the API and allow the user to view and update values.
Values are updated each second, settings changed by other users (eg max min temp, phone #)
are also updated across all users of the app. 
