from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
import random

class GuessFootballerApp(App):
    def build(self):
        self.footballers = ["messi", "ronaldo", "mbappe"]  # Add more footballers as needed
        self.current_footballer = None

        self.layout = BoxLayout(orientation='vertical')
        self.image = Image(source='', size_hint=(1, 0.7))
        self.layout.add_widget(self.image)

        self.text_input = TextInput(multiline=False, size_hint=(1, 0.2))
        self.layout.add_widget(self.text_input)

        self.submit_button = Button(text='Submit', on_press=self.check_answer, size_hint=(1, 0.1))
        self.layout.add_widget(self.submit_button)

        self.result_label = Label(text='', size_hint=(1, 0.1))
        self.layout.add_widget(self.result_label)

        self.new_game()

        return self.layout

    def new_game(self):
        self.current_footballer = random.choice(self.footballers)
        self.image.source = f'image/{self.current_footballer}.png'  # Replace with actual image filenames
        self.text_input.text = ''
        self.result_label.text = 'Guess the footballer!'

    def check_answer(self, instance):
        user_input = self.text_input.text.lower()
        if user_input == self.current_footballer:
            self.result_label.text = 'Correct! Well done.'
        else:
            self.result_label.text = f'Incorrect. The correct answer is {self.current_footballer}.'

if __name__ == '__main__':
    GuessFootballerApp().run()


