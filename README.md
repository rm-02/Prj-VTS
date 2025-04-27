# Vibro-Tactile Stimulation Device Design Repository

This repository contains all of the hardware and software files required to manufacture a prototype device capable of delivering low-latency vibro-tactile stimulation.

The device uses Enhanced Shockburst to wirelessly trigger a vibration via a piezoelectric TDK powerhap 1313 haptic actuator. From button press on a peripheral NRF52 device to actuation on this receiving device takes ~1.3ms.

The device uses a magnetic battery connector to allow for easy to use hot swappable batteries. This reduces the time without the device or time required to be stationary. From full charge to dead the battery lasts ~9.5 hours delivering vibration every 90ms.

Beware the device drives the piezo electric actuator at a high voltage, it is therefore imperative that it is handled safely. Please ensure the actuator leads are insulated from the skin, remove the battery before opening the device for any reason, and avoid water ingress into the case/actuator.

Below is an image of the assembled device, showing the dimensions when the battery is connected (in mm).

![Image](https://github.com/user-attachments/assets/cbbd6ffe-a1cb-4525-8aa0-f3d0e6cb2445)
