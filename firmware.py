import board
from kmk.kmk_keyboard import KMKKeyboard
from kmk.keys import KC
from kmk.scanners import DiodeOrientation
from kmk.scanners.keypad import KeysScanner
from kmk.modules.layers import Layers
from kmk.modules.encoder import EncoderHandler
from kmk.extensions.display import Display, TextEntry, ImageEntry

keyboard = KMKKeyboard()

# Northern Studios Pinout
# SW1=D0, SW2=D1, SW3=D2, SW4=D3
# SW5=D8, SW6=D9, SW7=D10 (Mode Button)
PINS = [
    board.D0, board.D1, board.D2, board.D3, # Left Side Buttons
    board.D8, board.D9, board.D10           # Right Side Buttons
]

keyboard.matrix = KeysScanner(
    pins=PINS,
    value_when_pressed=False, 
    pull=True,                
    interval=0.02,            # Debounce time
)

# --- 2. MODULES ---
layers = Layers()
keyboard.modules.append(layers)

encoder_handler = EncoderHandler()
keyboard.modules.append(encoder_handler)

# --- OLED DISPLAY CONFIG ---
# (Pins D4/SDA and D5/SCL) 
display = Display(
    display_signal=board.I2C(),
    font='kmk/extensions/display/font.bdf',
    brightness=0.8,
)

# Screen Layers 
display.entries.append(TextEntry(text='NORTHERN PAY', x=0, y=0, layer=0))
display.entries.append(TextEntry(text='FLIGHT SIM', x=0, y=0, layer=1))
display.entries.append(TextEntry(text='RACING SIM', x=0, y=0, layer=2))

keyboard.extensions.append(display)

# --- 4. KEYMAPS ---
# KEY LAYOUT:
# [SW1] [SW2] [SW3] [SW4]
# [SW5] [SW6] [SW7]

# Layer 0: MENU / SELECTION
# Layer 1: FLIGHT MODE
# Layer 2: RACING MODE

keyboard.keymap = [
    # LAYER 0 (Menu)
    [
        KC.NO,    KC.NO,    KC.NO,    KC.NO,
        KC.TO(1), KC.TO(2), KC.NO,
    ],

    # LAYER 1 (Flight Sim)
    # SW7 acts as "Exit to Menu"
    [
        KC.G,      KC.F,      KC.L,      KC.B,      # Gear, Flaps, Lights, Batt
        KC.A,      KC.E,      KC.TO(0),             # AP, Engine, BACK TO MENU
    ],

    # LAYER 2 (Racing Sim)
    # SW7 acts as "Exit to Menu"
    [
        KC.P,      KC.W,      KC.L,      KC.I,      # Pit, Wipers, Lights, Ignition
        KC.S,      KC.T,      KC.TO(0),             # Starter, TC, BACK TO MENU
    ]
]

# --- ENCODER MAPPING ---
# Pins: A=D6 (TX), B=D7 (RX)
encoder_handler.pins = ((board.D6, board.D7, None),)

encoder_handler.map = [
    # Layer 0 (Menu): Volume Control
    ((KC.VOLU, KC.VOLD),),
    
    # Layer 1 (Flight): Comms / Heading (Left/Right Arrows)
    ((KC.RIGHT, KC.LEFT),),
    
    # Layer 2 (Racing): Brake Bias (Square Brackets)
    ((KC.RBRC, KC.LBRC),),
]

if __name__ == '__main__':
    keyboard.go()
