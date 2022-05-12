from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.textinput import TextInput
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.core.clipboard import Clipboard


kv = Builder.load_file('frontend.kv')


class MainScreen(Screen):
    text_input = TextInput(text="")
    _schedule = None
    _schedule_erase = None
    erase_seconds = 0
    seconds = 300

    def convert_seconds(self, secs):
        """Converts the given amount of seconds into minutes and seconds ~helper function"""
        secs = secs % (24 * 3600)
        secs %= 3600
        minutes = secs // 60
        secs %= 60
        return "%02d:%02d" % (minutes, secs)

    def update_time(self, *args):
        """Updates the timer label and subtracts seconds off the class variable seconds"""
        if self.seconds > 0:
            self.seconds -= 1
            minutes = self.convert_seconds(self.seconds)
            self.ids.timer.text = str(minutes)
            self.ids.message.text = str(self.erase_seconds)

        else:
            self.ids.timer.text = "You Did It!"
            self.ids.message.text = "Your work has been copied to the clipboard, you can paste it" \
                                  " wherever you'd like to save it."
            Clock.schedule_once(self.copy, 0)

    def start_timer(self, *args):
        """Starts the timer and begins the game"""
        if self.seconds == 300:
            if self._schedule:
                self._schedule.cancel()
            self._schedule = Clock.schedule_interval(self.update_time, 1)

    def erase(self, *args):
        if self.seconds != 0:
            if self.erase_seconds <= 4:
                self.erase_seconds += 1
                self.ids.message.text = str(self.erase_seconds)

            else:
                if self._schedule:
                    self._schedule.cancel()
                    self.ids.text_input.select_all()
                    self.ids.text_input.delete_selection()
                    self._schedule_erase.cancel()
                    self.ids.message.text = "Not this time, sorry"

    def stop_erase_timer(self, *args):
        if self._schedule_erase:
            self._schedule_erase.cancel()
            self.ids.message.text = str(self.erase_seconds)
            self._schedule_erase = Clock.schedule_interval(self.erase, 1)
            self.erase_seconds = 0

        else:
            self._schedule_erase = Clock.schedule_interval(self.erase, 1)
            self.erase_seconds = 0
            self.ids.message.text = str(self.erase_seconds)

    def copy(self, *args):
        Clipboard.copy(self.ids.text_input.text)

    def reset(self):
        self.clear_widgets()
        self.add_widget(RootWidget())


class RootWidget(ScreenManager):
    pass


class MainApp(App):

    def build(self):
        return RootWidget()


MainApp().run()
