import numpy as np

''' Global Variables for use '''
lst_parameters = ['Lower Rate Limit', 'Upper Rate Limit', 'Maximum Sensor Rate', 'Fixed AV Delay', 'Dynamic AV Delay', 'Sensed AV Delay Offset',
                  'Atrial Amplitude', 'Ventricular Amplitude', 'Atrial Pulse Width', 'Ventricular Pulse Width', 'Atrial Sensitivity', 'Ventricular Sensitivity',
                  'VRP', 'ARP', 'PVARP', 'PVARP Extension', 'Hysteresis', 'Rate Smoothing', 'ATR Duration', 'ATR Fallback Mode', 'ATR Fallback Time',
                  'Activity Threshold', 'Reaction Time', 'Response Factor', 'Recovery Time']

dict_param_nom_vals = {'Lower Rate Limit' : 60, 'Upper Rate Limit' : 120, 'Maximum Sensor Rate' : 120, 'Fixed AV Delay' : 150, 'Dynamic AV Delay' : 'Off', 'Sensed AV Delay Offset' : 'Off',
                  'Atrial Amplitude' : 5, 'Ventricular Amplitude' : 5, 'Atrial Pulse Width' : 1, 'Ventricular Pulse Width' : 1, 'Atrial Sensitivity' : 2.5, 'Ventricular Sensitivity' : 2.5,
                  'VRP' : 320, 'ARP' : 250, 'PVARP' : 250, 'PVARP Extension' : 'Off', 'Hysteresis' : 'Off', 'Rate Smoothing' : 'Off', 'ATR Duration' : 20, 'ATR Fallback Mode' : 'Off', 'ATR Fallback Time' : 1,
                  'Activity Threshold' : 'Med', 'Reaction Time' : 30, 'Response Factor' : 8, 'Recovery Time' : 5}

# dicitonary of parameters and their values and units
dict_param_and_range = {
  'Lower Rate Limit' : [[i for i in range(30, 50, 5)] + [i for i in range(50, 91, 1)] + [i for i in range(95, 180, 5)], "ppm"], # [30,35,40,45,50,51,51,...]
  'Upper Rate Limit' : [[i for i in range(50, 180, 5)], "ppm"], # [50,55,60,65,...]
  'Maximum Sensor Rate' : [[i for i in range(50,176,5)], 'ppm'],
  'Fixed AV Delay' : [[i for i in range(70,301,10)], 'ms'],
  'Dynamic AV Delay' : [["Off", "On"], ''],
  'Sensed AV Delay Offset' : [["Off"] + [i for i in range(-10,-101,-10)], 'ms'],
  'Atrial Amplitude' : [["Off"] + [round(i,1) for i in np.arange(0.1,5.1,0.1)], "V"], # ["Off", 0.5,0.6,0.7,0.8,...]
  'Ventricular Amplitude' : [["Off"] + [round(i,1) for i in np.arange(0.1,5.1,0.1)], "V"], # ["Off", 0.5,0.6,0.7,0.8,...]
  'Atrial Pulse Width' : [[i for i in range(1, 31)], "ms"], # [[0.05, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9
  'Ventricular Pulse Width' : [[i for i in range(1, 31)], "ms"],
  'Atrial Sensitivity' : [[round(i,1) for i in np.arange(0, 5.1,0.1)], 'V'], 
  'Ventricular Sensitivity' : [[round(i,1) for i in np.arange(0, 5.1,0.1)], 'V'], 
  'VRP' : [[i for i in range(150, 510, 10)], "ms"], # [[150, 160, 170, 180, 190, 200, 210, 220, 230, 240, 250, 260, 270, 280, 290, 300, 310, 
  'ARP' : [[i for i in range(150, 510, 10)], "ms"], # [[150, 160, 170, 180, 190, 200, 210, 220, 230, 240, 250, 260, 270, 280, 290, 300, 310, 
  'PVARP' : [[i for i in range(150, 501, 10)],'ms'],
  'PVARP Extension' : [["Off"] + [i for i in range(50, 401, 50)], 'ms'],
  'Hysteresis' : [["Off"] + [i for i in range(30, 50, 5)] + [i for i in range(50, 91, 1)] + [i for i in range(95, 180, 5)], 'ppm'],
  'Rate Smoothing' : [["Off", 3, 6, 9, 12, 15, 18, 21, 25], '%'],
  'ATR Duration' : [[10] + [i for i in range(20,81,20)] + [i for i in range(100,2001,100)], 'cc'],
  'ATR Fallback Mode' : [["Off", "On"], ''],
  'ATR Fallback Time' : [[i for i in range(1,6)], 'min'],
  'Activity Threshold' : [['V-Low', 'Low', 'Med-Low', 'Med', 'Med-High', 'High', 'V-High'], ''],
  'Reaction Time' : [[i for i in range(10,51,10)], 'sec'],
  'Response Factor' : [[i for i in range(1,17)], ''],
  'Recovery Time' : [[i for i in range(2,17)],'min']
}

dict_modes = {'AOO' : [0, 1, 6, 8], 'VOO' : [0, 1, 7, 9], 'AAI' : [0, 1, 6, 8, 10, 13, 14, 16, 17], 'VVI' : [0, 1, 7, 9, 11, 12, 16, 17], 
              'AOOR' : [0, 1, 2, 6, 8, 21, 22, 23, 24], 'AAIR' : [0, 1, 2, 6, 8, 10, 13, 14, 16, 17, 21, 22, 23, 24], 'VOOR' : [0, 1, 2, 7, 9, 21, 22, 23, 24], 'VVIR' : [0, 1, 2, 7, 9, 11, 12, 16, 17, 21, 22, 23, 24],
              'DDD' : [0, 1, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 
              'DDDR' : [i for i in range(25)]} # all current modes implemented modes and their paramaters

dict_modes_enumeration = {'Off' : 0, 'AOO' : 1, 'VOO' : 2, 'AAI' : 3, 'VVI' : 4, 'AOOR' : 5, 'VOOR' : 6, 'AAIR' : 7, 'VVIR' : 8, 'DDD' : 9, 'DDDR' : 10}

dict_param_and_tolerance = {
  'Lower Rate Limit' : [8, "ms"],
  'Upper Rate Limit' : [8, "ms"], 
  'Maximum Sensor Rate' : [4, 'ms'],
  'Fixed AV Delay' : [8, 'ms'],
  'Atrial Amplitude' : [12, "%"], 
  'Ventricular Amplitude' : [12, "%"], 
  'Atrial Pulse Width' : [0.2, "ms"], 
  'Ventricular Pulse Width' : [0.2, "ms"],
  'VRP' : [8, "ms"], 
  'ARP' : [8, "ms"],
  'PVARP' : [8, 'ms'],
  'Atrial Sensitivity' : [20, "%"],
  'Ventricular Sensitivity' : [20, '%'],
  'Reaction Time' : [3, 's'],
  'Recovery Time' : [30, 's'],
  'Rate Smoothing' : [1, '%']
}

# format data to be sent to pacemaker
def format_data(current_mode_data):
    formattedArray = [0] * 26
    for parameter in current_mode_data:
        valueForParameter = current_mode_data[parameter] # the number or text value associated with a certain parameter in a mode
        index26 = lst_parameters.index(parameter) # grab the index relative to all the other parameters
        formattedArray[index26 + 1] = dict_param_and_range[parameter][0].index(valueForParameter) # insert the index of the correct number into the formatted array
    return formattedArray

def encrypt_password(password):
    new_pass = ""
    for i in password:
        new_pass = new_pass + i + "~"

    return new_pass
        

def decrypt_password(encrypted_password):
    password = ""
    count = 0
    for i in encrypted_password:
        if count % 2 == 0:
          password = password + i

        count += 1

    return password