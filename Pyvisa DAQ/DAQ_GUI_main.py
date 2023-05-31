#import tkinter
import customtkinter
import sys
import DAQ_GUI_func as func
import DAQ_GUI_IV as iv
import DAQ_GUI_Spec as spec
import DAQ_GUI_Wf as wf
import lab_module as lm

#Selector apariencia
customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

#Clase para tener un stdout en la aplicacion
class StdoutRedirector(object):
    def __init__(self,text_widget):
        self.text_space = text_widget

    def write(self,string):
        self.text_space.insert('end', string)
        self.text_space.see('end')
    def flush(self):
        pass

class StderrRedirector(object):
    def __init__(self, text_widget):
        self.text_space = text_widget

    def write(self, string):
        self.text_space.insert('end', string, 'error')
        self.text_space.see('end')

    def flush(self):
        pass

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.vValuesAux = customtkinter.StringVar()
        self.iValuesAux = customtkinter.StringVar()
        self.valuesAux = customtkinter.StringVar()
        self.histData = customtkinter.StringVar()
        self.pathWf = customtkinter.StringVar()

        #Titulo ventana
        self.title("SiPMs UGR DAQ")
        self.geometry(f"{1200}x{700}")

        # configure grid layout (4x4)
        self.grid_columnconfigure(0, weight=2)
        self.grid_columnconfigure(1, weight=0)
        self.grid_rowconfigure(0, weight=2)
        self.grid_rowconfigure((1,2,3), weight=0)

        #3 areas de la aplicacion
        # create tabview
        self.tabview = customtkinter.CTkTabview(self, width=250)
        self.tabview.grid(row=0, column=0, padx=(20, 20), pady=(10, 10), sticky="nsew")
        self.tabview.add("IV Curves")
        self.tabview.add("Spectrum")
        self.tabview.add("Waveform")
        self.tabview.tab("IV Curves").grid_columnconfigure(0, weight=0)
        self.tabview.tab("IV Curves").grid_columnconfigure(1, weight=3)  
        self.tabview.tab("IV Curves").grid_rowconfigure(0, weight=1)  # 100% de altura
        self.tabview.tab("Spectrum").grid_columnconfigure(0, weight=0)
        self.tabview.tab("Spectrum").grid_columnconfigure(1, weight=3)  
        self.tabview.tab("Spectrum").grid_rowconfigure(0, weight=1)  # 100% de altura
        self.tabview.tab("Waveform").grid_columnconfigure(0, weight=0)
        self.tabview.tab("Waveform").grid_columnconfigure(1, weight=3)  
        self.tabview.tab("Waveform").grid_rowconfigure(0, weight=1)  # 100% de altura

        # create option frame
        self.option_frame = customtkinter.CTkFrame(self, width=140)
        self.option_frame.grid(row=0, column=1, padx=(0, 20), pady=(30, 20), rowspan=4, sticky="nsew")
        self.option_frame.grid_rowconfigure(4, weight=1)

        # Uppers options from option frame
        self.save_entry = customtkinter.CTkEntry(self.option_frame, placeholder_text="File name..")
        self.save_entry.grid(row=0, column=0, padx=10, pady=(20,10))
        self.save_button = customtkinter.CTkButton(self.option_frame)
        self.save_button.grid(row=1, column=0, padx=10, pady=(10,10))
        self.print_button = customtkinter.CTkButton(self.option_frame)
        self.print_button.grid(row=2, column=0, padx=10, pady=10)
        self.folder_button = customtkinter.CTkButton(self.option_frame)
        self.folder_button.grid(row=3, column=0, padx=10, pady=(10,20))

        # Down options from option frame
        self.appearance_mode_label = customtkinter.CTkLabel(self.option_frame, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=5, column=0, padx=10, pady=(0, 0))
        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.option_frame, values=["Light", "Dark", "System"], command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=6, column=0, padx=10, pady=(0, 5))
        self.scaling_label = customtkinter.CTkLabel(self.option_frame, text="UI Scaling:", anchor="w")
        self.scaling_label.grid(row=7, column=0, padx=10, pady=(5, 0))
        self.scaling_optionemenu = customtkinter.CTkOptionMenu(self.option_frame, values=["80%", "90%", "100%", "110%", "120%"], command=self.change_scaling_event)
        self.scaling_optionemenu.grid(row=8, column=0, padx=10, pady=(0, 100))

        # create textbox
        self.textbox = customtkinter.CTkTextbox(self, width=250)
        self.textbox.grid(row=1, column=0, padx=(20, 20), pady=(10, 20), sticky="nsew")

        spec.settingSpec(self)

        func.plotExampleSpec(self)

        wf.settingWf(self)

        func.plotExampleWf(self)

        iv.settingIV(self)

        func.plotExampleIV(self)

        # set default values
        self.save_button.configure(text="Save results", command=self.saveResults)
        self.print_button.configure(text="Print results", command=self.save_plot_as_png)
        self.folder_button.configure(text="Open folder", command=self.openResults)
        self.appearance_mode_optionemenu.set("System")
        self.scaling_optionemenu.set("100%")
        self.options.set("SMU")
        sys.stdout = StdoutRedirector(self.textbox)
        sys.stderr = StderrRedirector(self.textbox)

    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)

    def startIV(self):
        try:
            func.startIVTEST(self)
            print("IV curve finished")

        except Exception as e:
            print("Error:", e)

        finally:
            # Habilitar el botón Start nuevamente al finalizar
            lm.beep()
            self.start_button.configure(state="normal")

    def saveResults(self):
        func.saveResults(self)

    def openResults(self):
        func.openResults(self)

    def save_plot_as_png(self):
        func.save_plot_as_png(self)

    def startSpectrum(self):
        func.startSpectrum(self)

    def startWf(self):
        func.startWf(self)

app = App()
app.mainloop()