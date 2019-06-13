# RB3 Robotic Arm

# Table of Contents

- [1) Hardware](#1-hardware)
   - [1.1) Hardware requirements](#11-hardware-requirements)
- [2) Software](#2-software)
   - [2.1) Build Environment Setup](#21-build-environment-setup)
- [3) RB3 Robotic Arm](#3-rb3-robotic-arm)
   - [3.1) Hardware setup](#31-hardware-setup)
   - [3.2) Theory of Operation](#32-theory-of-operation)
- [4) Video Demonstration](#4-video-demonstration)
- [5) Change Log](#5-change-log)

***
***

# 1) Hardware

## 1.1) Hardware requirements

- [96Boards RB3 CE Board by Qualcomm](https://www.96boards.org/product/rb3-platform/)
- 5v 10A Power Supply
- [LewanSoul 6DOF Robotic Arm Kit](https://www.amazon.com/dp/B074T6DPKX/)
- [PCA9685 Based Servo Driver](https://www.amazon.com/Adafruit-16-Channel-12-bit-Servo-Driver/dp/B01G61MZF4/)
    - An I2C voltage Level shifter is required, either on of the following can be used:
        - [Audio Mezzanine](https://www.96boards.org/product/audio-mezzanine/)
        - [Sensors Mezzanine](https://www.96boards.org/product/sensors-mezzanine/)
        - [LinkSprite Mezzanine](https://www.96boards.org/product/linkspritesensorkit/)
- Decent USB Webcam
    - Recommended: [Logitech C922x Pro Stream Webcam](https://www.amazon.com/Logitech-C922x-Pro-Stream-Webcam/dp/B01LXCDPPK)
- Double Sided Tape to attach the Webcam:
    - Recommended: [3M Acrylic Foam Tape](https://www.amazon.com/3M-Automotive-Acrylic-Attachment-Black/dp/B000P18N76)
- HID Peripherals connected to the RB3
    - HDMI Monitor
    - USB Keyboard and Mouse
- Active Internet connection over Ethernet LAN Cable

***
***

# 2) Software

## 2.1 Build Environment Setup

- Follow the official Debian installation guide for the RB3
    - [Linux Host Installation for DragonBoard-845c](https://www.96boards.org/documentation/consumer/dragonboard/dragonboard845c/installation/linux-fastboot.md.html)
- After this step all the development will be done on the RB3 itself, there is no requirement for a PC.
- Once booted into debian clone this repository: `git clone https://github.com/96boards-projects/RB3-RoboticArm`
- Run the installation kit that install all dependencies:
```shell
cd RB3-RoboticArm
bash install.sh
```

***
***

# 3) RB3 Robotic Arm

## 3.1) Hardware Setup

### STEP-1: Assemble the Robotic Arm.

Although the assembly process highly depends on you particular model of robotic arm, but if you are using the LewanSoul 6DOF Robotic Arm Kit, here is their official tutorial that you can follow:

[![Assembly guide](https://img.youtube.com/vi/hFmm4dNWQac/0.jpg)](https://www.youtube.com/watch?v=hFmm4dNWQac)

Once you have everything assembled, temporarily disassemble the Robotic Arm from all the visible servo's axel. Your arm should now be in 6 pieces. We will put these pieces back together once we have all the servos set to their correct angles.


#### STEP-2: Connecting The Robotic Arm to PCA9685

> Note: align the Black wire to the ground pin on the PCA board

| Servo Number             | PCA9685 PWM Channel |
|:------------------------:|:-------------------:|
| Servo 1 (Base)           | Channel 0           |
| Servo 2 (Shoulder)       | Channel 1           |
| Servo 3 (Elbow)          | Channel 2           |
| Servo 4 (Wrist Up-Down)  | Channel 3           |
| Servo 5 (Wrist Sideways) | Channel 4           |
| Servo 6 (Gripper)        | Channel 5           |

- Connect the 5v 10A Power Supply to the external power input on the PCA9685 Board


#### STEP-3: Connecting the PCA9685 to the RB3

| PCA9685 | Level Shifter | RB3                        |
|:-------:|:-------------:|:--------------------------:|
| VCC     | 5v 'VCC' 1v8  | 1v8                        |
| GND     | GND           | GND                        |
| SDA     | 5v 'SDA' 1v8  | I2C0_SDA / Physical Pin 17 |
| SCL     | 5v 'SCL' 1v8  | I2C0_SCL / Physical Pin 15 |


#### STEP-4: Mounting the Camera on the Robotic Arm

The webcam needs to be attached to the gripper servo using a double sided tape with the camera lense facing down.
Use these images as visual aid to proceed: 

![](https://i.imgur.com/hyE3Utz.jpg)
![](https://i.imgur.com/chLLt9D.jpg)


#### STEP-5: Align the Servos and Reconnect the Pieces

- Run the code, this will cause the Servos to set in the correct orientation: `sudo bash launch.sh gui`
- Wait for the servos to twitch and set to required position.
- Now Re-Assemble the arm with the correct angles as follows, also make sure to keep the code running and the servos powered on throughout the process:
    - Base at 90º
    - Shoulder at 90º
    - Elbow at 90º
    - Wrist Up-Down at 30º
    - Wrist sideways at 30º
    - Gripper at 0º or closed
- At the end you arm should look like this:

![](https://i.imgur.com/kUjIUIy.png)


## 3.2) Theory of Operation

### Voice Mode

- Run the code: `sudo bash launch voice`
- Make sure the object(s) are in the opencv view window.
- Wait for the text console say: `Say Something`
- Follow by replying "Hey July"
- If your voice is replied correctly, you should see `What do you want?` appear on the text console
- Follow up by saying: "Pick up the [color] [shape]"
    - example: Pickup the Yellow Rectangle
- The Robotic Arm should proceed to center itself and pickup the object, wait for a bit, and drop it.

### Text Mode

- Run the code: `sudo bash launch gui`
- Make sure the object(s) are in the opencv view window.
- Wait for the GUI text box to come up.
- Follow up by typing: "Pick up the [color] [shape]"
    - example: Pickup the Yellow Rectangle
- Click submit button.
- The Robotic Arm should proceed to center itself and pickup the object, wait for a bit, and drop it.

# 5) Video Demonstration

[![Assembly guide](https://img.youtube.com/vi/Z6zoDpyWut8/0.jpg)](https://youtu.be/Z6zoDpyWut8)
