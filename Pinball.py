from kivy.app import App
import random
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import StringProperty
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from itertools import permutations, product
from kivy.graphics import Ellipse, Color
from kivy.clock import Clock

class StartMenu(Screen):
    def __init__(self, **kwargs):
        super(StartMenu, self).__init__(**kwargs)
        
        layout = BoxLayout(orientation='vertical')
        
        self.welcome = Label(text='PINBALL GAME', font_size='75')
        layout.add_widget(self.welcome)
        
        names_input = TextInput(hint_text="Enter your name", font_size='50', multiline=False)
        self.name_input = names_input
        layout.add_widget(names_input)

        self.button3 = Button(text="START", on_press=self.callback, font_size='50')
        layout.add_widget(self.button3)

        start_button = Button(text='START WITHOUT REGISTERING', on_press=self.go_to_game, font_size='50')
        layout.add_widget(start_button)
        self.add_widget(layout)

    def go_to_game(self, instance):
        self.manager.current = 'pinball_game'

    def callback(self, instance):
        self.welcome.text = 'Player name: ' + self.name_input.text
        self.manager.current = 'pinball_game'

class PinballGame(Screen):
    def __init__(self, start_screen_callback, **kwargs):
        super(PinballGame, self).__init__(**kwargs)

        self.ball_radius = 20
        self.ball_pos = [100, 100]
        self.ball_velocity = [2.5, 2.5]  # Decreased velocity
        self.start_screen_callback = start_screen_callback

        self.score_label = Label(text=f"Score: {self.score}/{self.max_score}", size_hint_y=None, height=44)
        self.remaining_time_label = Label(text=f"Time: {self.remaining_time}s", size_hint_y=None, height=44)
        self.exit_button = Button(text="Exit", on_press=self.exit_game, size_hint_y=None, height=44)
        self.reset_button = Button(text="Reset", on_press=self.reset_game, size_hint_y=None, height=44)

        self.add_widget(self.score_label)
        self.add_widget(self.remaining_time_label)
        self.add_widget(self.exit_button)
        self.add_widget(self.reset_button)
        self.add_widget(self.pause_button)
        self.add_widget(self.stop_button)

        Clock.schedule_once(self.setup_canvas)
        Clock.schedule_interval(self.update, 1 / 60.0)  

    def setup_canvas(self, dt):
        with self.canvas:
            Color(1, 1, 1)
            self.ball = Ellipse(pos=(self.ball_pos[0] - self.ball_radius, self.ball_pos[1] - self.ball_radius),
                                size=(self.ball_radius * 2, self.ball_radius * 2))

    def update(self, dt):
        self.move_ball()

    def move_ball(self):
        self.ball_pos[0] += self.ball_velocity[0]
        self.ball_pos[1] += self.ball_velocity[1]
        if self.ball_pos[0] - self.ball_radius < 0 or self.ball_pos[0] + self.ball_radius > self.width:
            self.ball_velocity[0] *= -1
        if self.ball_pos[1] - self.ball_radius < 0 or self.ball_pos[1] + self.ball_radius > self.height:
            self.ball_velocity[1] *= -1
        self.ball.pos = (self.ball_pos[0] - self.ball_radius, self.ball_pos[1] - self.ball_radius)

    def check_collision(self, touch):
        if (
            self.ball_pos[0] - self.ball_radius < touch.x < self.ball_pos[0] + self.ball_radius
            and self.ball_pos[1] - self.ball_radius < touch.y < self.ball_pos[1] + self.ball_radius
        ):
            # Reset the ball position to the center of the screen
            self.ball_pos = [self.width / 2, self.height / 2]
            self.ball.pos = (self.ball_pos[0] - self.ball_radius, self.ball_pos[1] - self.ball_radius)
            # Start the game or perform any other actions here

    def on_touch_down(self, touch):
        self.check_collision(touch)

    def stop_game(self, button):
        Clock.unschedule(self.update_timer)
        self.remaining_time_label.text = "Time: 0s"
        self.show_game_result()

    def update_timer(self, dt):
        self.remaining_time -= 1
        self.remaining_time_label.text = f"Time: {self.remaining_time}s"

    def reset_game(self, button):
        Clock.unschedule(self.update_timer)
        self.remaining_time_label.text = f"Time: {self.time_limit}s"

class PinballApp(App):
    def build(self):
        sm = ScreenManager()
        start_menu = StartMenu(name='start_menu')
        pinball_game = PinballGame(name='pinball_game', start_screen_callback=start_menu.go_to_game)
        sm.add_widget(start_menu)
        sm.add_widget(pinball_game)
        return sm

if __name__ == '__main__':
    PinballApp().run()