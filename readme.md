This postprossesor can be used to generate code for the Diabase H-Series printers using cura.
For the time being only additive manufacturing is supported. Subtractive manufacturing is not supported.

Installation instructions:
* Install the latest version of Cura (version 4.7.0 at the moment of writing).
* Locate your scripts folder: Cura->Help->Show Configuration Foler.
* Copy the file "NIFTyDiabasePostProcessor.py" inside the scripts/ folder.
* Install the Duet RepRapFirmware Integration plugin.
* Restart cura.
* Enable the script under Extensions->Post Processing->Modify G-Code-> Add a script-> NIFTy Diabase Post Processor.
* Go to extensions->DuetRRF and click on add. Fill in you printer name and ip address.
* Use the template.3mf file as template for your prints.

To make use of the new cleaning algorithm. You need to upload the systemconfigfiles.zip to the Diabase. Note that this post processor was written for a machine which has 5 additive tools.
