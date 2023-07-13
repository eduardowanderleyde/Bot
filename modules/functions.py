import modules.keyboard_bot as keyboard_bot
import modules.mouse_bot as mouse_bot
from pyautogui import sleep
from random import randint

class Command():
    __type = 0        # Integer who will appoint to the command to be executed
    __parameters = [] # list of the parameters who will be called by the command
    default_noise_time = 0
    default_noise_pixel = 0

    def __init__(self, type, parameters) -> None:
        self.__type = type
        self.__parameters = parameters

    def getCommand(self):
        return(self.__type,self.__parameters)
    
    def setCommand(self, type: int, parameters: list) -> None:
        self.__type = type
        self.__parameters = parameters

    def getType(self) -> int:
        return self.__type

    def getParameters(self) -> list:
        return self.__parameters

    def call(self) -> None: # for pause command
        sleep(self.__parameters)

    def __str__(self) -> str:
        return "pauseCommand "+ str(self.__parameters)

class MouseCommand(Command):
    def __init__(self, type: int, parameters: list = None) -> None:
        typeDict = {
            1:"click",
            2:"multiClick",
            3:"mousePos",
            4:"navigate",
            5:"mouseDrag",
            6:"rightClick",
            7:"clickHere",
            8:"moveHere"
        }
        # type = typeDict[type]
        if type == 7:
            type = 1
            parameters = list(mouse_bot.mousePos())
        if type == 8:
            type = 4
            parameters = list(mouse_bot.mousePos())
        super().__init__(type, parameters)

    def call(self):
        parameters = self.getParameters()
        if self.getType() == 1:
            mouse_bot.click(int(parameters[0])+randint(-self.default_noise_pixel,self.default_noise_pixel),int(parameters[1])+randint(-self.default_noise_pixel,self.default_noise_pixel))
        if self.getType() == 2:
            mouse_bot.multiClick(int(parameters[0])+randint(-self.default_noise_pixel,self.default_noise_pixel), int(parameters[1])+randint(-self.default_noise_pixel,self.default_noise_pixel), int(parameters[2]), float(parameters[3]))
        if self.getType() == 3:
            return mouse_bot.mousePos()
        if self.getType() == 4:
            mouse_bot.navigate(int(parameters[0])+randint(-self.default_noise_pixel,self.default_noise_pixel), int(parameters[1])+randint(-self.default_noise_pixel,self.default_noise_pixel))
        if self.getType() == 5:
            mouse_bot.mouseDrag(int(parameters[0])+randint(-self.default_noise_pixel,self.default_noise_pixel), int(parameters[1])+randint(-self.default_noise_pixel,self.default_noise_pixel), int(parameters[2])+randint(-self.default_noise_pixel,self.default_noise_pixel), int(parameters[3])+randint(-self.default_noise_pixel,self.default_noise_pixel), float(parameters[4]))
        if self.getType() == 6:
            mouse_bot.rightClick(int(parameters[0])+randint(-self.default_noise_pixel,self.default_noise_pixel), int(parameters[1])+randint(-self.default_noise_pixel,self.default_noise_pixel))

    def __str__(self) -> str:
        response = "mouse " + str(self.getType())
        for parameter in self.getParameters():
            response += " " + str(parameter)
        return response

class KeyboardCommand(Command):
    def __init__(self, type, parameters) -> None:
        typeDict = {
            1:"keyPress",
            2:"multikeyPress",
            3:"writeWord",
            4:"isPressed",
            5:"Hold",
            6:"Release"
        }
        # type = typeDict[type]
        super().__init__(type, parameters)

    def call(self):
        parameters = self.getParameters()
        if self.getType() == 1:
            keyboard_bot.keyPress(parameters[0])
        if self.getType() == 2:
            keyboard_bot.multikeyPress(parameters[0], int(parameters[1]), float(parameters[2]))
        if self.getType() == 3:
            keyboard_bot.writeWord(parameters[0])
        if self.getType() == 4: # obsoleto, não vale a pena criar um objeto pra isso kkk
            keyboard_bot.isPressed(parameters[0])
        if self.getType() == 5:
            keyboard_bot.keyDown(parameters[0])
        if self.getType() == 6:
            keyboard_bot.keyUp(parameters[0])    

    def __str__(self) -> str:
        response = "keyboard " + str(self.getType())
        for parameter in self.getParameters():
            response += " " + str(parameter)
        return response
    
class ConditionalCommand(Command):
    def __init__(self, condition, time: str, command: Command, path: str) -> None:
        super().__init__("conditionalPlay", [condition, command])
        self.__condition = condition
        self.__command = command
        self.__path = path
        self.__time = time

    def call(self):
        if self.__condition():
            self.__command.executeMacro("q")

    def __str__(self) -> str:
        response = "PlayOnTime " + str([self.__time, self.__path])
        return response

if __name__ == "__main__":
    print(list(mouse_bot.mousePos()))