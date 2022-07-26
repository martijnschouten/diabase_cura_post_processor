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
            }
        }"""

    def execute(self, data):
        #increase each tool number by one
        data[0] = 'G28\n; home the printer before cura does the T1' + data[0]
        
        for layer_number, layer in enumerate(data):
            #start by increasing number 5 and then go down. If one would start at 0 the result would end up as 1
            for i1 in range(5,-1,-1):
                data[layer_number] = re.sub('T'+str(i1),'T'+str(i1+1), data[layer_number]) #increase all tool numbers by one
        
        data[0] = '; postproccesed using the NIFTy Diabase Post processor\n' + data[0]

        return data