from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import Ellipse, Color
from kivy.clock import Clock
from random import randint

class PinballGame(Widget):
    def __init__(self, **kwargs):
        super(PinballGame, self).__init__(**kwargs)
        self.ball_radius = 20
        self.ball_pos = [100, 100]  # Initial ball position
        self.ball_velocity = [5, 5]  # Initial ball velocity

        with self.canvas:
            Color(1, 1, 1)
            self.ball = Ellipse(pos=(self.ball_pos[0] - self.ball_radius, self.ball_pos[1] - self.ball_radius),
                                size=(self.ball_radius * 2, self.ball_radius * 2))

    def update(self, dt):
        self.move_ball()
        self.check_collision()

    def move_ball(self):
        self.ball_pos[0] += self.ball_velocity[0]
        self.ball_pos[1] += self.ball_velocity[1]

        if self.ball_pos[0] - self.ball_radius < 0 or self.ball_pos[0] + self.ball_radius > self.width:
            self.ball_velocity[0] *= -1
        if self.ball_pos[1] - self.ball_radius < 0 or self.ball_pos[1] + self.ball_radius > self.height:
            self.ball_velocity[1] *= -1

        self.ball.pos = (self.ball_pos[0] - self.ball_radius, self.ball_pos[1] - self.ball_radius)

    def check_collision(self):
        pass

class PinballApp(App):
    def build(self):
        layout = FloatLayout()

        game = PinballGame()
        layout.add_widget(game)

        Clock.schedule_interval(game.update, 1.0 / 60.0)  

        return layout

if __name__ == '__main__':
    PinballApp().run()