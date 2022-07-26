This postprossesor can be used to generate code for the Diabase H-Series printers using cura.
For the time being only additive manufacturing is supported. Subtractive manufacturing is not supported.

Installation instructions for Windows:
* Install the latest version of Cura (version 5.1.0 at the moment of writing).
* Locate your scripts folder: Cura->Help->Show Configuration Foler.
* Copy the file "NIFTyDiabasePostProcessor.py" inside the scripts/ folder.
* Install the Duet RepRapFirmware Integration plugin.
* Restart cura.
* Use the H4052_template.3mf file as template for your prints on the diabase 52.
* Go to Manage Printers and select your diabase printer profile. Then click on connect Duet RepRapFirmware. Then fill in the IP-adress of your printer.

When working with multi-material prints you probably want to turn off "Automatically drop models to build plate" under Preverences->Configure Cura.

# Acknowledgement
This work was developed within the Wearable Robotics programme, funded by the Dutch Research Council (NWO)

<img src="https://user-images.githubusercontent.com/6079002/124443163-bd35c400-dd7d-11eb-9fe5-53c3def86459.jpg" width="62" height="100"><img src="https://user-images.githubusercontent.com/6079002/124443273-d3dc1b00-dd7d-11eb-9282-54c56e0f42db.png" width="165" height="100">
