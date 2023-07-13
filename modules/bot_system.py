from modules.macros import Macro
from modules.functions import Command, KeyboardCommand, MouseCommand, ConditionalCommand
import modules.keyboard_bot as keyboard_bot
from threading import Thread
from datetime import datetime

class Bot():
    __macroAtual = None # Macro who is loaded on main execution of the program
    __macroPress = [Macro() for i in range(5)] # Macros of auto execution when press the respective key
    __hotkeys = ["" for i in range(5)]
    __enableMacroPress = [False for i in range(5)] # Flag of the activation on macroPress
    default_pause_time = 1
    default_noise_time = 0
    default_noise_pixel = 0
    default_stop_key = 'q'

    def __init__(self) -> None:
        self.__macroAtual = Macro()

    def macroLoad(self, path: str) -> Macro:
        macro = Macro()
        macro.macroClear()
        macro.definePath(path)
        with open(path, "r") as archive:
            archive = archive.read().split("\n")
            firstLine = True
            for command in archive:
                if firstLine:
                    macro.setSleep(float(command))
                    firstLine = False
                else:
                    command = str(command).split(" ")
                    try:
                        if command[0] == "keyboard":
                            if command[1] == '3':
                                macro.insertCommand(KeyboardCommand(int(command[1]), [" ".join(command[2:])]))
                            else:
                                macro.insertCommand(KeyboardCommand(int(command[1]), command[2:]))
                        if command[0] == "mouse":
                            macro.insertCommand(MouseCommand(int(command[1]), command[2:]))
                        if command[0] == "macro":
                            macro.insertCommand(self.macroLoad(command[1]))
                        if command[0] == "pauseCommand":
                            macro.insertCommand(Command(0, float(command[1])))
                        if command[0] == "PlayOnTime":
                            macro.insertCommand(ConditionalCommand(lambda: command[1] == str(datetime.now())[11:16],command[1] , self.macroLoad(command[2]), command[2]))
                    except:
                        pass
        return macro

    def macroSave(self, path: str, macro: Macro = None) -> None:
        if macro == None:
            macro = self.__macroAtual
        macro.definePath(path)
        with open(path, "w") as archive:
            archive.write(str(macro.getSleep()))
            for command in macro.commandStrIterate():
                archive.write("\n"+str(command))

    def selectMacro(self, path: str) -> None:
        self.__macroAtual = self.macroLoad(path)

    def runSelectedMacro(self, stopKey: str = None) -> None:
        self.__macroAtual.executeMacro(stopKey)

    def loopRunSelectedMacro(self, stopKey: str = None) -> None:
        self.__macroAtual.executeMacroOnLoop(stopKey)

    def changeMacroPressStatus(self) -> None:
        self.__macroPress = not self.__macroPress

    def createMouseCommand(self, commandType: int, commandParameters: list) -> None:
        self.__macroAtual.insertCommand(MouseCommand(commandType, commandParameters))

    def createKeyboardCommand(self, commandType: int, commandParameters: list) -> None:
        self.__macroAtual.insertCommand(KeyboardCommand(commandType, commandParameters))

    def createConditionalCommand(self, time: str, path: str) -> None:
        path = "scripts\\"+path+".mcr"
        self.__macroAtual.insertCommand(ConditionalCommand(lambda: time == str(datetime.now())[11:16], time, self.macroLoad(path), path))

    def deleteCommand(self, commandIndex: int) -> None:
        self.__macroAtual.removeCommand(commandIndex)

    def alterCommand(self,  type: int, parameters: list, index: int) -> None: # uses less memory than changeCommand()
        self.__macroAtual.alterCommand(type, parameters, index) # for changing Commands of the same type

    def changeCommand(self, command: Command, commandIndex: int) -> None:
        self.__macroAtual.changeCommand(command, commandIndex) # for changing Commands of different types

    def injectCommand(self, command: Command, commandIndex: int) -> None:
        self.__macroAtual.insertCommand(command, commandIndex)

    def createPauseCommand(self, pauseTime: float) -> None:
        self.__macroAtual.insertCommand(Command(0, pauseTime))

    def injectPauseCommand(self, pauseTime: float, index: int) -> None:
        self.__macroAtual.insertCommand(Command(0, pauseTime), index)

    def loadMacroAsCommand(self, path: str) -> None:
        self.__macroAtual.insertCommand(self.macroLoad(path))

    def executeMacro(self, stopKey: str = default_stop_key) -> None:
        self.__macroAtual.executeMacro(stopKey)

    def executeMacroUndefined(self, stopKey: str) -> None:
        self.__macroAtual.executeMacroOnLoop(stopKey)

    def teste(self):
        for command in self.__macroAtual.commandStrIterate():
            print(command)

    def callMacroPress(self):
        for key in self.__macroPress:
            if keyboard_bot.isPressed(key):
                self.__macroPress[key].call()

    def insertMacropress(self, key: str, macro: Macro = None) -> None:
        if macro == None:
            self.__macroPress[key] = self.__macroAtual
        else:
            self.__macroPress[key] = macro

    def macroPressChangeStatus(self) -> None:
        self.__enableMacroPress = self.__enableMacroPress

    def saveMacroPress(self, path: str) -> None:
        with open(path, "w") as archive:
            archive.write("macroPress")
            for key in self.__macroPress:
                archive.write("\n"+key+" "+self.__macroPress[key].getPath())

    def loadMacroPress(self, path: str, index: int) -> None:
        self.__macroPress[index] = self.macroLoad(path)

    def macroPressKey(self, key: str, index: int) -> None:
        self.__hotkeys[index] = key

    def macroPressSetState(self, value: bool, index: int) -> None:
        self.__enableMacroPress[index] = value

    def getMacroPress(self) -> tuple:
        return (self.__enableMacroPress, self.__hotkeys, self.__macroPress)
    
    def macroPressExecute(self, key: str) -> None:
        try:
            index = self.__hotkeys.index(key)
            if self.__enableMacroPress[index]:
                self.__hotkeys[index] = None
                def execute():
                    try:
                        self.__macroPress[index].executeMacro("esc")
                    except:
                        pass
                    self.__hotkeys[index] = key
                Thread(target=execute,args=[]).start()
        except:
            pass

    def get_path(self) -> str:
        return self.__macroAtual.getPath()

    def configure(self):
        # sets the noise of timers and mouse commands position, for anti-detection
        # sets the standart pause time of the macro
        self.__macroAtual.default_noise_time = self.default_noise_time
        self.__macroAtual.default_noise_pixel = self.default_noise_pixel

    def getCommandList(self) -> list:
        return self.__macroAtual.getCommandList()