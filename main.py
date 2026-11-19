
from kivy.app import App
from kivy.clock import Clock
from kivy.graphics import Color, Rectangle, RoundedRectangle
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
from random import randint, choice


class Game(Widget):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.lane = 1
        self.score = 0
        self.enemies = []
        self.running = False
        self.speed = 280
        Clock.schedule_interval(self.update, 1 / 60)

    def start(self):
        self.lane = 1
        self.score = 0
        self.enemies = []
        self.running = True
        self.draw()

    def move(self, direction):
        if self.running:
            self.lane = max(0, min(2, self.lane + direction))
            self.draw()

    def draw_car(self, x, y, color):
        with self.canvas:
            Color(*color)
            RoundedRectangle(
                pos=(x - 20, y),
                size=(40, 65),
                radius=[8]
            )
            Color(0.6, 0.9, 1, 1)
            Rectangle(
                pos=(x - 13, y + 40),
                size=(26, 15)
            )

    def draw(self):
        self.canvas.clear()
        w, h = self.width, self.height

        with self.canvas:
            Color(0.15, 0.17, 0.19, 1)
            Rectangle(pos=self.pos, size=self.size)

            Color(1, 1, 1, 1)
            for x in [w / 3, 2 * w / 3]:
                for y in range(0, int(h), 100):
                    Rectangle(
                        pos=(x, y),
                        size=(3, 45)
                    )

        lane_x = [w / 6, w / 2, 5 * w / 6]

        for lane, y, color in self.enemies:
            self.draw_car(lane_x[lane], y, color)

        self.draw_car(
            lane_x[self.lane],
            40,
            (0.1, 0.5, 1, 1)
        )

    def update(self, dt):
        if not self.running:
            return

        self.score += dt
        self.spawn_timer = getattr(self, "spawn_timer", 0) + dt

        if self.spawn_timer > 1.2:
            self.spawn_timer = 0
            self.enemies.append([
                randint(0, 2),
                self.height,
                choice([
                    (1, 0.2, 0.1, 1),
                    (0.7, 0.3, 0.9, 1),
                    (1, 0.8, 0.1, 1)
                ])
            ])

        new_enemies = []

        for lane, y, color in self.enemies:
            y -= self.speed * dt

            if lane == self.lane and 40 < y < 105:
                self.running = False

            if y > -70:
                new_enemies.append([lane, y, color])

        self.enemies = new_enemies
        self.draw()


class RacingApp(App):

    def build(self):
        root = FloatLayout()

        self.game = Game(
            size_hint=(1, 0.78),
            pos_hint={"x": 0, "y": 0.20}
        )
        root.add_widget(self.game)

        self.label = Label(
            text="Score: 0",
            size_hint=(1, 0.1),
            pos_hint={"x": 0, "y": 0.90}
        )
        root.add_widget(self.label)

        left = Button(
            text="LEFT",
            size_hint=(0.3, 0.12),
            pos_hint={"x": 0.05, "y": 0.02}
        )

        right = Button(
            text="RIGHT",
            size_hint=(0.3, 0.12),
            pos_hint={"x": 0.65, "y": 0.02}
        )

        start = Button(
            text="START",
            size_hint=(0.3, 0.12),
            pos_hint={"x": 0.35, "y": 0.02}
        )

        left.bind(
            on_press=lambda x: self.game.move(-1)
        )
        right.bind(
            on_press=lambda x: self.game.move(1)
        )
        start.bind(
            on_press=lambda x: self.game.start()
        )

        root.add_widget(left)
        root.add_widget(right)
        root.add_widget(start)

        Clock.schedule_interval(self.refresh, 0.1)

        return root

    def refresh(self, dt):
        self.label.text = (
            "Score: " + str(int(self.game.score * 10))
        )

        if not self.game.running and self.game.score > 0:
            self.label.text += " - GAME OVER"


if __name__ == "__main__":
    RacingApp().run()
