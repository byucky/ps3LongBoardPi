# ps3LongBoardPi
Code to run an electric longboard ESC with a raspberry pi + bluetooth using a ps3 controller.

# Install Dependencies
```
sudo apt-get -y install libusb-dev joystick python-pygame
```

# To Connect Controller to Pi (Jessie and Jessie lite)

Compile the sixpair.c (This is a modified version of sixpair that works with the play station move navigation controller).
```
cd sixpair
gcc -o sixpair sixpair.c -lusb
```
Next we tell the controller to connect to the pi using sixpair.
Be sure you're bluetooth dongle is pluged in or bluetooth in enables with `ifconfig`, the pi should output something like this:
```
bluetooth functioning output
```
Now plug the ps3 controller into the pi and run sixpair: `./sixpair`. You should get an output like this.
```
Current Bluetooth master: 00:15:83:0c:bf:eb
Setting master bd_addr to 00:15:83:0c:bf:eb
```
Now unplug the controller.
The next step is to pair the devices.
```
sudo bluetoothctl
discoverable on
agent on
```
Now you can press the PS button on the controller and it should attempt to talk to the Raspberry Pi.
You should see some log lines like this at a regular interval:
```
[NEW] Device 38:C0:96:5C:C6:60 38-C0-96-5C-C6-60
[CHG] Device 38:C0:96:5C:C6:60 Connected: no
[DEL] Device 38:C0:96:5C:C6:60 38-C0-96-5C-C6-60
```
You will need to make a note of the MAC address displayed, it is the sequence with ':' symbols.
In this example it is 38:C0:96:5C:C6:60
With this we can attempt to make contact with the controller.
We need to use the connect command with the MAC address shown, in our example:
```
connect 38:C0:96:5C:C6:60
```
When it works you should see something like this:
```
Attempting to connect to 38:C0:96:5C:C6:60
[CHG] Device 38:C0:96:5C:C6:60 Modalias: usb:v054Cp0268d0100
[CHG] Device 38:C0:96:5C:C6:60 UUIDs:
        00001124-0000-1000-8000-00805f9b34fb
        00001200-0000-1000-8000-00805f9b34fb
Failed to connect: org.bluez.Error.Failed
```
Once we have seen the UUID values we can use the trust command to allow the controller to connect on its own.
Use the trust command with the MAC address from earlier, in our example:
```
trust 38:C0:96:5C:C6:60
```
If everything went well you should see something like:
```
[CHG] Device 38:C0:96:5C:C6:60 Trusted: yes
Changing 38:C0:96:5C:C6:60 trust succeeded
```
Use `quit` to exit bluetoothctl.

This explaination was highly based on [this](https://www.piborg.org/rpi-ps3-help) excellent explaination from PiBorg. 
I made the modifications to sixpair to work with the navigation controller.

# Make sure it's all working
Run the code with `sudo python piboard.py debug` and make sure your inputs are working.
Then hook everything up to your board and run `sudo python piboard.py` and get your motor turning.

# Commands

