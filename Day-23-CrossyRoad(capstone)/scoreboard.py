from turtle import Turtle

FONT = ("Courier", 24, "normal")

class Scoreboard(Turtle):
    def __init__(self):
        super().__init__()
        self.level = 0
        self.hideturtle()
        self.penup()
        self.update_scoreboard()

    def update_scoreboard(self):
        self.color("white")
        self.clear()
        self.level += 1
        self.goto(-220, 250)
        self.write(f"Level: {self.level}", align="center", font=FONT)

    def game_over(self):
        self.color("white")
        self.penup()
        self.home()
        self.write("GAME OVER", align="center", font=FONT)
