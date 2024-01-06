import kivy
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.clock import Clock
from random import randint

kivy.require('1.11.1')


class Ball(Widget):
    def __init__(self, **kwargs):
        super(Ball, self).__init__(**kwargs)
        self.size = (50, 50)
        self.source = 'ball.png'  # Add an image for the ball
        self.velocity = (4, 0)  # Initial velocity

    def move(self):
        self.pos = (self.pos[0] + self.velocity[0], self.pos[1] + self.velocity[1])

        # Bounce off walls
        if (self.x < 0) or (self.right > self.parent.width):
            self.velocity = (-self.velocity[0], self.velocity[1])

        # Bounce off ceiling and floor
        if (self.y < 0) or (self.top > self.parent.height):
            self.velocity = (self.velocity[0], -self.velocity[1])


class Coin(Widget):
    def __init__(self, **kwargs):
        super(Coin, self).__init__(**kwargs)
        self.size = (40, 40)
        self.source = 'coin.png'  # Add an image for the coin
        self.pos = (randint(0, 400), randint(0, 400))  # Random initial position


class PinballGame(Widget):
    def __init__(self, **kwargs):
        super(PinballGame, self).__init__(**kwargs)
        self.ball = Ball()
        self.coins = [Coin() for _ in range(5)]  # Create 5 coins

        for coin in self.coins:
            self.add_widget(coin)

        self.add_widget(self.ball)

        Clock.schedule_interval(self.update, 1 / 60.)

    def update(self, dt):
        self.ball.move()

        # Check collisions with coins
        coins_to_remove = []
        for coin in self.coins:
            if self.ball.collide_widget(coin):
                coins_to_remove.append(coin)

        for coin in coins_to_remove:
            self.coins.remove(coin)
            self.remove_widget(coin)

        # Check if all coins are collected
        if not self.coins:
            self.add_widget(Label(text="You Win!", font_size=40))
            Clock.unschedule(self.update)  # Stop the game


class PinballApp(App):
    def build(self):
        return PinballGame()


if __name__ == '__main__':
    PinballApp().run()
