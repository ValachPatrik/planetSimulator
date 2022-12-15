# Patrik Valach 
# 2021

from typing import List, Optional
import tkinter
import time
import random

from gravity import Body, calculate_system_energy
from initial_states import solar_bodies, n_nary_stable_system
from point import Point, Vector

SCALE = 10**9
SCREEN_SIZE = (600, 600)
line_group_index = 0
n_lines = 500  # Ammount of lines, more slows down simulation rapidly
lines = [None for i in range(n_lines)]
colors = ['#ffff00', '#ff0000', '#00ff00', '#0000ff', '#ff00ff']
pause = True
step_count = 1
elapsed_time = 0


def point_reduced(xy: Point) -> tuple:
    # Calculate coords when reduced to screen size
    return SCREEN_SIZE[0]/2 + xy.x/SCALE, SCREEN_SIZE[1]/2 + xy.y/SCALE


def pause_switch():  # Toggle simulation pause
    global pause
    if pause:
        pause = False
    else:
        pause = True


def create_popup(event, new: bool):
    # Window to add, edit or delete a body in canvas
    global pause
    pause = False
    pop_window = tkinter.Tk()
    pop_window.geometry('200x500')
    pop_window.title('Edit Celestial Body')

    i = None
    name = 'Planet'
    location = Point((event.x - SCREEN_SIZE[0]/2) * SCALE, (event.y - SCREEN_SIZE[0]/2) * SCALE)
    mass = 0
    vector = Vector(0, 0)
    if not new:
        for i in bodies:
            if location.distance(i.location) <= 10*SCALE:
                name = i.name
                location = i.location
                mass = i.mass
                vector = i.motion_vector
                break

    body_par = {
        'name': label_input(pop_window, 'Name', name),
        'location_x': label_input(pop_window, 'Location X', location.x),
        'location_y': label_input(pop_window, 'Location Y', location.y),
        'mass': label_input(pop_window, 'Mass', mass),
        'vector_x': label_input(pop_window, 'Motion Vector X', vector.x),
        'vector_y': label_input(pop_window, 'Motion Vector Y', vector.y)}

    implement = tkinter.Button(pop_window, text='Save', command=lambda: add_body(body_par, pop_window, i))
    implement.pack()
    delete = tkinter.Button(pop_window, text='Delete', command=lambda: del_body(pop_window, i, new))
    delete.pack()


def label_input(window: tkinter.Tk, label_text: str, entry_text: str) -> tkinter.Entry:
    # subfunction for popup window - labels and inputs
    label = tkinter.Label(window, text=label_text, padx=60, pady=5)
    label.pack()
    entry_text = tkinter.StringVar(window, entry_text)
    entry_box = tkinter.Entry(window, textvariable=entry_text)
    entry_box.pack()
    return entry_box


def add_body(body_par: dict, window: tkinter.Tk, body: Body):
    # subfunction for popup window to add or edit a body
    global bodies, n_planets, pause

    if body is None:  # new body
        n_planets += 1
        bodies.append(Body(
            Point(float(body_par['location_x'].get()), float(body_par['location_y'].get())),
            float(body_par['mass'].get()),
            Vector(float(body_par['vector_x'].get()), float(body_par['vector_y'].get())),
            str(body_par['name'].get())))
    else:  # update body values
        for i in range(len(bodies)):
            if bodies[i] == body:
                bodies[i].location = Point(float(body_par['location_x'].get()), float(body_par['location_y'].get()))
                bodies[i].mass = float(body_par['mass'].get())
                bodies[i].motion_vector = Vector(float(body_par['vector_x'].get()), float(body_par['vector_y'].get()))
                bodies[i].name = str(body_par['name'].get())
                break
    window.destroy()
    reset_lines()
    pause = True


def del_body(window: tkinter.Tk, body: None, new: bool = False):
    # subfuncion for popup window to delete or not add a body
    global n_planets, pause, bodies
    if not new:
        bodies.remove(body)
    n_planets -= 1
    window.destroy()
    reset_lines()
    pause = True


def reset_lines():  # Clean lines
    global lines, line_group_index
    for i in lines:
        canvas.delete(i)
    lines = [None for i in range(n_lines)]
    line_group_index = 0


def bodies_delete():  # Clean bodies & Lines
    global bodies
    bodies = []
    reset_lines()


def format_time(time: int) -> str:
    # format number of elapsed seconds into bigger time units
    y = int(time // 3.154 // 10**7)
    time -= y * 3.154 * 10**7
    d = int(time // 86400)
    time -= d * 86400
    h = int(time // 3600)
    time -= h * 3600
    m = int(time // 60)
    time -= m * 60
    return '{:n} years, {:3n} days, {:2n} hours, {:2n} minutes, {:2n} seconds'.format(y, d, h, m, time)


def update_step_size(plus_minus: int, step: int):
    # change step size based on input
    global step_size
    step_size += plus_minus * step


if __name__ == '__main__':
    # Create n-tary system or Create sol
    simulation = input('1 for n-tary-semi-stable-system | 2 for solar system ')
    assert simulation == '1' or simulation == '2', 'You inputed invalid values'
    n_planets = input('How many planets in system (solar system optimized for the first 4 planets) ')
    assert n_planets.isdigit(), 'You inputed invalid values'
    n_planets = int(n_planets)
    if simulation == '1':
        step_size = 10 ** 7
        bodies = n_nary_stable_system(n_planets, SCALE, SCREEN_SIZE)
    else:
        step_size = 10 ** 5
        n_planets += 1
        bodies = solar_bodies(only_first_n_planets=n_planets)

    # Canvas spawn
    window = tkinter.Tk()
    window.title('Celestial body simulation')
    canvas = tkinter.Canvas(window, width=SCREEN_SIZE[0], height=SCREEN_SIZE[1])
    canvas.pack()
    # Other widgets
    info_one_var = tkinter.StringVar()
    info_two_var = tkinter.StringVar()
    pause_button = tkinter.Button(window, text="Pause/Play", command=lambda: pause_switch())
    pause_button.pack()
    info_one = tkinter.Label(window, textvariable=info_one_var)
    info_one.pack()
    info_two = tkinter.Label(window, textvariable=info_two_var)
    info_two.pack()
    info_three = tkinter.Label(window, text='Pause/Play: Enter | Slow-down: Q | Speed-up: E | Combine with Shift for faster / Control for slower increments \n Wipe star trails: R | Remove all bodies: C')
    info_three.pack()
    info_four = tkinter.Label(window, text='Click on body to edit | Control + Click to create new Turtle')
    info_four.pack()

    while 42:  # Main Loop
        # Controls Bind
        window.bind('<Return>', lambda event: pause_switch())
        canvas.tag_bind('cel_body', '<Button-1>', lambda event, new=False: create_popup(event, new))
        window.bind('<Control-Button-1>', lambda event, new=True: create_popup(event, new))
        window.bind('<r>', lambda event: reset_lines())
        window.bind('<c>', lambda event: bodies_delete())
        window.bind('<q>', lambda event, plus_minus=-1, step=3600: update_step_size(plus_minus, step))
        window.bind('<e>', lambda event, plus_minus=1, step=3600: update_step_size(plus_minus, step))
        window.bind('<Shift-Q>', lambda event, plus_minus=-1, step=86400: update_step_size(plus_minus, step))
        window.bind('<Shift-E>', lambda event, plus_minus=1, step=86400: update_step_size(plus_minus, step))
        window.bind('<Control-q>', lambda event, plus_minus=-1, step=60: update_step_size(plus_minus, step))
        window.bind('<Control-e>', lambda event, plus_minus=1, step=60: update_step_size(plus_minus, step))

        while pause:
            for x in range(len(bodies)):
                if n_planets+1 >= len(bodies):  # Add color if not enough
                    colors.append("#"+''.join([random.choice('0123456789ABCDEF') for j in range(6)]))
                # Draw Planets
                xy = point_reduced(bodies[x].location)
                canvas.create_oval(xy[0]-5, xy[1]-5, xy[0]+5, xy[1]+5, outline=colors[x], fill=colors[x], tag='cel_body')

                # Update planet location, get line coords
                linecoords = bodies[x].body_update(step_size)

                # Draw line where planets passed
                for i in range(len(lines) - len(lines) % n_planets):
                    if lines[i] is None:
                        lines[i] = canvas.create_line(point_reduced(linecoords[0]), point_reduced(linecoords[1]), fill=colors[x])
                        break

            for x in bodies:  # Update planet vectors
                x.vector_update(bodies, step_size)

            try:  # Canvas Update
                canvas.update()
                canvas.update_idletasks()
            except:
                break

            # Planet Delete
            if pause:
                canvas.delete('cel_body')
            # Line Delete
            if n_planets:
                if lines[len(lines) - len(lines) % n_planets - 1] is not None:
                    for i in range(line_group_index * n_planets, (line_group_index + 1) * n_planets):
                        canvas.delete(lines[i])
                        lines[i] = None
                    line_group_index += 1
                    if len(lines) - len(lines) % n_planets < (line_group_index + 1) * n_planets:
                        line_group_index = 0

            # Step increment
            step_count += 1
            elapsed_time += step_size
            info_one_var.set('Step ID: {:5n} | Elapsed time: {:50}'.format(step_count, format_time(elapsed_time)))
            info_two_var.set('Step size: {:50}'.format(format_time(step_size)))

            # Beware this is negative. Only check the % difference from the initial state.
            initial_energy_level = calculate_system_energy(bodies)
            # print(initial_energy_level)

        try:  # Canvas Update
            canvas.update()
            canvas.update_idletasks()
        except:
            break
