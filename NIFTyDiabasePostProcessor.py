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
                "blob_size_T1": {
                    "label": "Blob size T1",
                    "description": "How much material in mm should be used to make the blob",
                    "type": "float",
                    "default_value": 15.0,
                    "minimum_value": "0",
                    "enabled": "cleaning_T1 != 'Off' and cleaning_style == 'New'"
                },
                "blob_speed_T1": {
                    "label": "Blob extrusion speed T1",
                    "description": "How fast the material should be extruded while making a blob",
                    "unit": "mm/s",
                    "type": "float",
                    "default_value": 30.0,
                    "minimum_value": "0",
                    "enabled": "cleaning_T1 != 'Off' and cleaning_style == 'New'"
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
                "blob_size_T2": {
                    "label": "Blob size T2",
                    "description": "How much material in mm should be used to make the blob",
                    "type": "float",
                    "default_value": 15.0,
                    "minimum_value": "0",
                    "enabled": "cleaning_T2 != 'Off' and cleaning_style == 'New'"
                },
                "blob_speed_T2": {
                    "label": "Blob extrusion speed T2",
                    "description": "How fast the material should be extruded while making a blob",
                    "unit": "mm/s",
                    "type": "float",
                    "default_value": 30.0,
                    "minimum_value": "0",
                    "enabled": "cleaning_T2 != 'Off' and cleaning_style == 'New'"
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
                "blob_size_T3": {
                    "label": "Blob size T3",
                    "description": "How much material in mm should be used to make the blob",
                    "type": "float",
                    "default_value": 15.0,
                    "minimum_value": "0",
                    "enabled": "cleaning_T3 != 'Off' and cleaning_style == 'New'"
                },
                "blob_speed_T3": {
                    "label": "Blob extrusion speed T3",
                    "description": "How fast the material should be extruded while making a blob",
                    "unit": "mm/s",
                    "type": "float",
                    "default_value": 30.0,
                    "minimum_value": "0",
                    "enabled": "cleaning_T3 != 'Off' and cleaning_style == 'New'"
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
                "blob_size_T4": {
                    "label": "Blob size T4",
                    "description": "How much material in mm should be used to make the blob",
                    "type": "float",
                    "default_value": 15.0,
                    "minimum_value": "0",
                    "enabled": "cleaning_T4 != 'Off' and cleaning_style == 'New'"
                },
                "blob_speed_T4": {
                    "label": "Blob extrusion speed T4",
                    "description": "How fast the material should be extruded while making a blob",
                    "unit": "mm/s",
                    "type": "float",
                    "default_value": 30.0,
                    "minimum_value": "0",
                    "enabled": "cleaning_T4 != 'Off' and cleaning_style == 'New'"
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
                },
                "blob_size_T5": {
                    "label": "Blob size T5",
                    "description": "How much material in mm should be used to make the blob",
                    "type": "float",
                    "default_value": 15.0,
                    "minimum_value": "0",
                    "enabled": "cleaning_T5 != 'Off' and cleaning_style == 'New'"
                },
                "blob_speed_T5": {
                    "label": "Blob extrusion speed T5",
                    "description": "How fast the material should be extruded while making a blob",
                    "unit": "mm/s",
                    "type": "float",
                    "default_value": 30.0,
                    "minimum_value": "0",
                    "enabled": "cleaning_T5 != 'Off' and cleaning_style == 'New'"
                },
                "cleaning_style": {
                    "label": "Cleaning style",
                    "description": "Cleaning style",
                    "type": "enum",
                    "options": {
                        "Old": "Old",
                        "New": "New"
                    },
                    "default_value": "New"
                }
            }
        }"""

    def execute(self, data):
        #increase each tool number by one
        for layer_number, layer in enumerate(data):
            #start by increasing number 4 and then go down. If one would start at 0 the result would end up as 1
            for i1 in range(4,-1,-1):
                data[layer_number] = re.sub('T'+str(i1),'T'+str(i1+1), data[layer_number]) #increase all tool numbers by one
        
        cleaning_style = self.getSettingValueByKey("cleaning_style")
        initial_extruder = self.find_initial_extruder(data)
        Logger.log("i", 'initial extruder: ' + str(initial_extruder))
        
        cleaning_T1 = self.getSettingValueByKey("cleaning_T1")
        interval_T1 = self.getSettingValueByKey("interval_T1")
        blob_size_T1 = self.getSettingValueByKey("blob_size_T1")
        blob_speed_T1 = self.getSettingValueByKey("blob_speed_T1")
        data = self.insert_cleaning(data,cleaning_T1,interval_T1,blob_size_T1,blob_speed_T1,cleaning_style,initial_extruder,1)
        
        cleaning_T2 = self.getSettingValueByKey("cleaning_T2")
        interval_T2 = self.getSettingValueByKey("interval_T2")
        blob_size_T2 = self.getSettingValueByKey("blob_size_T2")
        blob_speed_T2 = self.getSettingValueByKey("blob_speed_T2")
        data = self.insert_cleaning(data,cleaning_T2,interval_T2,blob_size_T2,blob_speed_T2,cleaning_style,initial_extruder,2)
        
        cleaning_T3 = self.getSettingValueByKey("cleaning_T3")
        interval_T3 = self.getSettingValueByKey("interval_T3")
        blob_size_T3 = self.getSettingValueByKey("blob_size_T3")
        blob_speed_T3 = self.getSettingValueByKey("blob_speed_T3")
        data = self.insert_cleaning(data,cleaning_T3,interval_T3,blob_size_T3,blob_speed_T3,cleaning_style,initial_extruder,3)
        
        cleaning_T4 = self.getSettingValueByKey("cleaning_T4")
        interval_T4 = self.getSettingValueByKey("interval_T4")
        blob_size_T4 = self.getSettingValueByKey("blob_size_T4")
        blob_speed_T4 = self.getSettingValueByKey("blob_speed_T4")
        data = self.insert_cleaning(data,cleaning_T4,interval_T4,blob_size_T4,blob_speed_T4,cleaning_style,initial_extruder,4)
        
        cleaning_T5 = self.getSettingValueByKey("cleaning_T5")
        interval_T5 = self.getSettingValueByKey("interval_T5")
        blob_size_T5 = self.getSettingValueByKey("blob_size_T5")
        blob_speed_T5 = self.getSettingValueByKey("blob_speed_T5")
        data = self.insert_cleaning(data,cleaning_T5,interval_T5,blob_size_T5,blob_speed_T5,cleaning_style,initial_extruder,5)
        
        
        
        
        data[0] = '; postproccesed using the NIFTy Diabase Post processor\n' + data[0]

        return data
        
    def insert_cleaning(self,data,behaviour,interval,blob_size,blob_speed,cleaning_style,initial_extruder,tool_number):
        
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
        passed_initialisation_toolchange = False
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
                            #ignore the very first toolchange
                            if passed_initialisation_toolchange == True or initial_extruder != tool_number:
                                #found the tool change
                                state = 'found_the_tool_change'
                                tool_change = tool_change + 1
                                
                                if behaviour == 'Interval':
                                    if not ((tool_change % interval ) == 1):
                                        break

                                tool_change_line = line_number
                            else:
                                passed_initialisation_toolchange = True
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
                    if cleaning_style == 'Old':
                        layer_lines.insert(cleaning_line,'M98 P"tprime' + str(tool_number) + '.g" ; cleaning ')
                    else:
                        toolchange_retraction_distance = Application.getInstance().getGlobalContainerStack().getProperty("switch_extruder_retraction_amount", "value")
                        toolchange_retraction_speed = Application.getInstance().getGlobalContainerStack().getProperty("switch_extruder_retraction_speed", "value")
                        toolchange_extrusion_speed = Application.getInstance().getGlobalContainerStack().getProperty("switch_extruder_prime_speed", "value")
                        toolchange_extra_extrusion = Application.getInstance().getGlobalContainerStack().getProperty("switch_extruder_extra_prime_amount", "value")
                        
                        Logger.log("i", 'layer_number: ' + str(layer_number))
                        Logger.log("i", 'initial extruder: ' + str(initial_extruder))
                        Logger.log("i", 'tool number: ' + str(tool_number))
                        toolchange_string = 'M98 P"tprime' + str(tool_number) + 'pre.g" ; move to cleaning station\n' + \
                                                'G1 E' + str(toolchange_retraction_distance+toolchange_extra_extrusion) + ' F' + str(toolchange_extrusion_speed*60) + '\n' + \
                                                'M42 P20 S0.75\n' + \
                                                'G1 E' + str(blob_size) + ' F' + str(blob_speed*60) + '\n' + \
                                                'M400\n' + \
                                                'G4 P3000 ;\n' + \
                                                'M42 P20 S0\n' + \
                                                'G1 E-' + str(toolchange_retraction_distance) + ' F' + str(toolchange_retraction_speed*60) + '\n' + \
                                                'M98 P"tprime' + str(tool_number) + 'post.g" ; move back'
                        if layer_number == 1 and initial_extruder == tool_number:
                            toolchange_string = toolchange_string + \
                                                '\nG1 E' + str(toolchange_retraction_distance+toolchange_extra_extrusion) + ' F' + str(toolchange_extrusion_speed*60)
                        layer_lines.insert(cleaning_line,toolchange_string)
                #delete the original toolchange.
                if tool_change_line > -1:                        
                    layer_lines.pop(tool_change_line)
                        
                #make one string of the list of gcode lines.
                data[layer_number] = '\n'.join(layer_lines)
        return data
                    
    def find_initial_extruder(self,data):
        for layer_number, layer in enumerate(data):
            layer_lines = layer.splitlines()
            for line_number, layer_line in enumerate(layer_lines):
                if layer_line[0] == 'T':
                    return int(layer_line[1])