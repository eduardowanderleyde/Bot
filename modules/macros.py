from modules.functions import Command, MouseCommand, KeyboardCommand
import modules.keyboard_bot as keyboard_bot
from pyautogui import sleep
from random import randint

class Macro():
    __commandList = []
    __path = ""
    __sleepTime = 1 # The number of secconds who will pass after a Command
                    # be executed until the next be called.
    default_noise_time = 0
    default_noise_pixel = 0

    def definePath(self, path: str) -> None:
        self.__path = path

    def getPath(self) -> str:
        return self.__path
    
    def getSleep(self) -> float:
        return self.__sleepTime
    
    def setSleep(self, sleep: float) -> None:
        self.__sleepTime = sleep

    def executeMacro(self, stopKey: str = None) -> None:
        stop = [False]
        keyboard_bot.whenPressed(stopKey, lambda exit: stop.insert(0, True))
        for command in self.__commandList:
            if stop[0]:
                break
            command.default_noise_time = self.default_noise_time
            command.default_noise_pixel = self.default_noise_pixel
            if isinstance(command, Command):
                command.call()
            # A Macro object can contains other Macro loaded inside,
            # if it happens, the Macro inside will be executed between
            # the other Commands who are loaded with inside the outer
            # Macro.
            elif isinstance(command, Macro):
                command.executeMacro(stopKey)
            sleep(self.__sleepTime + randint(-self.default_noise_time,self.default_noise_time)/1000)

    def executeMacroOnLoop(self, stopKey: str) -> None:
        stop = [False]
        keyboard_bot.whenPressed(stopKey, lambda exit: stop.insert(0, True))
        while not stop[0]:
            self.executeMacro(stopKey)

    def insertCommand(self, command: Command, index: int = "last") -> None:
        if index == "last":
            self.__commandList.append(command)
        elif index == "first":
            self.__commandList.insert(0, command)
        else:
            self.__commandList.insert(index, command)

    def removeCommand(self, index: int = -1) -> None:
        del self.__commandList[index]

    def changeCommand(self, newCommand: Command, index: int) -> None:
        self.__commandList[index] = newCommand

    def alterCommand(self, type: int, parameters: list, index: int) -> None:
        self.__commandList[index].setCommand(type, parameters)

    def commandStrIterate(self) -> Command:
        for command in self.__commandList:
            yield command

    def macroClear(self) -> None:
        self.__commandList = []

    def __str__(self) -> str:
        return "macro " + self.__path
    
    def getCommandList(self) -> list:
        return self.__commandList
