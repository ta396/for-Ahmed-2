import random
from (kivy.app) import App  # type: ignore
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition  # type: ignore
from kivy.properties import StringProperty, ListProperty, NumericProperty, BooleanProperty  # type: ignore
from kivy.core.audio import SoundLoader  # type: ignore
from kivy.clock import Clock  # type: ignore


def try_load_sound(path):
    try:
        s = SoundLoader.load(path)
        return s
    except Exception:
        return None


class MenuScreen(Screen):
    pass


class Stage1Screen(Screen):
    target_color = StringProperty('')
    colors = ListProperty(['red', 'green', 'blue', 'yellow', 'purple'])

    def on_enter(self):
        self.new_round()

    def new_round(self):
        self.target_color = random.choice(self.colors)
        # Large prompt
        self.ids.prompt.text = f"Find: {self.target_color.capitalize()}"
        self.ids.feedback.text = ''

    def check_choice(self, color):
        if color == self.target_color:
            self.ids.feedback.text = 'Nice! ✅'
            snd = try_load_sound('assets/success.wav')
            if snd:
                snd.play()
            Clock.schedule_once(lambda dt: setattr(
                self.manager, 'current', 'stage2'), 0.8)
        else:
            self.ids.feedback.text = 'Try again! ✋'
            snd = try_load_sound('assets/error.wav')
            if snd:
                snd.play()


class Stage2Screen(Screen):
    target_shape = StringProperty('')
    shapes = ListProperty(['Circle', 'Square', 'Triangle', 'Star'])

    def on_enter(self):
        self.new_round()

    def new_round(self):
        self.target_shape = random.choice(self.shapes)
        self.ids.prompt.text = f"Tap the {self.target_shape}!"
        self.ids.feedback.text = ''

    def check_choice(self, choice):
        if choice == self.target_shape:
            self.ids.feedback.text = 'Great! ✅'
            snd = try_load_sound('assets/success.wav')
            if snd:
                snd.play()
            Clock.schedule_once(lambda dt: setattr(
                self.manager, 'current', 'stage3'), 0.8)
        else:
            self.ids.feedback.text = 'Not that one — try again!'
            snd = try_load_sound('assets/error.wav')
            if snd:
                snd.play()


class Stage3Screen(Screen):
    target_count = NumericProperty(0)
    current_count = NumericProperty(0)

    def on_enter(self):
        self.start_round()

    def start_round(self):
        self.target_count = random.randint(1, 5)
        self.current_count = 0
        self.ids.prompt.text = f"Tap {self.target_count} animals"
        self.ids.feedback.text = ''
        # Show/enable animal buttons

    def tapped_animal(self):
        self.current_count += 1
        self.ids.counter.text = str(self.current_count)
        snd = try_load_sound('assets/tap.wav')
        if snd:
            snd.play()
        if self.current_count >= self.target_count:
            self.ids.feedback.text = 'Well done! ✅'
            snd2 = try_load_sound('assets/success.wav')
            if snd2:
                snd2.play()
            Clock.schedule_once(lambda dt: setattr(
                self.manager, 'current', 'win'), 0.8)


class WinScreen(Screen):
    pass


class KidGameApp(App):
    big_buttons = BooleanProperty(False)
    high_contrast = BooleanProperty(False)

    def build(self):
        sm = ScreenManager(transition=FadeTransition())
        sm.add_widget(MenuScreen(name='menu'))
        sm.add_widget(Stage1Screen(name='stage1'))
        sm.add_widget(Stage2Screen(name='stage2'))
        sm.add_widget(Stage3Screen(name='stage3'))
        sm.add_widget(WinScreen(name='win'))
        return sm


if __name__ == '__main__':
    KidGameApp().run()
