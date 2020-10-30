# Copyright (c) 2017 Ruben Dulek
# The PostProcessingPlugin is released under the terms of the AGPLv3 or higher.

import re #To perform the search and replace.

from ..Script import Script
import warnings

from UM.Application import Application #To get the current printer's settings.
from UM.Logger import Logger

class NIFTyDiabasePressureAdvance(Script):
    """Performs a search-and-replace on all g-code.

    Due to technical limitations, the search can't cross the border between
    layers.
    """

    def getSettingDataString(self):
        return """{
            "name": "NIFTy Diabase Pressure Advance",
            "key": "NIFTyDiabasePressureAdvance",
            "metadata": {},
            "version": 2,
            "settings":
            {
                "pressure_advance_T1": {
                    "label": "amount of pressure advance T1",
                    "description": "How much pressure advance should be used",
                    "type": "float",
                    "default_value": 0.1,
                    "minimum_value": "0"
                },
                "pressure_advance_T2": {
                    "label": "amount of pressure advance T2",
                    "description": "How much pressure advance should be used",
                    "type": "float",
                    "default_value": 1.0,
                    "minimum_value": "0"
                },
                "pressure_advance_T3": {
                    "label": "amount of pressure advance T3",
                    "description": "How much pressure advance should be used",
                    "type": "float",
                    "default_value": 1.2,
                    "minimum_value": "0"
                },
                "pressure_advance_T4": {
                    "label": "amount of pressure advance T4",
                    "description": "How much pressure advance should be used",
                    "type": "float",
                    "default_value": 4.0,
                    "minimum_value": "0"
                },
                "pressure_advance_T5": {
                    "label": "amount of pressure advance T5",
                    "description": "How much pressure advance should be used",
                    "type": "float",
                    "default_value": 0.1,
                    "minimum_value": "0"
                }
            }
        }"""

    def execute(self, data):     
        #Logger.log("i", 'initial extruder: ' + str(initial_extruder))
        
        PA_T1 = self.getSettingValueByKey("pressure_advance_T1")
        data = self.add_pressure_advance(data,PA_T1,1)
        PA_T2 = self.getSettingValueByKey("pressure_advance_T2")
        data = self.add_pressure_advance(data,PA_T2,2)
        PA_T3 = self.getSettingValueByKey("pressure_advance_T3")
        data = self.add_pressure_advance(data,PA_T3,3)
        PA_T4 = self.getSettingValueByKey("pressure_advance_T4")
        data = self.add_pressure_advance(data,PA_T4,4)
        PA_T5 = self.getSettingValueByKey("pressure_advance_T5")
        data = self.add_pressure_advance(data,PA_T5,5)     
        
        data[0] = '; postproccesed using the NIFTy Diabase Pressure Advance Postprocessor\n' + data[0]

        return data
    
    def add_pressure_advance(self,data,PA_amount,tool_number):
        for layer_number, layer in enumerate(data):
            layer_lines = layer.splitlines()
            for line_number, layer_line in enumerate(layer_lines):
                if layer_line == 'T'+str(tool_number) or \
                layer_line == 'M98 P"tprime' + str(tool_number) + 'pre.g" ; move to cleaning station' or \
                layer_line == 'M98 P"tprime' + str(tool_number) + '.g" ; cleaning ':
                    layer_lines.insert(line_number+1,'M572 D1 S' + str(PA_amount))
                    layer_lines.insert(line_number+1,'M572 D0 S' + str(PA_amount))
                    
                    
            data[layer_number] = '\n'.join(layer_lines)
        
        return data