This postprossesor can be used to generate code for the Diabase H-Series printers using cura.
For the time being only additive manufacturing is supported. Subtractive manufacturing is not supported.

Installation instructions for Windows:
* Install the latest version of Cura (version 4.9.0 at the moment of writing).
* Locate your scripts folder: Cura->Help->Show Configuration Foler.
* Copy the file "NIFTyDiabasePostProcessor.py" inside the scripts/ folder.
* Install the Duet RepRapFirmware Integration plugin.
* Restart cura.
* Enable the script under Extensions->Post Processing->Modify G-Code-> Add a script-> NIFTy Diabase Post Processor.
* Use the template.3mf file as template for your prints.
* Go to Manage Printers and select your diabase printer profile. Then click on connect Duet RepRapFirmware. Then fill in the IP-adress of your printer.


To make use of the new cleaning algorithm. You need to upload the systemconfigfiles.zip to the Diabase. Note that this post processor was written for a machine which has 5 additive tools.

In order to be able to use the linear advance, you should install the linear advance plugin from the cura marketplace. Then copy the linearadvance.py file into the  %appdata%/cura/4.7.0/plugins/LinearAdvanceSettingPlugin/LinearAdvanceSettingPlugin folder.

When working with multi-material prints you probably want to turn off "Automatically drop models to build plate" under Preverences->Configure Cura.

# Acknowledgement
This work was developed within the Wearable Robotics programme, funded by the Dutch Research Council (NWO)

<img src="https://user-images.githubusercontent.com/6079002/124443163-bd35c400-dd7d-11eb-9fe5-53c3def86459.jpg" width="62" height="100"><img src="https://user-images.githubusercontent.com/6079002/124443273-d3dc1b00-dd7d-11eb-9282-54c56e0f42db.png" width="165" height="100">
