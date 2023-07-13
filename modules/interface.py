from tkinter import Tk, StringVar, Label, OptionMenu, Button, Entry, Listbox, Checkbutton, IntVar
from modules.bot_system import Bot
from modules.macros import Macro
from modules.functions import MouseCommand, KeyboardCommand, ConditionalCommand
from modules.mouse_bot import mousePos
from pyautogui import sleep
from modules.keyboard_bot import whenPressed
from threading import Thread

class Application():
    def __init__(self, bot: Bot) -> None:
        self.bot = bot
        self.__execute_undefined = False
        self.window = Tk()
        self.configureWindow()
        self.commandListActualization()
        self.__hotkey_set = [False for i in range(5)]
        self.window.mainloop()

    def configureWindow(self) -> None:
        if self.bot.get_path() == "":
            self.window.title("bot")
        else:
            self.window.title("Bot - "+self.bot.get_path()[8:-4])
        self.window.configure(background = '#1e3743')
        self.window.resizable(False, False)
        self.window.minsize(width=400, height=800)

        self.lista_comandos = Listbox(master=self.window)
        self.lista_comandos.place(relx=0.02,rely=0.08,relwidth=0.96,relheight=0.40)

        self.botao_salvar = Button(master=self.window,text="Salvar", command=self.__save)
        self.botao_salvar.place(relx=0.02,rely=0.93,relwidth=0.47,relheight=0.05)

        self.botao_salvar_como = Button(master=self.window,text="Salvar Como",command=self.saveScript)
        self.botao_salvar_como.place(relx=0.51,rely=0.93,relwidth=0.47,relheight=0.05)

        self.botao_carregar_script = Button(master=self.window,text="Carregar Script",command=self.loadScript)
        self.botao_carregar_script.place(relx=0.02,rely=0.86,relwidth=0.96,relheight=0.05)

        self.botao_editar_comando = Button(master=self.window,text="Editar Comando",command=self.__editCommand)
        self.botao_editar_comando.place(relx=0.02,rely=0.57,relwidth=0.47,relheight=0.05)

        self.checkbutton_executar_loop = Checkbutton(master=self.window,text="Executar em loop",command=self.__executeUndefinedChangeStatus)
        self.checkbutton_executar_loop.place(relx=0.51,rely=0.5,relwidth=0.47,relheight=0.05)

        self.botao_executar_script = Button(master=self.window,text="Executar Script",command=self.__executeScript)
        self.botao_executar_script.place(relx=0.02,rely=0.5,relwidth=0.47,relheight=0.05)

        self.botao_inserir_pausa = Button(master=self.window,text="Adicionar Pausa",command=self.__insertPause)
        self.botao_inserir_pausa.place(relx=0.51,rely=0.57,relwidth=0.47,relheight=0.05)

        self.botao_comando_mouse = Button(master=self.window,text="Comando Mouse",command=self.__mouseCommand)
        self.botao_comando_mouse.place(relx=0.02,rely=0.63,relwidth=0.47,relheight=0.05)

        self.botao_comando_teclado = Button(master=self.window,text="Comando Teclado",command=self.__keyboardCommand)
        self.botao_comando_teclado.place(relx=0.51,rely=0.63,relwidth=0.47,relheight=0.05)

        self.botao_carregar_comandos = Button(master=self.window,text="Carregar Comandos",command=self.loadCommands)
        self.botao_carregar_comandos.place(relx=0.51,rely=0.69,relwidth=0.47,relheight=0.05)

        self.botao_apagar_comando = Button(master=self.window,text="Apagar Comando",command=self.__deleteCommand)
        self.botao_apagar_comando.place(relx=0.02,rely=0.69,relwidth=0.47,relheight=0.05)

        self.botao_limpar_configuracoes = Button(master=self.window,text="Limpar Configuracoes",command=self.__limpar_config)
        self.botao_limpar_configuracoes.place(relx=0.02,rely=0.77,relwidth=0.47,relheight=0.05)

        self.botao_hotkeys = Button(master=self.window,text="Hotkeys",command=self.__hotkeys)
        self.botao_hotkeys.place(relx=0.51,rely=0.77,relwidth=0.47,relheight=0.05)

        self.botao_config = Button(master=self.window,text="Configurações",command=self.__configuration)
        self.botao_config.place(relx=0.02,rely=0.02,relwidth=0.96,relheight=0.05)

    def __saveConfiguration(self):
        self.bot.default_pause_time = float(self.entry_tempo_padrado.get())
        self.bot.default_noise_time = float(self.entry_ruido_tempo.get())
        self.bot.default_noise_pixel = int(self.entry_ruido_tela.get())
        self.bot.default_stop_key = self.entry_stopkey.get()
        self.bot.configure()
        self.configure.destroy()

    def __mouseCommand(self):
        self.mouse = Tk()
        self.mouse.title("Adicionar comando de mouse")
        self.mouse.configure(background = '#1e3743')
        self.mouse.resizable(False, False)
        self.mouse.minsize(width=400, height=400)

        self.comando = StringVar()
        lista_comandos = [
            "Click",
            "Multi-Click",
            "Navegar",
            "Arrastar",
            "Click Direito",
            "Clicar Aqui",
            "Mover Aqui"
        ]
        self.comando.set("Click")

        self.texto_erro = Label(master=self.mouse,text="",background='#1e3743',fg="red")
        self.texto_erro.place(relx=0.5,rely=0.7,anchor="center")
        
        self.menu_comandos_mouse = OptionMenu(self.mouse,self.comando,*lista_comandos,command=self.__alternateMouseCommandSelection)
        self.menu_comandos_mouse.place(relx=0.3,rely=0.05,relwidth=0.4,relheight=0.09)

        self.texto_pos = Label(master=self.mouse,text="Aperte 'p' para mostrar a posição do mouse",background='#1e3743',fg="white")
        self.texto_pos.place(relx=0.5,rely=0.95,anchor="center")

        whenPressed("p", lambda atualizar: self.texto_pos.configure(text=str(mousePos())))
        whenPressed("enter", lambda atualizar: self.__confirmMouseCommand())
        self.mouse.mainloop()
    
    def __confirmMouseCommand(self):
        if self.comando.get() == "Click":
            try:
                self.bot.createMouseCommand(1,[int(self.entry_posx.get()),int(self.entry_posy.get())])
                self.mouse.destroy()
            except Exception as erro:
                self.texto_erro.configure(text=str(erro))
        if self.comando.get() == "Multi-Click":
            try:
                self.bot.createMouseCommand(2,[int(self.entry_posx.get()),int(self.entry_posy.get()),int(self.entry_quantidade.get())])
                self.mouse.destroy()
            except Exception as erro:
                self.texto_erro.configure(text=str(erro))
        if self.comando.get() == "Navegar":
            try:
                self.bot.createMouseCommand(4,[int(self.entry_posx.get()),int(self.entry_posy.get())])
                self.mouse.destroy()
            except Exception as erro:
                self.texto_erro.configure(text=str(erro))
        if self.comando.get() == "Arrastar":
            try:
                self.bot.createMouseCommand(5,[int(self.entry_posx_fin.get()),int(self.entry_posy_fin.get()),int(self.entry_posx.get()),int(self.entry_posy.get()),float(self.bot.default_pause_time)])
                self.mouse.destroy()
            except Exception as erro:
                self.texto_erro.configure(text=str(erro))
        if self.comando.get() == "Click Direito":
            try:
                self.bot.createMouseCommand(6,[int(self.entry_posx.get()),int(self.entry_posy.get())])
                self.mouse.destroy()
            except Exception as erro:
                self.texto_erro.configure(text=str(erro))
        if self.comando.get() == "Clicar Aqui":
            try:
                self.bot.createMouseCommand(7,[mousePos[0],mousePos[1]])
                self.mouse.destroy()
            except Exception as erro:
                self.texto_erro.configure(text=str(erro))
        if self.comando.get() == "Mover Aqui":
            try:
                self.bot.createMouseCommand(5,[int(self.entry_posx_fin.get()),int(self.entry_posy_fin.get())])
                self.mouse.destroy()
            except Exception as erro:
                self.texto_erro.configure(text=str(erro))
        self.commandListActualization()

    def __alternateMouseCommandSelection(self, selection):
        self.texto_erro.configure(text="")
        try:
            self.texto_posx.destroy()
            self.entry_posx.destroy()
            self.texto_posy.destroy()
            self.entry_posy.destroy()
        except:
            pass
        try:
            self.texto_quantidade.destroy()
            self.entry_quantidade.destroy()
        except:
            pass
        try:
            self.texto_aperte_enter.destroy()
        except:
            pass
        try:
            self.texto_posx_fin.destroy()
            self.entry_posx_fin.destroy()
            self.texto_posy_fin.destroy()
            self.entry_posy_fin.destroy()
        except:
            pass
        
        self.button_confirmar = Button(master=self.mouse,text="Confirmar",command=self.__confirmMouseCommand)
        self.button_confirmar.place(relx=0.3,rely=0.8,relwidth=0.4)
        
        if self.comando.get() in ["Click", "Multi-Click", "Navegar", "Arrastar", "Click Direito"]:
            self.texto_posx = Label(master=self.mouse,text="Posição X:",background='#1e3743',fg="white")
            self.texto_posx.place(relx=0.05, rely=0.2)
            
            self.entry_posx = Entry(master=self.mouse)
            self.entry_posx.place(relx=0.6, rely=0.2, relwidth=0.35)

            self.texto_posy = Label(master=self.mouse,text="Posição Y:",background='#1e3743',fg="white")
            self.texto_posy.place(relx=0.05, rely=0.3)
            
            self.entry_posy = Entry(master=self.mouse)
            self.entry_posy.place(relx=0.6, rely=0.3, relwidth=0.35)

        if self.comando.get() == "Multi-Click":
            self.texto_quantidade = Label(master=self.mouse,text="Quantidade de repetições:",background='#1e3743',fg="white")
            self.texto_quantidade.place(relx=0.05, rely=0.4)
            
            self.entry_quantidade = Entry(master=self.mouse)
            self.entry_quantidade.place(relx=0.6, rely=0.4, relwidth=0.35)

        if self.comando.get() in ["Arrastar", "Mover Aqui"]:
            self.texto_posx_fin = Label(master=self.mouse,text="Posição X final:",background='#1e3743',fg="white")
            self.texto_posx_fin.place(relx=0.05, rely=0.4)
            
            self.entry_posx_fin = Entry(master=self.mouse)
            self.entry_posx_fin.place(relx=0.6, rely=0.4, relwidth=0.35)

            self.texto_posy_fin = Label(master=self.mouse,text="Posição Y final:",background='#1e3743',fg="white")
            self.texto_posy_fin.place(relx=0.05, rely=0.5)
            
            self.entry_posy_fin = Entry(master=self.mouse)
            self.entry_posy_fin.place(relx=0.6, rely=0.5, relwidth=0.35)

            if self.comando.get() == "Mover Aqui":
                self.texto_aperte_enter = Label(master=self.mouse,text="Essa função arrasta o click da posição que\no mouse estiver para a posição informada",background='#1e3743',fg="white")
                self.texto_aperte_enter.place(relx=0.5,rely=0.3,anchor="center")

        if self.comando.get() == "Clicar Aqui":
            self.texto_aperte_enter = Label(master=self.mouse,text="Posicione o mouse na posição de click\ne tecle Enter para confirmar",background='#1e3743',fg="white")
            self.texto_aperte_enter.place(relx=0.5,rely=0.3,anchor="center")
            
    def __keyboardCommand(self):
        self.keyboard = Tk()
        self.keyboard.title("Adicionar comando de teclado")
        self.keyboard.configure(background = '#1e3743')
        self.keyboard.resizable(False, False)
        self.keyboard.minsize(width=400, height=400)

        self.comando = StringVar()
        lista_comandos = [
            "Apertar Tecla",
            "Teclar Múltiplo",
            "Escrever Texto",
            "Segurar Tecla",
            "Soltar Tecla"
        ]
        self.comando.set("Apertar Tecla")

        self.texto_erro = Label(master=self.keyboard,text="",background='#1e3743',fg="red")
        self.texto_erro.place(relx=0.5,rely=0.7,anchor="center")
        
        self.menu_comandos_teclado = OptionMenu(self.keyboard,self.comando,*lista_comandos,command=self.__alternateKeyboardCommandSelection)
        self.menu_comandos_teclado.place(relx=0.3,rely=0.05,relwidth=0.4,relheight=0.09)
        
        whenPressed("enter", lambda atualizar: self.__confirmKeyboardCommand())
        self.keyboard.mainloop()

    def __alternateKeyboardCommandSelection(self, selection):
        self.texto_erro.configure(text="")

        try:
            self.texto_texto.destroy()
            self.texto_texto.destroy()
            self.texto_quantidade.destroy()
            self.entry_quantidade.destroy()
            self.texto_tempo.destroy()
            self.entry_tempo.destroy()
        except:
            pass
        
        if self.comando.get() in ["Apertar Tecla", "Segurar Tecla", "Soltar Tecla"]:
            self.texto_texto = Label(master=self.keyboard,text="Tecla:",background='#1e3743',fg="white")
            self.texto_texto.place(relx=0.05, rely=0.2)
            
            self.entry_texto = Entry(master=self.keyboard)
            self.entry_texto.place(relx=0.6, rely=0.2, relwidth=0.35)

        if self.comando.get() == "Escrever Texto":
            self.texto_texto = Label(master=self.keyboard,text="Texto:",background='#1e3743',fg="white")
            self.texto_texto.place(relx=0.05, rely=0.2)
            
            self.entry_texto = Entry(master=self.keyboard)
            self.entry_texto.place(relx=0.6, rely=0.2, relwidth=0.35)

        if self.comando.get() == "Teclar Múltiplo":
            self.texto_texto = Label(master=self.keyboard,text="Tecla:",background='#1e3743',fg="white")
            self.texto_texto.place(relx=0.05, rely=0.2)
            
            self.entry_texto = Entry(master=self.keyboard)
            self.entry_texto.place(relx=0.6, rely=0.2, relwidth=0.35)

            self.texto_quantidade = Label(master=self.keyboard,text="Quant. clicks:",background='#1e3743',fg="white")
            self.texto_quantidade.place(relx=0.05, rely=0.3)
            
            self.entry_quantidade = Entry(master=self.keyboard)
            self.entry_quantidade.place(relx=0.6, rely=0.3, relwidth=0.35)

            self.texto_tempo = Label(master=self.keyboard,text="Tempo Execução:",background='#1e3743',fg="white")
            self.texto_tempo.place(relx=0.05, rely=0.4)
            
            self.entry_tempo = Entry(master=self.keyboard)
            self.entry_tempo.place(relx=0.6, rely=0.4, relwidth=0.35)


        self.button_confirmar = Button(master=self.keyboard,text="Confirmar",command=self.__confirmKeyboardCommand)
        self.button_confirmar.place(relx=0.3,rely=0.8,relwidth=0.4)

    def __confirmKeyboardCommand(self):
        if self.comando.get() == "Apertar Tecla":
            try:
                self.bot.createKeyboardCommand(1,[self.entry_texto.get()])
                self.keyboard.destroy()
            except Exception as erro:
                self.texto_erro.configure(text=str(erro))
        if self.comando.get() == "Teclar Múltiplo":
            try:
                self.bot.createKeyboardCommand(2,[self.entry_texto.get(),int(self.entry_quantidade.get()),float(self.entry_tempo.get())])
                self.keyboard.destroy()
            except Exception as erro:
                self.texto_erro.configure(text=str(erro))
        if self.comando.get() == "Escrever Texto":
            try:
                self.bot.createKeyboardCommand(3,[self.entry_texto.get()])
                self.keyboard.destroy()
            except Exception as erro:
                self.texto_erro.configure(text=str(erro))
        if self.comando.get() == "Segurar Tecla":
            try:
                self.bot.createKeyboardCommand(5,[self.entry_texto.get()])
                self.keyboard.destroy()
            except Exception as erro:
                self.texto_erro.configure(text=str(erro))
        if self.comando.get() == "Soltar Tecla":
            try:
                self.bot.createKeyboardCommand(6,[self.entry_texto.get()])
                self.keyboard.destroy()
            except Exception as erro:
                self.texto_erro.configure(text=str(erro))
        
        self.commandListActualization()

    def __configuration(self):
        self.configure = Tk()
        self.configure.title("Configurações")
        self.configure.configure(background = '#1e3743')
        self.configure.resizable(False, False)
        self.configure.minsize(width=400, height=400)

        self.botao_salvar_configuracoes = Button(master=self.configure,text="Salvar Configuracoes",command=self.__saveConfiguration)
        self.botao_salvar_configuracoes.place(relx=0.02,rely=0.88,relwidth=0.96,relheight=0.09)

        self.texto_tempo_padrão = Label(master=self.configure, text="Tempo de pausa padrão:",background='#1e3743',fg="white")
        self.texto_tempo_padrão.place(relx=0.02,rely=0.05)

        self.entry_tempo_padrado = Entry(master=self.configure)
        self.entry_tempo_padrado.insert(0,str(self.bot.default_pause_time))
        self.entry_tempo_padrado.place(relx=0.55,rely=0.05,relwidth=0.33,relheight=0.09)

        self.texto_unidade_tempo_padrão = Label(master=self.configure, text="sec",background='#1e3743',fg="white")
        self.texto_unidade_tempo_padrão.place(relx=0.9,rely=0.05)

        self.texto_ruido_tempo = Label(master=self.configure, text="Ruído de tempo padrão:",background='#1e3743',fg="white")
        self.texto_ruido_tempo.place(relx=0.02,rely=0.15)

        self.entry_ruido_tempo = Entry(master=self.configure)
        self.entry_ruido_tempo.insert(0,str(self.bot.default_noise_time))
        self.entry_ruido_tempo.place(relx=0.55,rely=0.15,relwidth=0.33,relheight=0.09)

        self.texto_unidade_ruido_tempo = Label(master=self.configure, text="ms",background='#1e3743',fg="white")
        self.texto_unidade_ruido_tempo.place(relx=0.9,rely=0.15)

        self.texto_ruido_tela = Label(master=self.configure, text="Ruído de tela padrão:",background='#1e3743',fg="white")
        self.texto_ruido_tela.place(relx=0.02,rely=0.25)

        self.entry_ruido_tela = Entry(master=self.configure)
        self.entry_ruido_tela.insert(0,str(self.bot.default_noise_pixel))
        self.entry_ruido_tela.place(relx=0.55,rely=0.25,relwidth=0.33,relheight=0.09)

        self.texto_unidade_ruido_tela = Label(master=self.configure, text="px",background='#1e3743',fg="white")
        self.texto_unidade_ruido_tela.place(relx=0.9,rely=0.25)

        self.texto_stopkey = Label(master=self.configure, text="Tecla de parada:",background='#1e3743',fg="white")
        self.texto_stopkey.place(relx=0.02,rely=0.35)

        self.entry_stopkey = Entry(master=self.configure)
        self.entry_stopkey.insert(0,str(self.bot.default_stop_key))
        self.entry_stopkey.place(relx=0.55,rely=0.35,relwidth=0.33,relheight=0.09)

        self.configure.mainloop()

    def __editCommand(self):
        edit_index = self.lista_comandos.curselection()

    def __deleteCommand(self):
        lista_de_comandos = list(reversed(self.lista_comandos.curselection()))
        for comandoIndex in lista_de_comandos:
            self.bot.deleteCommand(comandoIndex)
        self.commandListActualization()

    def loadCommands(self):
        self.load = Tk()
        self.load.title("Adicionar comandos")
        self.load.configure(background = '#1e3743')
        self.load.resizable(False, False)
        self.load.minsize(width=400, height=200)

        self.texto_nome = Label(master=self.load,text="Nome do arquivo:",background='#1e3743',fg="white")
        self.texto_nome.place(relx=0.5, rely=0.1, anchor="center")

        self.texto_mcr = Label(master=self.load,text=".mcr",background='#1e3743',fg="white")
        self.texto_mcr.place(relx=0.85, rely=0.2)

        self.texto_time = Label(master=self.load,text="Hora",background='#1e3743',fg="white")
        self.texto_time.place(relx=0.1, rely=0.4)
            
        self.entry_path = Entry(master=self.load)
        self.entry_path.place(relx=0.1, rely=0.2, relwidth=0.725)
            
        self.entry_time = Entry(master=self.load)
        self.entry_time.place(relx=0.32, rely=0.4, relwidth=0.5)

        self.button_confirmar = Button(master=self.load,text="Confirmar",command=self.__confirmLoadCommands)
        self.button_confirmar.place(relx=0.3,rely=0.75,relwidth=0.4)

        self.texto_erro = Label(master=self.load,text="",background='#1e3743',fg="red")
        self.texto_erro.place(relx=0.5,rely=0.65,anchor="center")

        self.load.mainloop()

    def __confirmLoadCommands(self):
        try:
            if self.entry_time.get() == "":
                self.bot.loadMacroAsCommand("scripts\\"+self.entry_path.get()+".mcr")
            else:
                self.bot.createConditionalCommand(self.entry_time.get(), self.entry_path.get())
            self.commandListActualization()
            self.load.destroy()
        except Exception as erro:
            self.texto_erro.configure(text=erro)

    def loadScript(self):
        self.load = Tk()
        self.load.title("Carregar Script")
        self.load.configure(background = '#1e3743')
        self.load.resizable(False, False)
        self.load.minsize(width=400, height=200)

        self.texto_nome = Label(master=self.load,text="Nome do arquivo:",background='#1e3743',fg="white")
        self.texto_nome.place(relx=0.5, rely=0.2, anchor="center")

        self.texto_mcr = Label(master=self.load,text=".mcr",background='#1e3743',fg="white")
        self.texto_mcr.place(relx=0.85, rely=0.4)
            
        self.entry_path = Entry(master=self.load)
        self.entry_path.place(relx=0.1, rely=0.4, relwidth=0.725)

        self.button_confirmar = Button(master=self.load,text="Confirmar",command=self.__confirmLoadScript)
        self.button_confirmar.place(relx=0.3,rely=0.75,relwidth=0.4)

        self.texto_erro = Label(master=self.load,text="",background='#1e3743',fg="red")
        self.texto_erro.place(relx=0.5,rely=0.65,anchor="center")

        self.load.mainloop()

    def __confirmLoadScript(self):
        try:
            self.bot.selectMacro("scripts\\"+self.entry_path.get()+".mcr")
            self.commandListActualization()
            self.window.title("Bot - "+self.entry_path.get())
            self.load.destroy()
        except Exception as erro:
            self.texto_erro.configure(text=erro)

    def saveScript(self):
        self.save = Tk()
        self.save.title("Salvar Script")
        self.save.configure(background = '#1e3743')
        self.save.resizable(False, False)
        self.save.minsize(width=400, height=200)

        self.texto_nome = Label(master=self.save,text="Nome do arquivo:",background='#1e3743',fg="white")
        self.texto_nome.place(relx=0.5, rely=0.2, anchor="center")

        self.texto_mcr = Label(master=self.save,text=".mcr",background='#1e3743',fg="white")
        self.texto_mcr.place(relx=0.85, rely=0.4)
            
        self.entry_path = Entry(master=self.save)
        self.entry_path.place(relx=0.1, rely=0.4, relwidth=0.725)

        self.button_confirmar = Button(master=self.save,text="Salvar",command=self.__confirmSaveScript)
        self.button_confirmar.place(relx=0.3,rely=0.75,relwidth=0.4)

        self.texto_erro = Label(master=self.save,text="",background='#1e3743',fg="red")
        self.texto_erro.place(relx=0.5,rely=0.65,anchor="center")

    def __confirmSaveScript(self):
        try:
            self.bot.macroSave("scripts\\"+self.entry_path.get()+".mcr")
            self.commandListActualization()
            self.window.title("Bot - "+self.entry_path.get())
            self.save.destroy()
        except Exception as erro:
            self.texto_erro.configure(text=erro)

    def __save(self):
        path = self.bot.get_path()
        if path == "":
            self.saveScript()
        else:
            self.bot.macroSave(path)

    def __executeUndefinedChangeStatus(self):
        self.__execute_undefined = not self.__execute_undefined

    def __executeScript(self):
        def execute():
            if self.__execute_undefined:
                self.bot.executeMacroUndefined(self.bot.default_stop_key)
            else:
                self.bot.executeMacro(self.bot.default_stop_key)

        Thread(target=execute,args=[]).start()

    def __insertPause(self):
        self.bot.createPauseCommand(self.bot.default_pause_time)
        self.commandListActualization()

    def commandListActualization(self):       
        command_list = self.bot.getCommandList()
        self.lista_comandos.delete(0, self.lista_comandos.size()) 
        for command_index in range(len(command_list)):
            if type(command_list[command_index]) == Macro:
                command_text = command_list[command_index].getPath()
            elif isinstance(command_list[command_index], ConditionalCommand):
                command_text = str(command_list[command_index])
            else:
                command_text = ""
                if isinstance(command_list[command_index], MouseCommand):
                    command_text += "Mouse "
                elif isinstance(command_list[command_index], KeyboardCommand):
                    command_text += "Teclado "
                else:
                    command_text += "Pausa "
                command_text += str(command_list[command_index].getParameters())
            self.lista_comandos.insert(command_index, command_text)

    def __hotkeys(self) -> None:
        self.hotkey = Tk()
        self.hotkey.title("Hotkeys")
        self.hotkey.configure(background = '#1e3743')
        self.hotkey.resizable(False, False)
        self.hotkey.minsize(width=400, height=400)
        macros = self.bot.getMacroPress()
        print(macros)

        self.texto_hotkey = Label(master=self.hotkey, text="Key",background='#1e3743',fg="white")
        self.texto_hotkey.place(relx=0.15,rely=0.065)

        self.texto_macro = Label(master=self.hotkey, text="Macro",background='#1e3743',fg="white")
        self.texto_macro.place(relx=0.55,rely=0.065)

        self.checkbutton_hotkey_0 = Checkbutton(master=self.hotkey,background='#1e3743',command=self.__hotkeyChecking0)
        if macros[0][0]:
            self.checkbutton_hotkey_0.select()
        self.checkbutton_hotkey_0.place(relx=0.02,rely=0.15,relwidth=0.065,relheight=0.075)
        
        self.entry_hotkey_0 = Entry(master=self.hotkey)
        self.entry_hotkey_0.insert(0,macros[1][0])
        self.entry_hotkey_0.place(relx=0.1,rely=0.15,relwidth=0.2,relheight=0.07)

        self.entry_macro_0 = Entry(master=self.hotkey)
        self.entry_macro_0.insert(0,macros[2][0].getPath()[8:-4])
        self.entry_macro_0.place(relx=0.33,rely=0.15,relwidth=0.6,relheight=0.07)

        self.checkbutton_hotkey_1 = Checkbutton(master=self.hotkey,background='#1e3743',command=self.__hotkeyChecking1)
        if macros[0][1]:
            self.checkbutton_hotkey_1.select()
        self.checkbutton_hotkey_1.place(relx=0.02,rely=0.25,relwidth=0.065,relheight=0.075)
        
        self.entry_hotkey_1 = Entry(master=self.hotkey)
        self.entry_hotkey_1.insert(0,macros[1][1])
        self.entry_hotkey_1.place(relx=0.1,rely=0.25,relwidth=0.2,relheight=0.07)

        self.entry_macro_1 = Entry(master=self.hotkey)
        self.entry_macro_1.insert(0,macros[2][1].getPath()[8:-4])
        self.entry_macro_1.place(relx=0.33,rely=0.25,relwidth=0.6,relheight=0.07)

        self.checkbutton_hotkey_2 = Checkbutton(master=self.hotkey,background='#1e3743',command=self.__hotkeyChecking2)
        if macros[0][2]:
            self.checkbutton_hotkey_2.select()
        self.checkbutton_hotkey_2.place(relx=0.02,rely=0.35,relwidth=0.065,relheight=0.075)
        
        self.entry_hotkey_2 = Entry(master=self.hotkey)
        self.entry_hotkey_2.insert(0,macros[1][2])
        self.entry_hotkey_2.place(relx=0.1,rely=0.35,relwidth=0.2,relheight=0.07)

        self.entry_macro_2 = Entry(master=self.hotkey)
        self.entry_macro_2.insert(0,macros[2][2].getPath()[8:-4])
        self.entry_macro_2.place(relx=0.33,rely=0.35,relwidth=0.6,relheight=0.07)

        self.checkbutton_hotkey_3 = Checkbutton(master=self.hotkey,background='#1e3743',command=self.__hotkeyChecking3)
        if macros[0][3]:
            self.checkbutton_hotkey_3.select()
        self.checkbutton_hotkey_3.place(relx=0.02,rely=0.45,relwidth=0.065,relheight=0.075)
        
        self.entry_hotkey_3 = Entry(master=self.hotkey)
        self.entry_hotkey_3.insert(0,macros[1][3])
        self.entry_hotkey_3.place(relx=0.1,rely=0.45,relwidth=0.2,relheight=0.07)

        self.entry_macro_3 = Entry(master=self.hotkey)
        self.entry_macro_3.insert(0,macros[2][3].getPath()[8:-4])
        self.entry_macro_3.place(relx=0.33,rely=0.45,relwidth=0.6,relheight=0.07)

        self.checkbutton_hotkey_4 = Checkbutton(master=self.hotkey,background='#1e3743',command=self.__hotkeyChecking4)
        if macros[0][4]:
            self.checkbutton_hotkey_4.select()
        self.checkbutton_hotkey_4.place(relx=0.02,rely=0.55,relwidth=0.065,relheight=0.075)
        
        self.entry_hotkey_4 = Entry(master=self.hotkey)
        self.entry_hotkey_4.insert(0,macros[1][4])
        self.entry_hotkey_4.place(relx=0.1,rely=0.55,relwidth=0.2,relheight=0.07)

        self.entry_macro_4 = Entry(master=self.hotkey)
        self.entry_macro_4.insert(0,macros[2][4].getPath()[8:-4])
        self.entry_macro_4.place(relx=0.33,rely=0.55,relwidth=0.6,relheight=0.07)

        self.hotkey.mainloop()

    def __hotkeyChecking0(self) -> None:
        self.__hotkey_set[0] = not self.__hotkey_set[0]
        self.__hotkeyChecking()

    def __hotkeyChecking1(self) -> None:
        self.__hotkey_set[1] = not self.__hotkey_set[1]
        self.__hotkeyChecking()

    def __hotkeyChecking2(self) -> None:
        self.__hotkey_set[2] = not self.__hotkey_set[2]
        self.__hotkeyChecking()

    def __hotkeyChecking3(self) -> None:
        self.__hotkey_set[3] = not self.__hotkey_set[3]
        self.__hotkeyChecking()

    def __hotkeyChecking4(self) -> None:
        self.__hotkey_set[4] = not self.__hotkey_set[4]
        self.__hotkeyChecking()

    def __hotkeyChecking(self) -> None:
        print(self.__hotkey_set[0])
        try:
            if self.__hotkey_set[0]:
                self.bot.loadMacroPress("scripts\\"+self.entry_macro_0.get()+".mcr", 0)
                self.bot.macroPressKey(self.entry_hotkey_0.get(),0)
                self.bot.macroPressSetState(True, 0)
            else:
                self.bot.macroPressSetState(False, 0)
        except:
            self.bot.macroPressSetState(False, 0)

        try:
            if self.__hotkey_set[1]:
                self.bot.loadMacroPress("scripts\\"+self.entry_macro_1.get()+".mcr", 1)
                self.bot.macroPressKey(self.entry_hotkey_1.get(), 1)
                self.bot.macroPressSetState(True, 1)
            else:
                self.bot.macroPressSetState(False, 1)
        except:
            self.bot.macroPressSetState(False, 1)

        try:
            if self.__hotkey_set[2]:
                self.bot.loadMacroPress("scripts\\"+self.entry_macro_2.get()+".mcr", 2)
                self.bot.macroPressKey(self.entry_hotkey_2.get(), 2)
                self.bot.macroPressSetState(True, 2)
            else:
                self.bot.macroPressSetState(False, 2)
        except:
            self.bot.macroPressSetState(False, 2)

        try:
            if self.__hotkey_set[3]:
                self.bot.loadMacroPress("scripts\\"+self.entry_macro_3.get()+".mcr", 3)
                self.bot.macroPressKey(self.entry_hotkey_3.get(), 3)
                self.bot.macroPressSetState(True, 3)
            else:
                self.bot.macroPressSetState(False, 3)
        except:
            self.bot.macroPressSetState(False, 3)

        try:
            if self.__hotkey_set[4]:
                self.bot.loadMacroPress("scripts\\"+self.entry_macro_4.get()+".mcr", 4)
                self.bot.macroPressKey(self.entry_hotkey_4.get(), 4)
                self.bot.macroPressSetState(True, 4)
            else:
                self.bot.macroPressSetState(False, 4)
        except:
            self.bot.macroPressSetState(False, 4)
            
        def save_hotkey(key):
            try:
                whenPressed(key, lambda executing: self.bot.macroPressExecute(key))
            except:
                pass
        save_hotkey(self.entry_hotkey_0.get())
        save_hotkey(self.entry_hotkey_1.get())
        save_hotkey(self.entry_hotkey_2.get())
        save_hotkey(self.entry_hotkey_3.get())
        save_hotkey(self.entry_hotkey_4.get())

    def __limpar_config(self) -> None:
        # press key to stop execution
        KeyboardCommand(5, [self.bot.default_stop_key])
        sleep(1)
        KeyboardCommand(6, [self.bot.default_stop_key])
        self.bot = Bot()
        self.commandListActualization()
        self.window.title("Bot")

def saveSession(bot: Bot) -> None:
    with open("config\last.cfg", "w") as archive:
        archive.write(bot.get_path()+"\n"+str(bot.default_pause_time)+"\n"+str(bot.default_noise_time)+"\n"+str(bot.default_noise_pixel)+"\n"+str(bot.default_stop_key)+"\n")

def loadLastSession(bot: Bot):
    try:
        with open("config\last.cfg", "r") as archive:
            configuration = archive.read().split("\n")
            bot.selectMacro(configuration[0])
            bot.default_pause_time = float(configuration[1])
            bot.default_noise_time = float(configuration[2])
            bot.default_noise_pixel = int(configuration[3])
            bot.default_stop_key = configuration[4]
            bot.configure()
    except:
        pass

def launch(time: float = 0):
    if time > 0:
        creditos = Tk()
        creditos.title("Créditos")
        creditos.configure(background = '#1e3743')
        creditos.resizable(False, False)
        creditos.minsize(width=400, height=200)
        nome = Label(master=creditos,text="Criado por:\nRafael Marinho dos Anjos\n2023",background='#1e3743',fg="white")
        nome.place(relx=0.5,rely=0.5,anchor="center")
        def timer():
            sleep(time)
            creditos.destroy()
        Thread(target=timer).start()
        creditos.mainloop()

    bot = Bot()
    try:
        loadLastSession(bot)
    except:
        pass
    Application(bot)
    saveSession(bot)
    
if __name__ == "__main__":
    launch()