from kivy.config import Config
Config.set("graphics", "width", "360")
Config.set("graphics", "height", "640")
Config.set("graphics", "resizable", "0")  # not resizable

# 2048 colors (R, G, B, A) — values 0.0 to 1.0
BG_COLOR = (250 / 255, 248 / 255, 239 / 255, 1)       # #faf8ef
GRID_BG = (187 / 255, 173 / 255, 160 / 255, 1)        # #bbada0
EMPTY_CELL = (205 / 255, 193 / 255, 180 / 255, 1)     # #cdc1b4
TEXT_DARK = (119 / 255, 110 / 255, 101 / 255, 1)      # #776e65
TEXT_LIGHT = (249 / 255, 246 / 255, 242 / 255, 1)     # #f9f6f2

# background rgb, text rgb, font size (dp)
TILE_STYLES = {
    2: ((238 / 255, 228 / 255, 218 / 255, 1), TEXT_DARK, 32),
    4: ((237 / 255, 224 / 255, 200 / 255, 1), TEXT_DARK, 32),
    8: ((242 / 255, 177 / 255, 121 / 255, 1), TEXT_LIGHT, 32),
    16: ((245 / 255, 149 / 255, 99 / 255, 1), TEXT_LIGHT, 30),
    32: ((246 / 255, 124 / 255, 95 / 255, 1), TEXT_LIGHT, 30),
    64: ((246 / 255, 94 / 255, 59 / 255, 1), TEXT_LIGHT, 30),
    128: ((237 / 255, 207 / 255, 114 / 255, 1), TEXT_LIGHT, 24),
    256: ((237 / 255, 204 / 255, 97 / 255, 1), TEXT_LIGHT, 24),
    512: ((237 / 255, 200 / 255, 80 / 255, 1), TEXT_LIGHT, 24),
    1024: ((237 / 255, 197 / 255, 63 / 255, 1), TEXT_LIGHT, 18),
    2048: ((237 / 255, 194 / 255, 46 / 255, 1), TEXT_LIGHT, 18),
}
SUPER_STYLE = ((60 / 255, 58 / 255, 50 / 255, 1), TEXT_LIGHT, 16)

from typing import Literal

from game_engine import Game2048

from kivy.app import App
from kivy.core.window import Window
Window.clearcolor = BG_COLOR

Direction = Literal["up", "down", "left", "right"]

# Kivy key codes: arrows + WASD (for desktop testing)
KEY_TO_DIRECTION: dict[int, Direction] = {
    273: "up",
    274: "down",
    276: "left",
    275: "right",
    119: "up",
    115: "down",
    97: "left",
    100: "right",
}

from kivy.metrics import dp
from kivy.graphics import Color, RoundedRectangle
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.widget import Widget


def style_for(value: int):
    if value == 0:
        return EMPTY_CELL, TEXT_DARK, 32
    if value in TILE_STYLES:
        return TILE_STYLES[value]
    return SUPER_STYLE


class Tile(Widget):
    """One cell: empty (0) or a power-of-two tile with a number."""

    def __init__(self, value: int = 0, **kwargs):
        super().__init__(**kwargs)
        self.value = value
        self._label = Label(
            bold=True,
            halign="center",
            valign="middle",
        )
        self._label.bind(size=self._label.setter("text_size"))
        self.add_widget(self._label)
        self.bind(pos=self._sync, size=self._sync)
        self.set_value(value)

    def set_value(self, value: int) -> None:
        self.value = value
        bg, fg, font_px = style_for(value)

        self.canvas.before.clear()
        with self.canvas.before:
            Color(*bg)
            self._rect = RoundedRectangle(
                pos=self.pos,
                size=self.size,
                radius=[dp(4)],
            )

        self._label.text = "" if value == 0 else str(value)
        self._label.color = fg
        self._label.font_size = dp(font_px)
        self._sync()

    def _sync(self, *args) -> None:
        self._rect.pos = self.pos
        self._rect.size = self.size
        self._label.pos = self.pos
        self._label.size = self.size


class GameBoard(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(
            cols=4,
            spacing=dp(10),
            padding=dp(10),
            size_hint=(None, None),
            size=(dp(324), dp(324)),
            **kwargs,
        )
        with self.canvas.before:
            Color(*GRID_BG)
            self._bg = RoundedRectangle(
                pos=self.pos,
                size=self.size,
                radius=[dp(6)],
            )
        self.bind(pos=self._update_bg, size=self._update_bg)

        self._tiles: list[Tile] = []
        for _ in range(16):
            tile = Tile(0)
            self._tiles.append(tile)
            self.add_widget(tile)

        self._update_bg()

    def set_grid(self, grid: list[list[int]]) -> None:
        """Refresh all cells from a 4×4 list (0 = empty)."""
        for r in range(4):
            for c in range(4):
                self._tiles[r * 4 + c].set_value(grid[r][c])

    def _update_bg(self, *args):
        self._bg.pos = self.pos
        self._bg.size = self.size


class app_2048(App):
    def build(self):
        self.title = "2048"
        self.game = Game2048()

        root = BoxLayout(orientation="vertical", padding=dp(16))
        root.add_widget(Widget(size_hint_y=0.3))
        self.board = GameBoard()
        self.board.set_grid(self.game.grid)
        root.add_widget(self.board)
        root.add_widget(Widget(size_hint_y=1))

        self._move_hint = Label(
            text="Arrow keys / WASD — movement coming next",
            font_size=dp(14),
            color=TEXT_DARK,
            size_hint_y=None,
            height=dp(28),
        )
        root.add_widget(self._move_hint)
        return root

    def on_start(self):
        Window.bind(on_key_down=self._on_key_down)

    def on_stop(self):
        Window.unbind(on_key_down=self._on_key_down)

    def _on_key_down(self, _window, key, _scancode, codepoint, modifiers):
        if "ctrl" in modifiers and codepoint == "z":
            self.on_undo()
            return True

        direction = KEY_TO_DIRECTION.get(key)
        if direction is None:
            return False
        self.on_move(direction)
        return True

    def refresh_board(self) -> None:
        self.board.set_grid(self.game.grid)

    def on_undo(self):
        self.game.undo()
        self.refresh_board()
        self._move_hint.text = "Undo"

    def on_move(self, direction: Direction) -> None:
        """Hook for game logic — called when user presses a direction key."""
        self._move_hint.text = f"Last key: {direction}"
        self.game.move(direction)
        self.refresh_board()

