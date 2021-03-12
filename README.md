# w202-final-project
Final project for w202, University of California, Berkeley MICS program.

## Contributors
``Nathaniel Singer <nathaniel.singer@berkeley.edu><br>
Lauren Ayala <layala23@berkeley.edu><br>
Jeremy Carlson <jscarlson@berkeley.edu><br>
Mariah Martinez <mariah.martinez@berkeley.edu><br>``

# Execution
## Overview
The basic interface setup is an emulated Space Vehicle, over TCP. While these frames normally would be sent over a much lower level link, due to the development context and language used for prototyping, in this context, the protocol rides TCP. This results in some "ism's" but the byte representation is fairly straightforward and can be directly translated to the associated C for direct hardware interfacing, given more time.

To execute commands on the space vehicle, the ground.py client file coordinates frame direction to the vehicle.

## Start the Space Vehicle(SV) Emulator
``./space.py -h``

## Run the ground segment client
``./ground.py -h``
