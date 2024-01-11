from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import Ellipse, Color
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen


class StartScreen(BoxLayout):
    def __init__(self, start_game_callback, **kwargs):
        super(StartScreen, self).__init__(**kwargs)

        self.orientation = 'vertical'

        title_label = Label(text='Pinball Game', font_size='75sp', size_hint=(1, 0.5))
        start_button = Button(text='Start Game', font_size='35sp', size_hint=(1, 0.5), color='red')
        start_button.bind(on_press=start_game_callback)

        self.add_widget(title_label)
        self.add_widget(start_button)


class GameOverScreen(BoxLayout):
    def __init__(self, restart_game_callback, **kwargs):
        super(GameOverScreen, self).__init__(**kwargs)

        self.orientation = 'vertical'

        title_label = Label(text='Game Over', font_size='30sp', size_hint=(1, 0.5))
        restart_button = Button(text='Restart', size_hint=(1, 0.5))
        restart_button.bind(on_press=restart_game_callback)

        self.add_widget(title_label)
        self.add_widget(restart_button)


class PinballGame(Widget):
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
        app.root.current_screen.manager.current = 'start_menu'

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
        # Implement collision detection and response logic here
        pass

    def on_touch_down(self, touch):
        # Implement touch event handling here
        pass


class PinballApp(App):
    def build(self):
        # Screen Manager
        sm = ScreenManager()

        # Start Screen
        start_screen = Screen(name='start_menu')
        start_layout = FloatLayout()
        start_screen_widget = StartScreen(start_game_callback=self.start_game)
        start_layout.add_widget(start_screen_widget)
        start_screen.add_widget(start_layout)
        sm.add_widget(start_screen)

        # Game Screen
        game_screen = Screen(name='game')
        game_layout = FloatLayout()
        game_screen_widget = PinballGame(start_screen_callback=self.show_start_screen, game_over_callback=self.show_game_over)
        game_layout.add_widget(game_screen_widget)
        game_screen.add_widget(game_layout)
        sm.add_widget(game_screen)

        # Game Over Screen
        game_over_screen = Screen(name='game_over')
        game_over_layout = FloatLayout()
        game_over_screen_widget = GameOverScreen(restart_game_callback=self.start_game)
        game_over_layout.add_widget(game_over_screen_widget)
        game_over_screen.add_widget(game_over_layout)
        sm.add_widget(game_over_screen)

        return sm

    def start_game(self, instance):
        self.root.current = 'game'
        Clock.schedule_interval(self.root.current_screen.children[0].update, 1.0 / 60.0)

    def show_start_screen(self):
        self.root.current = 'start_menu'

    def show_game_over(self):
        self.root.current = 'game_over'


if __name__ == '__main__':
    PinballApp().run()