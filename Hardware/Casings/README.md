# Casing 3D Designs

This folder contains the required 3D models for the casings of the device.

## WARNING: 
Ensure the cables connected to the actuator are not in direct contact with the skin without insulation. This can cause significant EEG artefacts and even irritation when VTS is applied to certain areas of the body. The wires should be insulated and the terminals facing away from the skin, ideally further insulated with glue or some other method


## Extra Information:
- All of the above was printed in PETG for the prototype

- 4 M2 screws and 2 M2 hex standoffs (6mm) were used to close the main casing

- The charger casing has a small mounting postion for a magnetic connector, compatible with the battery packs. The charger used for the prototype was 	
Sparkfun's PRT-12711 as it was readily available, though any single cell li-po charger with max current of 800mA should work. Again, M2 screws and standoffs were used to close the casing.

- Some designs have a triangle fin attached for ease of 3D printing which can then be snapped off and filed till smooth.
  
- The main housing has wings to attach material for a strap which can then be buckled to the upper arm with the given buckle design (the buckle design is from https://www.printables.com/model/491473-camera-buckle).

- The actuator casing serves to increase pressure on the skin (making the vibrations feel stronger) and insulate it, though tape on the area of skin that it is placed may also be necessary to prevent sweat ingress and further insulate the actuator to avoid EEG artefacts. This can then be tightly taped to the skin with appropriate tape or held in place with a strap if using the mountable actuator sleeve.
  
- The battery leads should be cut and soldered to the corresponding magnetic connector terminals (view the PCB to see which pin is which, there are 2 ground pins and one VDD, the battery used had a TH pin that was unused). The battery can then be slotted into the battery holder - the magnetic conncetor glued into the battery lid and the lid glued into the holder, creating a standalone battery pack. Note: the battery should be relatively loose in the holder when placing it in, li-po batteries may expand and this must be accounted for.

- The button can be placed into the recess in the wall of the main housing before the PCB is inserted, after which it will be held in place by the button.


