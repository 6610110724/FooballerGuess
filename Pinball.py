from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.widget import Widget
from kivy.clock import Clock
import random


class StartMenu(Screen):
    def __init__(self, **kwargs):
        super(StartMenu, self).__init__(**kwargs)

        layout = BoxLayout(orientation='vertical')
        self.welcome = Label(text='PINBALL GAME',font_size = 80)
        names_input = TextInput(hint_text="Enter your Name", multiline=False,font_size=60)
        self.name_input = names_input
        self.enter_button = Button(text="SAVE", on_press=self.callback, font_size=60)
        self.enter_button.background_color = (100/255, 255/255, 100/255, 1)
        self.start_button = Button(text="Press to start", on_press=self.go_to_game, font_size=50)
        self.start_button.background_color = (150/255, 205/255, 100/255, 1)


        layout.add_widget(self.welcome)
        layout.add_widget(names_input)
        layout.add_widget(self.enter_button)
        layout.add_widget(self.start_button)

        self.add_widget(layout)

    def go_to_game(self, instance):
        self.manager.current = 'pinball_game'

    def callback(self, instance):
        self.welcome.text = 'Player Name :' + ' ' + self.name_input.text


class PinballGame(Screen):
    def __init__(self, **kwargs):
        super(PinballGame, self).__init__(**kwargs)
        self.is_paused = False

        layout = BoxLayout(orientation='vertical')
        self.pinball_layout = PinballLayout()
        self.exit_button = Button(text='Back to Menu', on_press=self.exit, size_hint_y=None, height=100)
        self.pause_button = Button(text='Pause/Resume', on_press=self.toggle_pause, size_hint_x=None, width=100)
        self.timer_label = Label(text="Time: 120", size_hint_y=None, height=50)

        layout.add_widget(self.pinball_layout)
        layout.add_widget(self.exit_button)
        layout.add_widget(self.pause_button)
        layout.add_widget(self.timer_label)

        self.add_widget(layout)

        Clock.schedule_interval(self.update_timer, 1)
        Clock.schedule_interval(self.update_pinball, 1 / 60.)

    def exit(self, instance):
        self.manager.current = 'start_menu'
        self.is_paused = not self.is_paused

    def toggle_pause(self, instance):
        self.is_paused = not self.is_paused

    def update_timer(self, dt):
        if not self.is_paused:
            remaining_time = int(self.timer_label.text.split()[-1])
            if remaining_time > 0:
                remaining_time -= 1
                self.timer_label.text = f"Time: {remaining_time}"
            else:
                self.show_game_over_popup()

    def update_pinball(self, dt):
        if not self.is_paused:
            pass 
    
    def show_game_over_popup(self):
        popup = Popup(title='Game Over', content=Label(text='Your final score is: TODO'), size_hint=(None, None),
                      size=(400, 200))
        popup.open()


class PinballLayout(Widget):
    pass


class MyApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(StartMenu(name='start_menu'))
        sm.add_widget(PinballGame(name='pinball_game'))
        return sm


if __name__ == '__main__':
    MyApp().run()
