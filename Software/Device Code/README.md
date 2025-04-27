The .zip file included here is the source code for the VTS device's microcontroller.

To upload this to the NRF52 devkit: 
- Connect the devkit to your PC
- Double click the RST button on the devkit (next to the USB-C port) and a folder should appear on your PC
- Drag and drop the zephyr.uf2 file (from VTS_Device_Code --> build --> zephyr) from your PC to the folder
- Once complete, press the USER button again to reset the device, it should now be programmed and ready to be used

The flow chart below shows how the program is set to behave from start up and on packet reception

![Image](https://github.com/user-attachments/assets/d7f2b869-4d52-4732-8c64-c215bd287e3f)
