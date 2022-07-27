# Copyright (c) 2017 Ruben Dulek
# The PostProcessingPlugin is released under the terms of the AGPLv3 or higher.

import re #To perform the search and replace.

from ..Script import Script
import warnings

from UM.Application import Application #To get the current printer's settings.
from UM.Logger import Logger

class NIFTyDiabasePostProcessor(Script):
    """Performs a search-and-replace on all g-code.

    Due to technical limitations, the search can't cross the border between
    layers.
    """

    def getSettingDataString(self):
        return """{
            "name": "NIFTy Diabase Post Processor",
            "key": "NIFTyDiabasePostProcessor",
            "metadata": {},
            "version": 2,
            "settings":
            {
                "Z_offset_all": {
                    "label": "Z offset all tools",
                    "description": "Additional Z offset for all tools",
                    "unit": "mm",
                    "type": "float",
                    "default_value": 0.0
                },
                "Z_offset_T1": {
                    "label": "Z offset T1",
                    "description": "Additional Z offset T1",
                    "unit": "mm",
                    "type": "float",
                    "default_value": 0.0
                },
                "Z_offset_T2": {
                    "label": "Z offset T2",
                    "description": "Additional Z offset T1",
                    "unit": "mm",
                    "type": "float",
                    "default_value": 0.0
                },
                "Z_offset_T3": {
                    "label": "Z offset T3",
                    "description": "Additional Z offset T1",
                    "unit": "mm",
                    "type": "float",
                    "default_value": 0.0
                },
                "Z_offset_T4": {
                    "label": "Z offset T4",
                    "description": "Additional Z offset T1",
                    "unit": "mm",
                    "type": "float",
                    "default_value": 0.0
                },
                "Z_offset_T5": {
                    "label": "Z offset T5",
                    "description": "Additional Z offset T1",
                    "unit": "mm",
                    "type": "float",
                    "default_value": 0.0
                },
                "Z_offset_T6": {
                    "label": "Z offset T6",
                    "description": "Additional Z offset T1",
                    "unit": "mm",
                    "type": "float",
                    "default_value": 0.0
                }
            }
        }"""

    def execute(self, data):
        #add message confirming that the postprocessor was used
        data[0] = '; postproccesed using the NIFTy Diabase Post processor\n' + data[0]
    
        #replace the tool selection command all the way at the beginning with a homing command
        #and add a tool number to the M104 and M109 commands without a tool number
        layer0_lines = data[1].splitlines()
        #Logger.log("e", 'lines in first layer: ' + str(len(layer0_lines)))
        initial_extruder = -1
        for i1 in range(len(layer0_lines)):
            #Logger.log("e", 'First letters: ' + layer0_lines[i1][0:6])
            #Logger.log("e", 'Initial extruder: ' + str(initial_extruder))
            if layer0_lines[i1][0] == 'T' and initial_extruder == -1:
                initial_extruder = int(layer0_lines[i1][1])
                layer0_lines[i1] = 'G28'
            
            if layer0_lines[i1][0:6] == 'M104 S' and initial_extruder > -1:
                layer0_lines[i1] = layer0_lines[i1][0:4] + ' T'+str(initial_extruder) + layer0_lines[i1][4:]
            
            if layer0_lines[i1][0:6] == 'M109 S' and initial_extruder > -1:
                layer0_lines[i1] = layer0_lines[i1][0:4] + ' T'+str(initial_extruder) + layer0_lines[i1][4:]
                break
            
        data[1] = '\n'.join(layer0_lines)
        
        #increase each tool number by one
        for layer_number, layer in enumerate(data):
            #start by increasing number 5 and then go down. If one would start at 0 the result would end up as 1
            for i1 in range(5,-1,-1):
                data[layer_number] = re.sub('T'+str(i1),'T'+str(i1+1), data[layer_number]) #increase all tool numbers by one
        
        Z_offset_all = float(self.getSettingValueByKey("Z_offset_all"))
        Z_offset_T1 = float(self.getSettingValueByKey("Z_offset_T1"))
        Z_offset_T2 = float(self.getSettingValueByKey("Z_offset_T2"))
        Z_offset_T3 = float(self.getSettingValueByKey("Z_offset_T3"))
        Z_offset_T4 = float(self.getSettingValueByKey("Z_offset_T4"))
        Z_offset_T5 = float(self.getSettingValueByKey("Z_offset_T5"))
        Z_offset_T6 = float(self.getSettingValueByKey("Z_offset_T6"))
        z_offsets = [Z_offset_T1, Z_offset_T2, Z_offset_T3, Z_offset_T4, Z_offset_T5, Z_offset_T6]
        last_offset = 99999999
        for layer_number, layer in enumerate(data):
            
            layer_lines = data[layer_number].splitlines()
            for line_number, layer_line in enumerate(layer_lines):
                for i1 in range(6):
                    #if layer_number<5:
                    #    Logger.log("e", 'layer_line: ' + layer_line)
                    if layer_line[0:2] == 'T' + str(i1+1) and last_offset!=Z_offset_all+z_offsets[i1]:
                        baby_step_line = 'M290 S%0.3f R0'%(Z_offset_all+z_offsets[i1])
                        layer_lines.insert(line_number+1,baby_step_line)
                        last_offset = Z_offset_all+z_offsets[i1]
                data[layer_number] = '\n'.join(layer_lines)
        return data