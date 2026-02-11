from turtle import Turtle
import random

COLORS = ["red", "orange", "yellow", "green", "blue", "purple"]
STARTING_MOVE_DISTANCE = 5
MOVE_INCREMENT = 10


class CarManager:
    def __init__(self):
        self.cars = []
        self.car_speed = STARTING_MOVE_DISTANCE

    def create_cars(self):
        if random.randint(1, 7) == 1:
            new_car = Turtle("square")
            new_car.penup()
            new_car.color(random.choice(COLORS))
            new_car.shapesize(1, 2)
            rand_y = -250 + (20 * (random.randint(0, 25)))
            new_car.goto(320, rand_y)
            self.cars.append(new_car)

    def drive(self):
        for car in self.cars:
            car.backward(self.car_speed)

    def level_up(self):
        self.car_speed *= MOVE_INCREMENT