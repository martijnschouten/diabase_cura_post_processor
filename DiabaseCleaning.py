# Copyright (c) 2017 Ruben Dulek
# The PostProcessingPlugin is released under the terms of the AGPLv3 or higher.

import re #To perform the search and replace.

from ..Script import Script
import warnings

class DiabaseCleaning(Script):
    """Performs a search-and-replace on all g-code.

    Due to technical limitations, the search can't cross the border between
    layers.
    """

    def getSettingDataString(self):
        return """{
            "name": "Diabase cleaning",
            "key": "DiabaseCleaning",
            "metadata": {},
            "version": 2,
            "settings":
            {
                "cleaning_T1": {
                    "label": "Cleaning of T1",
                    "description": "Cleaning behaviour for Tool 1",
                    "type": "enum",
                    "options": {
                        "Off": "Off",
                        "Once": "Once",
                        "Interval": "Interval",
                        "Always": "Always"
                    },
                    "default_value": "Off"
                },
                "interval_T1": {
                    "label": "Interval T1",
                    "description": "Once in how many toolchanges the tool is cleaned",
                    "type": "int",
                    "default_value": 3,
                    "minimum_value": "2",
                    "enabled": "cleaning_T1 == 'Interval'"
                },
                "cleaning_T2": {
                    "label": "Cleaning of T2",
                    "description": "Cleaning behaviour for Tool 2",
                    "type": "enum",
                    "options": {
                        "Off": "Off",
                        "Once": "Once",
                        "Interval": "Interval",
                        "Always": "Always"
                    },
                    "default_value": "Off"
                },
                "interval_T2": {
                    "label": "Interval T2",
                    "description": "Once in how many toolchanges the tool is cleaned",
                    "type": "int",
                    "default_value": 3,
                    "minimum_value": "2",
                    "enabled": "cleaning_T2 == 'Interval'"
                },
                "cleaning_T3": {
                    "label": "Cleaning of T3",
                    "description": "Cleaning behaviour for Tool 3",
                    "type": "enum",
                    "options": {
                        "Off": "Off",
                        "Once": "Once",
                        "Interval": "Interval",
                        "Always": "Always"
                    },
                    "default_value": "Off"
                },
                "interval_T3": {
                    "label": "Interval T3",
                    "description": "Once in how many toolchanges the tool is cleaned",
                    "type": "int",
                    "default_value": 3,
                    "minimum_value": "2",
                    "enabled": "cleaning_T3 == 'Interval'"
                },
                "cleaning_T4": {
                    "label": "Cleaning of T4",
                    "description": "Cleaning behaviour for Tool 4",
                    "type": "enum",
                    "options": {
                        "Off": "Off",
                        "Once": "Once",
                        "Interval": "Interval",
                        "Always": "Always"
                    },
                    "default_value": "Off"
                },
                "interval_T4": {
                    "label": "Interval T4",
                    "description": "Once in how many toolchanges the tool is cleaned",
                    "type": "int",
                    "default_value": 3,
                    "minimum_value": "2",
                    "enabled": "cleaning_T4 == 'Interval'"
                },
                "cleaning_T5": {
                    "label": "Cleaning of T5",
                    "description": "Cleaning behaviour for Tool 5",
                    "type": "enum",
                    "options": {
                        "Off": "Off",
                        "Once": "Once",
                        "Interval": "Interval",
                        "Always": "Always"
                    },
                    "default_value": "Off"
                },
                "interval_T5": {
                    "label": "Interval T5",
                    "description": "Once in how many toolchanges the tool is cleaned",
                    "type": "int",
                    "default_value": 3,
                    "minimum_value": "2",
                    "enabled": "cleaning_T5 == 'Interval'"
                }
            }
        }"""

    def execute(self, data):
        #increase each tool number by one
        for layer_number, layer in enumerate(data):
            #start by increasing number 4 and then go down. If one would start at 0 the result would end up as 1
            for i1 in range(4,-1,-1):
                data[layer_number] = re.sub('T'+str(i1),'T'+str(i1+1), data[layer_number]) #increase all tool numbers by one
            
        cleaning_T1 = self.getSettingValueByKey("cleaning_T1")
        interval_T1 = self.getSettingValueByKey("interval_T1")
        data = self.insert_cleaning(data,cleaning_T1,interval_T1,1)
        
        cleaning_T2 = self.getSettingValueByKey("cleaning_T2")
        interval_T2 = self.getSettingValueByKey("interval_T2")
        data = self.insert_cleaning(data,cleaning_T2,interval_T2,2)
        
        cleaning_T3 = self.getSettingValueByKey("cleaning_T3")
        interval_T3 = self.getSettingValueByKey("interval_T3")
        data = self.insert_cleaning(data,cleaning_T3,interval_T3,3)
        
        cleaning_T4 = self.getSettingValueByKey("cleaning_T4")
        interval_T4 = self.getSettingValueByKey("interval_T4")
        data = self.insert_cleaning(data,cleaning_T4,interval_T4,4)
        
        cleaning_T5 = self.getSettingValueByKey("cleaning_T5")
        interval_T5 = self.getSettingValueByKey("interval_T5")
        data = self.insert_cleaning(data,cleaning_T5,interval_T5,5)
        
        data[0] = '; postproccesed using the NIFTy Diabase Post processor\n' + data[0]

        return data
        
    def insert_cleaning(self,data,behaviour,interval,tool_number):
        
        if behaviour == 'Off':
            data[0] = '; Tool ' + str(tool_number) + ' will not be cleaned \n' + data[0]
            return data
        elif behaviour == 'Once':
            data[0] = '; Tool ' + str(tool_number) + ' will be cleaned just once \n' + data[0]
        elif behaviour == 'Interval':
            data[0] = '; Tool ' + str(tool_number) + ' will be cleaned once every ' + str(interval)+ ' toolchanges \n' + data[0]
        elif behaviour == 'Always':
            data[0] = '; Tool ' + str(tool_number) + ' will always be cleaned \n' + data[0]
        else:
            raise Exception('unknown cleaning behaviour selected')
            
            
        tool_change = 0
        for layer_number, layer in enumerate(data):
            if ((tool_change > 0) and (behaviour == 'Once')):
                return data
            #check if the tool number is mentioned at all. (just to speed things up)
            if ((not re.search('T'+str(tool_number),layer) is None)):
                #split up the layer gcodes into seperate lines
                layer_lines = layer.splitlines()
                
                state = 'found_nothing'
                tool_change_line = -1
                cleaning_line = -1
                
                #that there is a T3 somewhere in the layer doesn't mean there is a toolchange.
                for line_number, layer_line in enumerate(layer_lines):
                    if state == 'found_nothing':
                        if layer_line == 'T'+str(tool_number):
                            #found the tool change
                            state = 'found_the_tool_change'
                            tool_change = tool_change + 1
                            
                            if behaviour == 'Interval':
                                if not ((tool_change % interval ) == 1):
                                    break
                            
                            tool_change_line = line_number
                    elif state == 'found_the_tool_change':
                        #check if there is a extruder heating gcode with a tool number, which would not work since we are moving the toolchange
                        if ((re.search('T1',layer_line) is None) and \
                        (re.search('T2',layer_line) is None) and \
                        (re.search('T3',layer_line) is None) and \
                        (re.search('T4',layer_line) is None) and \
                        (re.search('T5',layer_line) is None)):
                            if (not (re.search('M104',layer_line) is None) or \
                            (not re.search('M109',layer_line) is None)):
                                layer_lines[line_number] = layer_lines[line_number] + ' T' + str(tool_number)
                                
                        #check if this line a heating command
                        if ((re.search('M104',layer_line) is None) and \
                        (re.search('M109',layer_line) is None) and \
                        (re.search('M190',layer_line) is None)):
                            #found a line of code that is not about heating something.
                            #this is where we want to insert the cleaning step.
                            cleaning_line = line_number
                            break
                        
                #insert the cleaning line
                if cleaning_line > -1:
                    layer_lines.insert(cleaning_line,'M98 P"tprime' + str(tool_number) + '.g" ; cleaning ')
                #delete the original toolchange.
                if tool_change_line > -1:                        
                    layer_lines.pop(tool_change_line)
                        
                #make one string of the list of gcode lines.
                data[layer_number] = '\n'.join(layer_lines)
        return data
                    
        