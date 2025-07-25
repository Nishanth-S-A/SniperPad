import board
import busio
import time
from kmk.kmk_keyboard import KMKKeyboard
from kmk.keys import KC
from kmk.keys import Key
from kmk.scanners import DiodeOrientation
from kmk.modules.layers import Layers
from kmk.extensions.media_keys import MediaKeys
from kmk.modules.encoder import EncoderHandler
from kmk.extensions.display import Display, TextEntry
from kmk.extensions.display.ssd1306 import SSD1306
from kmk.extensions.rgb import RGB
from kmk.extensions.rgb import AnimationModes

mapping = {
    "SniperPad (MacOS)": [
        KC.LCMD(KC.C), KC.LCMD(KC.V), KC.LCMD(KC.SPACE),
        KC.MEDIA_REWIND, KC.MEDIA_PLAY_PAUSE, KC.MEDIA_FAST_FORWARD,
    ],
    "SniperPad (Windows)": [
        KC.LCTL(KC.C), KC.LCTL(KC.V), KC.LWIN(KC.S),
        KC.MEDIA_PREV_TRACK, KC.MEDIA_PLAY_PAUSE, KC.MEDIA_NEXT_TRACK,
    ],
}

# Pinout
COL1 = board.D9
COL2 = board.D8
COL3 = board.D7
ROW1 = board.D2
ROW2 = board.D3
PUSHBUTTON = board.D10
ROTA = board.D0
ROTB = board.D1
i2c_bus = busio.I2C(board.SCL, board.SDA)
RGB_INP = board.D6
NUM_PIXELS = 4

# RGBB YAAAYYYY
rgb = RGB(
    pixel_pin=RGB_INP,
    num_pixels=NUM_PIXELS,
    animation_mode=AnimationModes.RAINBOW,
    refresh_rate=60,
    animation_speed=2,
    rgb_order=(1, 0, 2)
)


driver = SSD1306(
    i2c=i2c_bus,
    device_address=0x3C, # This is Default
)

entries = []
for layer, map_name in enumerate(mapping.keys()):
    entries.append(TextEntry(text=map_name, x=64, y=16, y_anchor='M', x_anchor="M", layer=layer))

#Screen
display = Display(
    display=driver,
    entries=entries,
    width=128,
    height=32,
    brightness=1,
)

class LayerKey(Key):
    def __init__(self, default_layer=0):
        self.layer = default_layer
        self.no_of_layers = len(mapping)

    def on_press(self, keyboard, coord_int=None):
        self.layer += 1
        if self.layer >= self.no_of_layers:
            self.layer = 0
        keyboard.add_key(KC.TO(self.layer))

    def on_release(self, keyboard, coord_int=None):
        ...

KC_LAYER = LayerKey()

# Temporary Rotary Code
encoder_handler = EncoderHandler()
encoder_handler.pins = ((ROTA, ROTB, PUSHBUTTON, False),) # PUSHBUTTON or None, False for normal direction
encoder_handler.map = (((KC.VOLD, KC.VOLU, KC_LAYER),),)

keyboard = KMKKeyboard()
keyboard.extensions.append(MediaKeys())
keyboard.extensions.append(rgb)
keyboard.modules.append(encoder_handler)
keyboard.modules.append(Layers())
keyboard.extensions.append(display)

# Matrixuhh MApuh
keyboard.col_pins = (COL1, COL2, COL3)
keyboard.row_pins = (ROW1, ROW2)
keyboard.diode_orientation = DiodeOrientation.COL2ROW

# Keymap
keyboard.keymap = list(mapping.values())

if __name__ == '__main__':
    keyboard.go()