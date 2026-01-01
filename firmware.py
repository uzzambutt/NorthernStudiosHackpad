import board
import busio
import microcontroller
import digitalio
import adafruit_ssd1306
from kmk.kmk_keyboard import KMKKeyboard
from kmk.keys import KC
from kmk.scanners.keypad import KeysScanner
from kmk.modules.layers import Layers

# 1. HARDWARE PIN SETUP (Rotary Encoder)
enc_a = digitalio.DigitalInOut(microcontroller.pin.GPIO0)
enc_b = digitalio.DigitalInOut(microcontroller.pin.GPIO1)
enc_a.direction = digitalio.Direction.INPUT
enc_b.direction = digitalio.Direction.INPUT
enc_a.pull = digitalio.Pull.UP
enc_b.pull = digitalio.Pull.UP

keyboard = KMKKeyboard()

# 2. OLED SETUP
i2c = busio.I2C(microcontroller.pin.GPIO7, microcontroller.pin.GPIO6)
display = adafruit_ssd1306.SSD1306_I2C(128, 32, i2c)

menu_modes = ["1. FLIGHT MODE", "2. RACE MODE", "3. MEDIA MODE"]
current_layer = 0

def update_menu(layer_idx):
    try:
        display.fill(0)
        display.text('--- SIM DECK ---', 15, 0, 1)
        display.text(menu_modes[layer_idx], 20, 15, 1)
        display.text('STATE: ACTIVE', 25, 24, 1)
        display.show()
    except:
        pass

# 3. KEYPAD SETUP (Stability Focus)
# We go back to a standard scan but use the specific GPIOs known to work
keyboard.matrix = KeysScanner(
    pins=[
        microcontroller.pin.GPIO26, microcontroller.pin.GPIO27, 
        microcontroller.pin.GPIO28, microcontroller.pin.GPIO29, 
        microcontroller.pin.GPIO2,  microcontroller.pin.GPIO4, 
        microcontroller.pin.GPIO3
    ],
    value_when_pressed=False,
    pull=True,
)

keyboard.modules = [Layers()]

# 4. KEYMAP
keyboard.keymap = [
    [KC.F13, KC.F14, KC.F15, KC.F16, KC.F17, KC.F18, KC.F19],
    [KC.N1, KC.N2, KC.N3, KC.N4, KC.N5, KC.N6, KC.N7],
    [KC.A, KC.B, KC.C, KC.D, KC.E, KC.F, KC.G]
]

# 5. LATCHED ENCODER LOGIC
last_stable_val = (enc_a.value << 1) | enc_b.value
rotation_count = 0

def master_loop(*args, **kwargs):
    global last_stable_val, current_layer, rotation_count
    
    # Check encoder
    cur_a = enc_a.value
    cur_b = enc_b.value
    current_val = (cur_a << 1) | cur_b
    
    if current_val != last_stable_val:
        state = (last_stable_val << 2) | current_val
        if state in (0b0001, 0b0111, 0b1110, 0b1000):
            rotation_count += 1
        elif state in (0b0010, 0b1011, 0b1101, 0b0100):
            rotation_count -= 1
        last_stable_val = current_val

        if abs(rotation_count) >= 4:
            if rotation_count >= 4:
                current_layer = (current_layer + 1) % 3
            else:
                current_layer = (current_layer - 1) % 3
            
            keyboard.active_layers = [current_layer]
            update_menu(current_layer)
            rotation_count = 0

keyboard.before_matrix_scan = master_loop
update_menu(0)

if __name__ == '__main__':
    keyboard.go()
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
