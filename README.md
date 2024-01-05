# Pacemaker Project
This project is based on the pacemaker specifications of [Boston Scientific](BostonScientificSpecs.pdf). For this project, a simulated pacemaker was built to visually and functionally represent the various functions of modern pacemakers. 

This project was completed in a team of 5 where there were 3 members on the Simulink team and 2 members on the DCM/GUI team. I was on the DCM/GUI team where we created the following features using model-based code generation and a Python GUI: 
1. 10 unique pacemaker modes (including AOO, VOO, AAI, VVI, AOOR, VOOR, AAIR, VVIR, DDD, DDDR)
2. Real-time electrocardiogram display from the ventricle and atrium readings
3. Locally encrypted data storage


## Technology Stack
* [Python](https://www.python.org)
* [MATLAB Simulink](https://www.mathworks.com/products/simulink.html)
* [CustomTkinter](https://customtkinter.tomschimansky.com)
* [NXP FRDM K64F Board](https://www.nxp.com/design/design-center/development-boards/freedom-development-boards/mcu-boards/freedom-development-platform-for-kinetis-k64-k63-and-k24-mcus:FRDM-K64F)
* [J-Link](https://www.segger.com/downloads/jlink/)

## Demonstration 
#### Video Demonstration
https://github.com/yangm-22/PacemakerProject/assets/122390643/221932aa-97bc-4ae0-be86-528b1932b4de

#### Device Controller-Monitor (DCM) 
![FRDM-K64F_Board](https://github.com/yangm-22/PacemakerProject/assets/122390643/0aafedc2-3788-4a01-81e2-f256bfadb3be) 
*<p align="center"> The FRDM-K64F Board </p>*
<br>

![Login_Screen](https://github.com/yangm-22/PacemakerProject/assets/122390643/c9a85ccc-4571-4e9d-a426-2c5cb4138ac1)
*<p align="center"> Login Screen </p>*
<br>

![Sign_Up_Screen](https://github.com/yangm-22/PacemakerProject/assets/122390643/f38ede96-df1f-41bb-8c8c-fee054f41e56)
*<p align="center"> Sign Up Screen </p>*
<br>

![Main_Screen](https://github.com/yangm-22/PacemakerProject/assets/122390643/996856f2-e724-4490-83b7-eb0567e7a1a8)
*<p align="center"> Main Screen </p>*
<br>

![Live_Electrogram_in_UI](https://github.com/yangm-22/PacemakerProject/assets/122390643/1da613e2-2025-4aa7-a2f9-bb1e6a97f041)
*<p align="center"> Live Electrogram Displayed in UI </p>*
<br>

#### Pacemaker (Simulink)
![Simulink_Overview](https://github.com/yangm-22/PacemakerProject/assets/122390643/a4b3c2a3-bc2b-48de-a350-a222037c7c50)
*<p align="center"> Simulink Overview </p>*
<br>

![Stateflow](https://github.com/yangm-22/PacemakerProject/assets/122390643/daae381d-51ec-4034-b101-6be90421ab8e)
*<p align="center"> Mode and Parameter Stateflow in Simulink </p>*
<br>

![Stateflow2](https://github.com/yangm-22/PacemakerProject/assets/122390643/5f8db0d7-d45a-4eca-840a-ecb0e562fc16)
*<p align="center"> Serial Communication Stateflow in Simulink </p>*
<br>

## Development Process 
#### Modeling with MATLAB Simulink
At the core of designing our pacemaker's functionality was the utilization of MATLAB Simulink. This enabled us to iteratively generate code and swiftly upload it onto our board.

Through user-defined parameters, our Simulink code facilitated pacing for both the atrium and ventricle, incorporating rate-adaptive pacing through a built-in accelerometer.

All important user-set data and electrocardiogram information were organized, forming a packet that was then transmitted to the device controller monitor via a micro USB connection.

#### Device Controller-Monitor (DCM)
Using the toolkit, Tkinter, in Python, we created a secure interface that allows for the modification of the pacemaker. The GUI that we designed allows for:
* Real-time display of the simulated heartbeat
* Patient data to be saved and modified
* Encryption of patient data
* Serial communication to the K64F board

#### Validation
To assess and verify the functionality of our pacemaker mode, we utilized Heartview, a cardiac simulation tool developed at McMaster University, which had been pre-flashed on our board.

## Installation
#### Prerequisites 
1. Python 3.18 or later
2. MATLAB Simulink 2023 or later

#### Python Libraries
```
pip install customtkinter matplotlib serial numpy
```

#### MATLAB Simulink Libraries
* Embedded Coder, Fixed-Point Designer, MATLAB Coder, Simulink Check, Simulink Coder, Simulink Coverage, Simulink Design Verifier, Simulink Desktop Real-Time, Simulink Test, and Stateflow
* [Simulink Coder Support Package for NXP FRDM-K64F Board](https://www.mathworks.com/matlabcentral/fileexchange/55318-simulink-coder-support-package-for-nxp-frdm-k64f-board#:~:text=Simulink®%20Coder™%20Support,K64F%20peripherals%20and%20communication%20interfaces.)
* [Kinetis SDK 1.2.0 mainline release](https://www.nxp.com/design/design-center/designs/software-development-kit-for-kinetis-mcus:KINETIS-SDK)
* [V6.20a of the J-Link Software](https://www.segger.com/downloads/jlink/)

In MATLAB, type the following into the terminal:
```
open([codertarget.freedomk64f.internal.getSpPkgRootDir,
'/src/mw_sdk_interface.c']);
```

Upon opening the device change the following line:
```
{ GPIO_MAKE_PIN(GPIOA_IDX, 0),  MW_NOT_USED},// PTA0, D8
```
into the following:
```
{ GPIO_MAKE_PIN(GPIOC_IDX, 12),  MW_NOT_USED},// PTC12, D8
```



