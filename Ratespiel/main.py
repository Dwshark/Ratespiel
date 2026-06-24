import random
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition, RiseInTransition
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.popup import Popup
from kivy.clock import Clock
from kivy.metrics import dp
from kivy.properties import StringProperty, ListProperty, NumericProperty, BooleanProperty
from kivy.core.window import Window
from kivy.animation import Animation


WORD_LIST = [
    "PIZZA", "STRAND", "RAKETE", "DRACHE", "ROBOTER",
    "GARTEN", "SCHOKOLADE", "KINO", "WALD", "PIRAT",
    "HAUSBOOT", "EISCREME", "TASCHENLAMPE", "FEUERWEHR", "SCHNEEMANN",
    "WOLKENKRATZER", "ZAHNBÜRSTE", "FLUGZEUG", "KAKTUS", "KUCHEN",
    "BIBLIOTHEK", "KOPFHÖRER", "SCHWIMMBAD", "KAMERA", "TIGER",
    "ELEFANT", "BANANE", "KARTOFFEL", "SCHNECKE", "REGENBOGEN",
    "VULKAN", "SCHMETTERLING", "GOLD", "SILBER", "DIAMANT",
    "KATZE", "HUND", "HAMSTER", "PFERD", "ZOO",
    "KRANKENHAUS", "SCHULE", "BUS", "AUTO", "ZUG",
    "UHR", "HANDY", "COMPUTER", "FERNSEHER", "SPIELKONSOLE",
    "BALL", "TOR", "FUSSBALL", "BASKETBALL", "TENNIS",
    "PARK", "SEE", "BERG", "INSEL", "WÜSTE",
    "PILZ", "BROKKOLI", "APFEL", "ORANGE", "TRAUBE",
    "MAGNET", "LUPE", "TELESKOP", "MIKROSKOP", "KOMPASS",
    "GITARRE", "KLAVIER", "TROMMEL", "GEIGE", "FLÖTE",
    "PIRATENSCHIFF", "SCHATZKARTE", "SCHWERT", "RITTER", "BURG",
    "ZAUBERER", "HEXENBESEN", "TRANK", "KRISTALLKUGEL", "GEIST",
    "ROCKET", "ASTRONAUT", "MOND", "SONNE", "STERN",
    "SCHNEE", "GEWITTER", "WIND", "NEBEL", "REGEN"
]


def choose_secret_count(player_count: int) -> int:
    if player_count <= 3:
        return 1
    elif player_count <= 8:
        return 2
    else:
        return 3


# ---------------------------------------------------------
# STARTSCREEN
# ---------------------------------------------------------
class StartScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        layout = BoxLayout(orientation="vertical", padding=dp(20), spacing=dp(20))

        title = Label(text="Geheimwort-Spiel", font_size="32sp", size_hint=(1, 0.3))
        layout.add_widget(title)

        rules_btn = Button(text="Regeln anzeigen", font_size="20sp", size_hint=(1, 0.2))
        rules_btn.bind(on_release=self.show_rules)
        layout.add_widget(rules_btn)

        start_btn = Button(text="Weiter", font_size="24sp", size_hint=(1, 0.2))
        start_btn.bind(on_release=self.go_next)
        layout.add_widget(start_btn)

        self.add_widget(layout)

    def show_rules(self, instance):
        rules_text = (
            "SPIELREGELN\n\n"
            "• Mindestens 3, maximal 10 Spieler\n"
            "• Jeder Spieler sieht nacheinander ein Wort\n"
            "• Einige Spieler bekommen 'GEHEIM' angezeigt\n"
            "• Diese Spieler müssen das Wort erraten.\n"
            "• Timer läuft.\n"
            "• Danach wird angezeigt, wer GEHEIM war.\n"
        )

        content = BoxLayout(orientation="vertical", padding=dp(10), spacing=dp(10))

        rules_label = Label(
            text=rules_text,
            font_size="18sp",
            halign="left",
            valign="top"
        )
        rules_label.bind(size=lambda *x: rules_label.setter("text_size")(rules_label, rules_label.size))

        close_btn = Button(text="Zurück", size_hint=(1, 0.2), font_size="20sp")

        content.add_widget(rules_label)
        content.add_widget(close_btn)

        popup = Popup(title="Regeln", content=content, size_hint=(0.9, 0.9))
        close_btn.bind(on_release=popup.dismiss)
        popup.open()

    def go_next(self, instance):
        self.manager.current = "time"


# ---------------------------------------------------------
# ZEITWAHL SCREEN
# ---------------------------------------------------------
class TimeSelectScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        layout = BoxLayout(orientation="vertical", padding=dp(20))

        title = Label(text="Spielzeit wählen", font_size="30sp", size_hint=(1, 0.2))
        layout.add_widget(title)

        btn1 = Button(text="Schnelles Spiel (1 Minute)", font_size="22sp", size_hint=(1, 0.2))
        btn1.bind(on_release=lambda x: self.set_time(60))
        layout.add_widget(btn1)

        btn2 = Button(text="Normales Spiel (3 Minuten)", font_size="22sp", size_hint=(1, 0.2))
        btn2.bind(on_release=lambda x: self.set_time(180))
        layout.add_widget(btn2)

        btn3 = Button(text="Langes Spiel (5 Minuten)", font_size="22sp", size_hint=(1, 0.2))
        btn3.bind(on_release=lambda x: self.set_time(300))
        layout.add_widget(btn3)

        self.add_widget(layout)

    def set_time(self, seconds):
        app = App.get_running_app()
        app.selected_time = seconds
        self.manager.current = "setup"


# ---------------------------------------------------------
# NAMENSEINGABE
# ---------------------------------------------------------
class PlayerSetupScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        root = BoxLayout(orientation="vertical", padding=dp(10), spacing=dp(10))

        title = Label(text="Spieler eingeben", font_size="28sp", size_hint=(1, 0.1))
        root.add_widget(title)

        self.inputs_layout = GridLayout(cols=2, size_hint=(1, 0.65), spacing=dp(5))
        self.name_inputs = []

        for i in range(10):
            lbl = Label(text=f"Spieler {i+1}:", font_size="16sp")
            ti = TextInput(multiline=False, font_size="16sp")
            self.inputs_layout.add_widget(lbl)
            self.inputs_layout.add_widget(ti)
            self.name_inputs.append(ti)

        root.add_widget(self.inputs_layout)

        self.info_label = Label(text="", font_size="14sp", size_hint=(1, 0.1))
        root.add_widget(self.info_label)

        btn_anchor = AnchorLayout(size_hint=(1, 0.15))
        start_btn = Button(text="Spiel starten", font_size="22sp", size_hint=(0.6, 1))
        start_btn.bind(on_release=self.on_prepare)
        btn_anchor.add_widget(start_btn)
        root.add_widget(btn_anchor)

        self.add_widget(root)

    def on_prepare(self, instance):
        names = [ti.text.strip() for ti in self.name_inputs if ti.text.strip()]

        if len(names) < 3:
            self.info_label.text = "Mindestens 3 Spieler eingeben."
            return

        word = random.choice(WORD_LIST)
        secret_count = choose_secret_count(len(names))
        secret_indices = random.sample(range(len(names)), secret_count)

        app = App.get_running_app()
        app.player_names = names
        app.secret_indices = secret_indices
        app.secret_word = word
        app.player_order = list(range(len(names)))
        app.current_player_index = 0

        self.manager.current = "reveal"


# ---------------------------------------------------------
# CHARACTER MIT ANIMATION
# ---------------------------------------------------------
class DraggableCharacter(RelativeLayout):
    word = StringProperty("")
    show_word = BooleanProperty(False)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self._center_y_down = 0.55
        self._center_y_up = 0.78

        self.img = Image(
            source="character.png",
            allow_stretch=True,
            keep_ratio=True,
            size_hint=(0.9, 0.55),
            pos_hint={"center_x": 0.5, "center_y": self._center_y_down}
        )
        self.add_widget(self.img)

        self.word_label = Label(
            text="",
            font_size="28sp",
            size_hint=(1, 0.15),
            pos_hint={"center_x": 0.5, "center_y": 0.30},
            halign="center",
            valign="middle",
            opacity=0
        )
        self.add_widget(self.word_label)

        self._touch_active = False
        self._start_y = 0

        self.bind(show_word=self.on_show_word_change)

    def on_show_word_change(self, instance, value):
        Animation.cancel_all(self.word_label)
        if value:
            self.word_label.text = self.word
            self.word_label.opacity = 0
            Animation(opacity=1, duration=0.2).start(self.word_label)
        else:
            anim = Animation(opacity=0, duration=0.2)
            anim.bind(on_complete=lambda *x: setattr(self.word_label, "text", ""))
            anim.start(self.word_label)

    def _set_img_center_y(self, value):
        Animation.cancel_all(self.img)
        anim = Animation(pos_hint={"center_x": 0.5, "center_y": value}, duration=0.15, t="out_quad")
        anim.start(self.img)

    def on_touch_down(self, touch):
        if self.img.collide_point(*touch.pos):
            self._touch_active = True
            self._start_y = touch.y
            return True
        return super().on_touch_down(touch)

    def on_touch_move(self, touch):
        if self._touch_active:
            dy = touch.y - self._start_y

            if dy > 40:
                self._set_img_center_y(self._center_y_up)
                self.show_word = True

            return True
        return super().on_touch_move(touch)

    def on_touch_up(self, touch):
        if self._touch_active:
            self._touch_active = False
            self._set_img_center_y(self._center_y_down)
            self.show_word = False
            return True
        return super().on_touch_up(touch)


# ---------------------------------------------------------
# REVEAL SCREEN
# ---------------------------------------------------------
class RevealScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        layout = BoxLayout(orientation="vertical", padding=dp(10), spacing=dp(10))

        self.player_label = Label(text="", font_size="24sp", size_hint=(1, 0.15))
        layout.add_widget(self.player_label)

        self.character = DraggableCharacter(size_hint=(1, 0.75))
        layout.add_widget(self.character)

        self.next_button = Button(text="Nächster Spieler", size_hint=(1, 0.1))
        self.next_button.bind(on_release=self.on_next)
        layout.add_widget(self.next_button)

        self.add_widget(layout)

    def on_pre_enter(self, *args):
        self.update_for_current_player()

    def update_for_current_player(self):
        app = App.get_running_app()
        idx = app.current_player_index
        player_idx = app.player_order[idx]
        name = app.player_names[player_idx]

        self.player_label.text = f"Spieler: {name}"

        # ⭐ KORREKTUR: Bildnummer basiert auf idx, nicht player_idx
        bild_nummer = idx + 1
        self.character.img.source = f"bild{bild_nummer}.png"

        if player_idx in app.secret_indices:
            self.character.word = "GEHEIM"
        else:
            self.character.word = app.secret_word

        self.character.show_word = False
        self.character._set_img_center_y(self.character._center_y_down)

        if idx == len(app.player_order) - 1:
            self.next_button.text = "Spiel starten"
        else:
            self.next_button.text = "Nächster Spieler"

    def on_next(self, instance):
        app = App.get_running_app()
        if app.current_player_index < len(app.player_order) - 1:
            app.current_player_index += 1
            self.update_for_current_player()
        else:
            self.manager.current = "game"


# ---------------------------------------------------------
# GAME SCREEN
# ---------------------------------------------------------
class GameScreen(Screen):
    remaining_time = NumericProperty(10)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        layout = BoxLayout(orientation="vertical", padding=dp(10), spacing=dp(10))

        self.info_label = Label(
            text="Beschreibt das Wort!\nGeheim-Spieler müssen es erraten.",
            font_size="18sp",
            halign="center",
            valign="middle",
            size_hint=(1, 0.3),
        )
        layout.add_widget(self.info_label)

        self.timer_label = Label(text="", font_size="40sp", size_hint=(1, 0.4))
        layout.add_widget(self.timer_label)

        self.add_widget(layout)
        self._event = None

    def on_pre_enter(self, *args):
        Window.keep_screen_on = True

        app = App.get_running_app()
        self.remaining_time = app.selected_time
        self.update_timer_label()
        self._event = Clock.schedule_interval(self.tick, 1)

    def on_leave(self, *args):
        Window.keep_screen_on = False

        if self._event:
            self._event.cancel()
            self._event = None

    def tick(self, dt):
        self.remaining_time -= 1
        if self.remaining_time <= 0:
            self.remaining_time = 0
            self.update_timer_label()
            self.manager.current = "result"
        else:
            self.update_timer_label()

    def update_timer_label(self):
        m = self.remaining_time // 60
        s = self.remaining_time % 60
        self.timer_label.text = f"{m:02d}:{s:02d}"

        # ⭐ Farbwechsel je nach verbleibender Zeit
        if self.remaining_time > 30:
            self.timer_label.color = (0, 1, 0, 1)  # Grün
        elif self.remaining_time > 10:
            self.timer_label.color = (1, 1, 0, 1)  # Gelb
        else:
            self.timer_label.color = (1, 0, 0, 1)  # Rot



# ---------------------------------------------------------
# RESULT SCREEN
# ---------------------------------------------------------
class ResultScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        layout = BoxLayout(orientation="vertical", padding=dp(10), spacing=dp(10))

        self.title_label = Label(text="Ergebnis", font_size="26sp", size_hint=(1, 0.2))
        layout.add_widget(self.title_label)

        self.result_label = Label(text="", font_size="18sp", size_hint=(1, 0.5))
        layout.add_widget(self.result_label)

        btns = BoxLayout(size_hint=(1, 0.3), spacing=dp(10))

        repeat_btn = Button(text="Spiel wiederholen")
        repeat_btn.bind(on_release=self.on_repeat)
        btns.add_widget(repeat_btn)

        new_btn = Button(text="Neu starten")
        new_btn.bind(on_release=self.on_new)
        btns.add_widget(new_btn)

        exit_btn = Button(text="Beenden")
        exit_btn.bind(on_release=self.on_exit)
        btns.add_widget(exit_btn)

        layout.add_widget(btns)
        self.add_widget(layout)

    def on_pre_enter(self, *args):
        app = App.get_running_app()
        secret_names = [app.player_names[i] for i in app.secret_indices]

        text = f"Das geheime Wort war:\n[b]{app.secret_word}[/b]\n\n"
        text += "Folgende Spieler hatten 'GEHEIM':\n"
        for n in secret_names:
            text += f"- {n}\n"

        self.result_label.markup = True
        self.result_label.text = text

    def on_repeat(self, instance):
        app = App.get_running_app()
        app.secret_word = random.choice(WORD_LIST)
        app.secret_indices = random.sample(
            range(len(app.player_names)),
            choose_secret_count(len(app.player_names))
        )
        app.player_order = list(range(len(app.player_names)))
        app.current_player_index = 0
        self.manager.current = "reveal"

    def on_new(self, instance):
        self.manager.current = "setup"

    def on_exit(self, instance):
        App.get_running_app().stop()


# ---------------------------------------------------------
# APP
# ---------------------------------------------------------
class GeheimwortApp(App):
    player_names = ListProperty([])
    secret_indices = ListProperty([])
    secret_word = StringProperty("")
    player_order = ListProperty([])
    current_player_index = NumericProperty(0)
    selected_time = NumericProperty(60)

    def build(self):
        sm = ScreenManager(transition=RiseInTransition(duration=0.45))
        sm.add_widget(StartScreen(name="start"))
        sm.add_widget(TimeSelectScreen(name="time"))
        sm.add_widget(PlayerSetupScreen(name="setup"))
        sm.add_widget(RevealScreen(name="reveal"))
        sm.add_widget(GameScreen(name="game"))
        sm.add_widget(ResultScreen(name="result"))
        sm.current = "start"
        return sm


if __name__ == "__main__":
    GeheimwortApp().run()
