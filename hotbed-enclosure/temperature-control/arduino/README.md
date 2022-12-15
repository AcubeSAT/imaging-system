To use the DHT sensor(s), you'll need two extra libraries.
The libraries are in zip form.
You need the [DHT sensor library](https://github.com/adafruit/DHT-sensor-library/archive/refs/tags/1.4.4.zip) and the [Adafruit Unified Sensor Driver library](https://github.com/adafruit/Adafruit_Sensor/archive/refs/tags/1.1.6.zip).
Then, open Arduino IDE and go to `Sketch` -> `Include lbrary` -> `Add .ZIP Library...`.
When programming the Arduino, you'll have to configure the board, processor and port.
If you're on Windows, to see the port to which the Arduino is connected, press `Win` + `R`, type `devmgmt.msc` to open the Device Manager.
Then, go to `View` -> `Show hidden devices`.
You'll find it in the `Ports (COM & LPT)` section.
The board is the `Arduino Nano`, and the processor is the `ATmega328P (Old Bootloader)`.
You can configure both in `Tools`.
