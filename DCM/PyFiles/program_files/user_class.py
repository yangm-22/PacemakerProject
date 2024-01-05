import os
import json
import datetime
from .mode_variables import *
from .serialcomm import *

## Parameters we need for A1
# Lower Rate Limit, 
# Upper Rate Limit, 
# Atrial Ampli-tude, 
# Atrial Pules Width, 
# Ventricular Amplitude,
# Ventricular Pulse Width, 
# VRP, 
# ARP. 

class user:
    _username:str
    _password:str
    _email:str
    _current_mode:str

    def __init__(self, username:str = None, password:str = None, email:str = None, current_mode: str = None, existing_mode_data = None, recognized_devices = [], mode_parameter_history = None):
        self._username = username # object username
        self._password = password # object password
        self._email = email # object email
        self._recognized_devices = recognized_devices

        # set the current mode if it exists, if its a new user then set it to off intiailly
        if current_mode == None:
            self._current_mode = "Off" # object current running mode
        else:
            self._current_mode = current_mode

        # Intializing all mode data for the user
        if existing_mode_data == None: # run this if no existing data exists (new user) to create a dict of nominal(default values)
            self._all_mode_data = {} # dictioanry for all modes
            self._mode_parameter_history = []

            for mode in dict_modes:
                dict_mode_params = {} # dictionary containing relevant parameters and nominal values

                lst_mode_param = dict_modes[mode]

                for parameter_index in lst_mode_param:
                    dict_mode_params[lst_parameters[parameter_index]] = dict_param_nom_vals[lst_parameters[parameter_index]]
                
                self._all_mode_data[mode] = dict_mode_params
            
            self._mode_parameter_history.append([str(datetime.datetime.now()), self._all_mode_data])

        else: # run this part of there is existing data
            self._all_mode_data = existing_mode_data
            self._mode_parameter_history = mode_parameter_history
    
    ''' Methods for interacting with saved user data '''
    # save the instance of the user class to a json file in the form of a dicitonary
    def save_to_json(self, str_root_dir:str):
        dict_save_user = {"_username" : self._username, "_password" : self._password, "_email" : self._email, "_current_mode" : self._current_mode, "_all_mode_data" : self._all_mode_data, "_recognized_devices" : self._recognized_devices, "_mode_parameter_history" : self._mode_parameter_history}
        with open(str_root_dir + f'/{self._username}.json','w') as file:
            json.dump(dict_save_user, file)
    
    # delete the account by deleting the json file
    def delete_account(self, str_root_dir:str):
        try:
            os.remove(str_root_dir + f'/{self._username}.json')
            del self
            print('Successfully deleted account')
        except:
            print("Error Removing Account")
    
    @classmethod # class method for intiailizing the user class if a returning user logs in
    def load_from_json(cls, dict_user):
        return cls(username = dict_user["_username"], password = dict_user["_password"], email = dict_user["_email"], current_mode = dict_user["_current_mode"], existing_mode_data = dict_user["_all_mode_data"], recognized_devices = dict_user["_recognized_devices"], mode_parameter_history = dict_user["_mode_parameter_history"])
    
    ''' Accessor Methods '''
    def get_username(self):
        return self._username
    
    def get_password(self):
        return self._password
    
    def get_email(self):
        return self._email
    
    def get_current_mode(self):
        return self._current_mode
    
    def get_all_mode_data(self):
        return self._all_mode_data

    def get_all_recognized_devices(self):
        return self._recognized_devices
    
    def get_mode_parameter_history(self):
        return self._mode_parameter_history
    


    ''' Mutator Methods '''
    def set_all_mode_data(self, updated_all_mode_data):
        self._all_mode_data = updated_all_mode_data # updates the current mode
        # adds the new parameters to the history of data
        self._mode_parameter_history.append([str(datetime.datetime.now()), updated_all_mode_data])

    def set_username(self, new_username:str):
        self._username = new_username
    
    def set_password(self, new_password:str):
        self._password = new_password

    def set_current_mode(self, new_mode:str):
        self._current_mode = new_mode
    
    def add_new_device(self, device):
        self._recognized_devices.append(device)

    ''' Pace a Mode '''
    def get_formatted_data(self):
        # initialize pacing and send to pacemaker upon user log in or pacemaker is plugged in
        mode = self._current_mode
        if mode != "Off":
            current_mode_data = self._all_mode_data[mode]
            formatted_data = format_data(current_mode_data=current_mode_data)
            formatted_data[0] = dict_modes_enumeration[mode] # set the first number to represent the mode
            return formatted_data
        return [0] * 26



