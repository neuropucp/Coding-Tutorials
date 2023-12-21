# Cargando datos
import mne
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

datos = mne.io.read_raw_edf(
    r"F:\_1project\project\05_12-FLEX-Complete task2.edf", stim_channel="MarkerType"
)

datos_dataframe = datos.to_data_frame()

datos.info

datos.pick_channels(["Fp1", "Fp2", "AF3", "AF7", "AF8", "AF4"])

# Eventos

events = mne.find_events(datos)

fig = mne.viz.plot_events(
    events, sfreq=datos.info["sfreq"], first_samp=datos.first_samp
)

datos.plot(
    events=events,
    start=5,
    duration=1200,
    color="gray",
    event_color={1: "red"},
    n_channels=1,
)


##Extra
datos.plot(duration=10)

fig = datos.compute_psd(tmax=np.inf, fmax=64).plot(
    average=True, picks="data", exclude="bads"
)

for ax in fig.axes[1:]:
    freqs = ax.lines[-1].get_xdata()
    psds = ax.lines[-1].get_ydata()
    for freq in (60, 120, 180, 240):
        idx = np.searchsorted(freqs, freq)
        ax.arrow(
            x=freqs[idx],
            y=psds[idx] + 18,
            dx=0,
            dy=-12,
            color="red",
            width=0.1,
            head_width=3,
            length_includes_head=True,
        )

# Parte del montaje
easycap_montage = mne.channels.make_standard_montage("easycap-M1")

print(easycap_montage)

datos.set_montage(easycap_montage)
fig = datos.plot_sensors(show_names=True)


spectrum = datos.compute_psd()


spectrum.plot()

spectrum.plot_topomap()


##### Epoch por default

epochs = mne.Epochs(datos, events)
print(epochs)

epochs.plot(n_epochs=5, events=True, n_channels=7, scalings=500e-6)

##IMPORTANTE
datos.plot(
    n_channels=4, duration=800, events=events, scalings=500e-6
)  # Aqui el e-6 significa el tipo de frecuencia/onda (hercios)


# Plotear epochs densidad espectral

epochs.compute_psd().plot(picks="eeg", exclude="bads")


# Plotear epochs combinadas

epochs.plot_image(picks="Fp1", combine="mean")

epochs.plot_image(picks="Fp2", combine="mean")

epochs.plot_image(picks="AF3", combine="mean")

epochs.plot_image(picks="AF7", combine="mean")

epochs.plot_image(picks="AF8", combine="mean")

epochs.plot_image(picks="AF4", combine="mean")

# EVOKED

evoked = epochs.average()

evoked.plot()
