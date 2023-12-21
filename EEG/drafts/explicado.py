^# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import mne
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

datos.info

#Se importa el archivo especificando qué channel es el de los eventos con stim_channel (en este caso se ha escogido 'MarkerType'). Se crea una nueva variable para el archivo, en este caso, "datos"


datos = mne.io.read_raw_edf(r"D:\Users\u_psicologia\eventmark_flex128_serial_26.05.20_08.54.33.edf", stim_channel='MarkerType')

#Sólo para saber la estructura de los datos y poder trabajar con el código lo he pasado a dataframe.
datos_dataframe = datos.to_data_frame()

#Se usa el comando "find_events" para encontrar eventos en los datos. Se ha creado una nueva variable llamada "eventos" que va a servir para que los comandos siguientes hagan referencia a estos eventos.
events = mne.find_events(datos) #Nótese que los eventos tienen forma de arrays.


#Adicionalmente se puede crear un diccionario con el nombre de los eventos. Esto no tiene nada que ver con los datos en sí y es un agregado. Sirve para que el código pueda acudir a este diccionario y saber qué evento tiene qué nombre.
event_dict = {
    "auditory/left": 1,
}



#Se pueden hacer gráficos de los eventos. 

fig = mne.viz.plot_events(
    events, sfreq=datos.info["sfreq"], first_samp=0, event_id=event_dict
)


#Con el comando "info" vamos a ver la estructura de los datos que estamos leyendo. Aquí se puede ver que el emotiv no da tanta especificación de los tipos de canales como otros aparatos, pues casi todos los datos por default los considera como canales EEG, así que hay que arreglar ese inconveniente.

datos.info

#Para empezar a hacer gráficos que utilizen los eventos y los EEG, primero se puede especificar qué canales son de EEG. Para eso utilizamos "set_channel_types"

datos.set_channel_types({'T7':'eeg','T8':'eeg'})

#De momento se usará el comando "pick_channels" porque no sirve catalogar cuales son EEG si todos son EEG según el emotive

datos.pick_channels(['T7','T8'])

#Luego podemos hacer gráficos de los eventos con los datos
datos.plot(
    events=events,
    start=5,
    duration=10,
    color="gray",
    event_color={1: "r"},
)




#Load montage
easycap_montage = mne.channels.make_standard_montage("easycap-M1")

print(easycap_montage)


x.plot(start=5, duration=5)




# Use the preloaded montage
datos.set_montage(easycap_montage)
fig = datos.plot_sensors(show_names=True)




spectrum = datos.compute_psd()


spectrum.plot_topomap()



datos.describe()

datos.load_data()

#avance artifacts EOG. Crear epoch de artifacts

eog_epochs = mne.preprocessing.create_eog_epochs(datos, ch_name=['T7','T8'], baseline=(-0.5, -0.2), reject_by_annotation=True)
eog_epochs.plot_image(combine="mean")
eog_epochs.average().plot_joint()



epoch_eog=eog_epochs.to_data_frame()

#crear eventos por eog y anotarlos
eog_events = mne.preprocessing.find_eog_events(datos, ch_name=['T7','T8'])  #identificar eventos de eog
n_blinks = len(eog_events)  
onset = eog_events[:, 0] / datos.info['sfreq'] -0.25 #QUE SIGNIFICA ESTA OPERACION????
duration = np.repeat(0.5, n_blinks)  
description = ['bad blink'] * n_blinks  
annotations = mne.Annotations(onset, duration, description, orig_time=datos.info['meas_date'])  
datos.set_annotations(annotations)  


#reject by annotation

nuevos_eventos=mne.preprocessing.find_eog_events(datos, ch_name=['T7','T8'], reject_by_annotation=True)

#crear diccionario de eventos del 0 al 100

my_list = list(range(0,101))
string_list = [str(element) for element in my_list]
delimiter = ", "
result_string = delimiter.join(string_list)
print(result_string)

string_list


dictionary = {
  **dict.fromkeys(my_list, 'bad_datos'),
  }

eog_epochs = mne.preprocessing.create_eog_epochs(datos, ch_name=['T7','T8'], baseline=(-0.5, -0.2), reject_by_annotation=True)


datos.annotations
