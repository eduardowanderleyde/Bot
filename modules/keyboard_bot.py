import pyautogui
import keyboard

def keyPress(key: str) -> None:
    if key not in pyautogui.KEYBOARD_KEYS:
        ValueError("Selected key are not in keyboard keys list")
    pyautogui.press(key)

def multikeyPress(key: str, times: int, duration: float = 1) -> None:
    if key not in pyautogui.KEYBOARD_KEYS:
        ValueError("Selected key are not in keyboard keys list")
    if times <= 1:
        pyautogui.press(key)
    else:
        times -= 1
        for i in range(times):
            pyautogui.press(key)
            pyautogui.sleep(duration/times)
        pyautogui.press(key)

def writeWord(word: str) -> None:
    pyautogui.write(word)

def isPressed(key: str) -> bool:
    return keyboard.is_pressed(key)

def whenPressed(key: str, function) -> None:
    keyboard.on_press_key(key, function)

def keyDown(key: str) -> None:
    pyautogui.keyDown(key)

def keyUp(key: str) -> None:
    pyautogui.keyUp(key)