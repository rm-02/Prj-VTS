This folder contains software examples for transmitting devices that would enable VTS.

USB_and_Button Example allows the NRF52 to be controlled by the provided Python app over USB to allow VTS waveform changes and sleep mode changes. It also triggers VTS when the voltage goes from low-high on pin D2 (P0.28), either by a connected button press or any other voltage trigger (0--> 3.3V). There is a debounce mechanism implemented to avoid the button press activating 2 VTS but this timeout has been set down to 50ms so should not pose an issue, if it does it can be set lower in src/main.c.

Time_Transmitter will simply make the NRF52 send a VTS enable packet over ESB every 90ms, useful for stress testing.

VTS triggers are sent by transmitting an ESB payload with the first byte {0x00}

VTS waveform changes are sent by transmitting an ESB payload with the first byte {0x01}

Sleep mode changes are sent by transmitting an ESB payload with the first byte {0x02}

To upload either program to the NRF52 devkit:

- Connect the devkit to your PC
- Double click the RST button on the devkit (next to the USB-C port) and a folder should appear on your PC
- Drag and drop the zephyr.uf2 file (from (Timed_Transmitter_Example or USB_and_Button_Example) --> build --> zephyr) from your PC to the folder
- Once complete, press the USER button again to reset the device, it should now be programmed and ready to be used

If you edit either file you can rebuild them in VSCode with Nordic Connect extensions. Set the bord to Nordic SOC/XIAO nrf52840 and add the device overlays. Use no sysbuild and then build the configuration
