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
                "Z_offset_T1": {
                    "label": "Z offset T1",
                    "description": "Additional Z offset T1",
                    "unit": "mm",
                    "type": "float",
                    "default_value": 0.0
                },
            }
        }"""

    def execute(self, data):
        #replace the tool selection command all the way at the beginning with a homing command
        layer0_lines = data[1].splitlines()
        #Logger.log("e", 'lines in first layer: ' + str(len(layer0_lines)))
        for i1 in range(len(layer0_lines)):
            #Logger.log("e", 'First letter: ' + layer0_lines[i1][0])
            if layer0_lines[i1][0] == 'T':
                layer0_lines[i1] = 'G28'
                break
        data[1] = '\n'.join(layer0_lines)
        
        #increase each tool number by one
        for layer_number, layer in enumerate(data):
            #start by increasing number 5 and then go down. If one would start at 0 the result would end up as 1
            for i1 in range(5,-1,-1):
                data[layer_number] = re.sub('T'+str(i1),'T'+str(i1+1), data[layer_number]) #increase all tool numbers by one
        
        data[0] = '; postproccesed using the NIFTy Diabase Post processor\n' + data[0]

        return data