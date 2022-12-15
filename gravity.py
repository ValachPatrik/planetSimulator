import math
from typing import List

from point import Point, Vector

GRAVITATION_CONSTANT = 6.67430 * 10**(-11)


class Body:
    def __init__(self,
                 location: Point,
                 mass: float,
                 motion_vector: Vector,
                 name: str):

        self.location = location  # location x, y in meters
        self.mass = mass  # mass in kilograms
        self.motion_vector = motion_vector  # meters per second
        self.name = name

    def __str__(self):
        return f"{self.name.ljust(20)}: Location {self.location}; Mass: {round(self.mass, 2)}; Motion vector: {self.motion_vector}"

    __repr__ = __str__

    def body_update(self, step_size: int) -> tuple:
        # set new location for object and return line traveled
        location1 = self.location
        self.location = self.location.__add__(self.motion_vector.__mul__(step_size))
        return (location1, self.location)

    def vector_update(self, bodies, step_size: int):
        # update motion vector based on gravitational pull of other obejcts
        for i in bodies:
            if i != self:
                acceleration_divided = GRAVITATION_CONSTANT * i.mass / i.location.distance(self.location)**3
                self.motion_vector = self.motion_vector.__add__(Vector(acceleration_divided * (i.location.x - self.location.x), acceleration_divided * (i.location.y - self.location.y)).__mul__(step_size))


# --- The following functions are not for the movement itself, but just for validation that the law of conservation of energy roughly holds. ---

def calculate_system_energy(bodies: List[Body]) -> float:
    """
        System energy level is kinetic + potential energy
        IT CAN BE (and often is) NEGATE. It's not meant as an absolute level of energy. Use it only in comparison with
        previously returned values - for example with the initial state.
    """
    kinetic_energy = __calculate_kinetic_energy(bodies)
    potential_energy = __calculate_potential_energy(bodies)  # This is negative.
    total_energy = kinetic_energy + potential_energy
    return total_energy


def __calculate_kinetic_energy(bodies: List[Body]) -> float:
    def kinetic_energy(body: Body):
        return 1/2 * body.mass * (body.motion_vector.x**2 + body.motion_vector.y**2)  # 1/2 * m * v**2

    return sum([kinetic_energy(x) for x in bodies])


def __calculate_potential_energy(bodies: List[Body]) -> float:
    total_potential_energy = 0
    for a in range(len(bodies)):
        for b in range(a + 1, len(bodies)):
            distance = bodies[a].location.distance(bodies[b].location)
            new_potential_energy = - 1 * GRAVITATION_CONSTANT * (bodies[a].mass * bodies[b].mass) * (1.0/distance)
            total_potential_energy += new_potential_energy

    return total_potential_energy
