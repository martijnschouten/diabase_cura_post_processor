This postprossesor can be used to generate code for the Diabase H-Series printers using cura.
For the time being only additive manufacturing is supported. Subtractive manufacturing is not supported.

Installation instructions for Windows:
* Install the latest version of Cura (version 4.7.0 at the moment of writing)
* copy the file "NIFTyDiabasePostProcessor.py" to the C:\Program Files\Ultimaker Cura 4.7.0\plugins\PostProcessingPlugin\scripts folder
* install the Duet RepRapFirmware Integration plugin
* restart cura
* enable the script under Extensions->post processing-> add a script-> NIFTy diabase post processor
* go to extensions->DuetRRF and click on add. Fill in you printer name and ip address.
* use the template.3mf file as template for your prints.