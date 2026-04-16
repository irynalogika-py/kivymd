from kivymd.app import MDApp
from kivymd.uix.widget import MDWidget
from kivymd.uix.screenmanager import MDScreenManager
from kivymd.uix.screen import MDScreen
from kivy.clock import Clock
from kivy.metrics import sp, dp
from kivy import platform
from kivy.core.window import Window
from kivymd.uix.boxlayout import MDBoxLayout

FPS = 60

BULLET_SPEED = dp(10)
SHIP_SPEED = dp(5)


class MainScreen(MDScreen):
    ...


class Shot(MDBoxLayout):
    ...


class GameScreen(MDScreen):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        Clock.schedule_interval(self.update, 1 / FPS)

        self.eventkeys = {}
        self.cartridge = []

    def update(self, dt):
        for key in self.eventkeys:
            if self.eventkeys[key] == True:
                if key == "left":
                    self.moveLeft()
                if key == "right":
                    self.moveRight()
                if key == "shot":
                    self.shot()
                    self.eventkeys[key] = False

        # Керування кулями
        for bullet in self.cartridge:
            bullet.y += BULLET_SPEED

    def pressKey(self, key):
        self.eventkeys[key] = True

    def releaseKey(self, key):
        self.eventkeys[key] = False

    def moveLeft(self):
        if self.ids.ship.x - SHIP_SPEED >= 0:
            self.ids.ship.x -= SHIP_SPEED
        else:
            self.ids.ship.x = 0

    def moveRight(self):
        if self.ids.ship.x + SHIP_SPEED <= self.width - self.ids.ship.width:
            self.ids.ship.x += SHIP_SPEED
        else:
            self.ids.ship.x = self.width - self.ids.ship.width

    def shot(self):
        shot = Shot(pos=(self.ids.ship.center_x - dp(50), self.ids.ship.top - dp(30)))
        self.cartridge.append(shot)
        self.ids.front.add_widget(shot)


class ShooterApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Orange"

        self.sm = MDScreenManager()

        self.sm.add_widget(MainScreen(name="main"))
        self.sm.add_widget(GameScreen(name="game"))

        return self.sm


if platform != "android":
    Window.size = (450, 700)
    Window.top = 100
    Window.left = 600

app = ShooterApp()
app.run()
