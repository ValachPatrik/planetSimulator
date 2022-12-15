# Planet Simulator

Simulator of the movement of celestial bodies, uses basic newton and vector logic.
Initialy spawn either an n-tary-stable-system or uses the library present in the files to create a representation of our solar system.
Key bindings for control are listed in the GUI. Uppon pressing any gravitational body an edit window pops up, which allows to edit it's values.

After longer run times the simulation is prone to big errors, for it uses basic point logic of gravitational mass. Moons are not present, or other bodies that could influence the movement of planets. The speed of the simulation can be increased, but beware the greater the step the greater the inacuracy. Also because of computer logic and inadequate precision of calculation the symulation gets completely out of whack after couple thousand of years. The simulation does not count with colisions of the bodies, therefore after close contact the planets tent to be catapulted out of the allocated GUI, but they continue to be simulated.

## N-Tary-Stable-System

Generates n planets of the same mass, that move synchronously around each other. Can be easily used to create custom systems to simulate your own planet configurations.

## Solar System

Constructs a simulation of our solar system. Generates the first x number of planets that is chosen by the user. The simulation is set up to closely observe our inner solar system. But can be modified by changing the scale to accomodate the whole solar system.
