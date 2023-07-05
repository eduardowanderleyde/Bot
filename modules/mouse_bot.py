import pyautogui

def click(posX: int, posY: int) -> None:
    if not pyautogui.onScreen(posX, posY):
        raise ValueError("Click location is out of screen")
    pyautogui.click(x=posX, y=posY)

def multiClick(posX: int, posY: int, clicksNum: int, interval: float = 1) -> None:
    if not pyautogui.onScreen(posX, posY):
        raise ValueError("Click location is out of screen")
    clicksNum -= 1
    for i in range(clicksNum):
        pyautogui.click(x=posX, y=posY)
        pyautogui.sleep(interval/clicksNum)
    pyautogui.click(x=posX, y=posY)

def mousePos() -> tuple:
    pos = pyautogui.position()
    return (pos[0], pos[1])

def navigate(posX: int, posY: int) -> None:
    if not pyautogui.onScreen(posX, posY):
        raise ValueError("Click location is out of screen")
    pyautogui.moveTo(posX,posY)

def mouseDrag(posFinX: int, posFinY: int, posInX: int = mousePos()[0], posInY: int = mousePos()[1], time: float = 1) -> None:
    if not pyautogui.onScreen(x = posInX, y = posInY):
        raise ValueError("Initial mouse position is out of screen")
    if not pyautogui.onScreen(x = posFinX, y = posFinY):
        raise ValueError("Final mouse position is out of screen")
    pyautogui.mouseDown(x = posInX, y = posInY)
    pyautogui.moveTo(x = posFinX, y = posFinY, duration = time)
    pyautogui.mouseUp()

def rightClick(posX: int, posY: int) -> None:
    if not pyautogui.onScreen(posX, posY):
        raise ValueError("Click location is out of screen")
    pyautogui.rightClick(x = posX, y = posY)

if __name__ == "__main__":
    navigate(100,100)