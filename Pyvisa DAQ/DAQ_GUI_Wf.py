import customtkinter as ctk
import DAQ_GUI_func as func
import os

def settingWf(self):

    # create tabview
    self.tabviewWf = ctk.CTkTabview(self.tabview.tab("Waveform"), width=100)
    self.tabviewWf.grid(row=0, column=0, padx=(5, 5), pady=(5, 5), sticky="nsew")
    self.tabviewWf.add("DAQ")
    self.tabviewWf.add("Analysis")
    self.tabviewWf.tab("DAQ").grid_columnconfigure(0, weight=0)
    self.tabviewWf.tab("DAQ").grid_columnconfigure(1, weight=3)  
    self.tabviewWf.tab("DAQ").grid_rowconfigure(0, weight=1)  # 100% de altura
    self.tabviewWf.tab("Analysis").grid_columnconfigure(0, weight=0)
    self.tabviewWf.tab("Analysis").grid_columnconfigure(1, weight=3)  
    self.tabviewWf.tab("Analysis").grid_rowconfigure(0, weight=1)  # 100% de altura

    # Waveform tab settings
    # Crear el primer contenedor (izquierda)
    self.optionsWf = ctk.CTkFrame(self.tabviewWf.tab("DAQ"))
    self.optionsWf.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
    self.optionsWf.grid_rowconfigure(4, weight=1)
    self.optionsWf.columnconfigure(0, weight=1)
    self.optionsWf.columnconfigure(1, weight=1)

    self.timeWfLabel = ctk.CTkLabel(self.optionsWf, text="Set time to acquire:", anchor="w")
    self.timeWfLabel.grid(row=0, column=0, padx=10, pady=(20, 0), columnspan=2)
    self.timeWf = ctk.CTkEntry(self.optionsWf, placeholder_text="Default inmediatly")
    self.timeWf.grid(row=1, column=0, padx=10, pady=(0,0), columnspan=2)

    # Variable de control
    self.selected_channelWf = ctk.StringVar(value="1")  # Establecer el valor predeterminado

    self.ch1Wf = ctk.CTkRadioButton(self.optionsWf, text="Ch1", variable=self.selected_channelWf, value="1")
    self.ch1Wf.grid(row=2, column=0, padx=(40,0), pady=(30,5))
    self.ch2Wf = ctk.CTkRadioButton(self.optionsWf, text="Ch2", variable=self.selected_channelWf, value="2")
    self.ch2Wf.grid(row=2, column=1, padx=(0,0), pady=(30,5))
    self.ch3Wf = ctk.CTkRadioButton(self.optionsWf, text="Ch3", variable=self.selected_channelWf, value="3")
    self.ch3Wf.grid(row=3, column=0, padx=(40,0), pady=(5,5))
    self.ch4Wf = ctk.CTkRadioButton(self.optionsWf, text="Ch4", variable=self.selected_channelWf, value="4")
    self.ch4Wf.grid(row=3, column=1, padx=(0,0), pady=(5,5))

    # Crear el botón de start
    self.start_buttonWf = ctk.CTkButton(self.optionsWf, text="Start", command=self.startWf)
    self.start_buttonWf.grid(row=10, column=0, padx=20, pady=(20,50), columnspan=2, sticky="s")

    # Crear el segundo contenedor (derecha)
    self.plotWf = ctk.CTkFrame(self.tabview.tab("Waveform"))
    self.plotWf.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
    self.plotWf.grid_rowconfigure(0, weight=1)
    self.plotWf.grid_columnconfigure(0, weight=1)

    #Spectrum setting analisys
    # Crear el primer contenedor (izquierda)
    self.analysisWf = ctk.CTkFrame(self.tabviewWf.tab("Analysis"))
    self.analysisWf.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
    # Configurar el comportamiento de expansión
    self.analysisWf.grid_columnconfigure(0, weight=1)
    self.analysisWf.grid_columnconfigure(1, weight=1)

    # Crear el botón de start dcr
    self.dcr_button = ctk.CTkButton(self.analysisWf, text="Calculate Dcr", command=lambda: func.startDcr(self, self.dcr_Output), width=120)
    self.dcr_button.grid(row=0, column=0, padx=(10), pady=(20,5), columnspan=2)
    # Crear el widget Text para mostrar la salida
    self.dcr_Output = ctk.CTkTextbox(self.analysisWf, width=90, height=30, activate_scrollbars=False)
    self.dcr_Output.grid(row=1, column=0, padx=(10), pady=(5,10), columnspan=2)

    count=func.count_files(self)

    self.sliderWf = ctk.CTkSlider(self.analysisWf, from_=0, to=count-1, command=lambda value: func.slider_event(self, value))
    self.sliderWf.grid(row=2, column=0, padx=(10), pady=(5,10), columnspan=2)

    self.decrease_button = ctk.CTkButton(self.analysisWf, text="-", width=5, command=lambda: func.decrease_slider_value(self, count))
    self.decrease_button.grid(row=3, column=0, padx=10, pady=10, sticky="nsew")

    self.increase_button = ctk.CTkButton(self.analysisWf, text="+", width=5, command=lambda: func.increase_slider_value(self, count))
    self.increase_button.grid(row=3, column=1, padx=10, pady=10, sticky="nsew")
