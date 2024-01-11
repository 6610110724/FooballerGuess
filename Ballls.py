from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.graphics import Ellipse, Color
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout

class StartScreen(Screen):
    def __init__(self, start_game_callback, **kwargs):
        super(StartScreen, self).__init__(**kwargs)

        self.orientation = 'vertical'

        title_label = Label(text='Pinball Game', font_size='75sp', size_hint=(1, 0.5))
        start_button = Button(text='Start Game', font_size='35sp', size_hint=(1, 0.5), color='red')
        start_button.bind(on_press=start_game_callback)

        self.add_widget(title_label)
        self.add_widget(start_button)

class PinballGame(Screen):
    def __init__(self, start_screen_callback, game_over_callback, **kwargs):
        super(PinballGame, self).__init__(**kwargs)
        self.ball_radius = 20
        self.ball_pos = [100, 100]
        self.ball_velocity = [5, 5]
        self.start_screen_callback = start_screen_callback
        self.game_over_callback = game_over_callback

        with self.canvas:
            Color(1, 1, 1)
            self.ball = Ellipse(pos=(self.ball_pos[0] - self.ball_radius, self.ball_pos[1] - self.ball_radius),
                                size=(self.ball_radius * 2, self.ball_radius * 2))

        exit_layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.1))
        exit_button = Button(text='Exit Game', on_press=self.exit)
        exit_layout.add_widget(exit_button)
        self.add_widget(exit_layout)

    def exit(self, instance):
        app = App.get_running_app()
        sm = app.root
        sm.current = 'start_menu'

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

    def on_touch_down(self, touch):
        pass


class PinballApp(App):
    def build(self):
        sm = ScreenManager()

        start_screen = StartScreen(name='start_menu', start_game_callback=self.start_game)
        game = PinballGame(name='game_screen', start_screen_callback=self.show_start_screen,
                           game_over_callback=self.show_game_over)

        sm.add_widget(start_screen)
        sm.add_widget(game)


        return sm

    def start_game(self, instance):
        sm = self.root
        sm.current = 'game_screen'

        Clock.schedule_interval(sm.get_screen('game_screen').update, 1.0 / 60.0)

    def show_start_screen(self):
        sm = self.root
        sm.current = 'start_menu'

    def show_game_over(self):
        sm = self.root
        sm.current = 'game_over_screen'

class MyApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(StartScreen(name='start_menu'))
        sm.add_widget(PinballGame(name='PinballGame'))

        return sm

if __name__ == '__main__':
    MyApp().run()