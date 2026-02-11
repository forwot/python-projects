import time
from turtle import Screen
from player import Player
from car_manager import CarManager
from scoreboard import Scoreboard

screen = Screen()
screen.bgcolor("black")
screen.title("Crossy Turtle")
screen.setup(width=600, height=600)
screen.tracer(0)

player = Player()
car_manager = CarManager()
scoreboard = Scoreboard()

screen.listen()
screen.onkey(player.up, "Up")

game_is_on = True
while game_is_on:
    time.sleep(0.1)
    screen.update()

    car_manager.create_cars()
    car_manager.drive()

    #detect if player hit car
    for car in car_manager.cars:
        if player.distance(car) < 26:
            scoreboard.game_over()
            game_is_on = False

    #detect successful crossing
    if player.ycor() > 280:
        player.finished()
        scoreboard.update_scoreboard()
        car_manager.level_up()

screen.exitonclick()