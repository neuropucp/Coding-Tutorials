# -*- coding: utf-8 -*-
"""
Created on Thu Nov  9 13:27:42 2023

@author: u_psicologia
"""
# Se importa el módulo para el PCA
from sklearn.decomposition import PCA, FastICA
from mne.preprocessing import ICA

# Se extrae la data ya filtrada de los sensores
x = (
    datos.get_data()
)  # Se supone que este comando convierte la data de "datos" en un array. El resultado ya no es un raw porque el raw no puede leerlo el scikit.


# Se define el tipo del PCA. En este caso dejamos todos los valores en none (por default) así que sólo colocamos que se llame al paquete PCA (en caps) como tal.
pca = PCA(n_components=None)


# Creamos una variable del PCA ya aplicado a los datos
PCAX = pca.fit(x)

# Se supone que después de esto ya tenemos nuestro PCA y podemos pedirles todos los datos vistos en la documentación https://scikit-learn.org/stable/modules/generated/sklearn.decomposition.PCA.html
# En este caso utilizaremos el comando para ver los componentes
print(PCAX.n_components_)  # Hay 2 componentes

matrix = PCAX.components_
#######ICA#######

# Antes de aplicar ICA recomiendan ya hacer un filtrado de los slow drift

datos.load_data()

filt_datos = datos.copy().filter(l_freq=1.0, h_freq=None)


# Setupear cómo será el ICA. Un poco parecido a setupear como es el PCA.
ica = ICA(
    n_components=2, max_iter="auto", random_state=97
)  # El random state es el SEED.

# Aplicar el ICA

ica.fit(filt_datos)
ica

# Varianza explicada
explained_var_ratio = ica.get_explained_variance_ratio(
    filt_datos
)  # se puede seleccionar ver la varianza del componente con components=[0,1,2] donde el primer componente siempre es 0
explained_var_ratio
# Varianza explicada pero con un output más leíble
explained_var_ratio = ica.get_explained_variance_ratio(filt_datos)
for channel_type, ratio in explained_var_ratio.items():
    print(
        f"Fraction of {channel_type} variance explained by all components: " f"{ratio}"
    )


# Varianza explicada por componentes. Se empieza en el componente 0, 1, etc.
explained_var_ratio = ica.get_explained_variance_ratio(filt_datos, components=[0])
# Imprimir en porcentaje la varianza
ratio_percent = round(100 * explained_var_ratio["eeg"])
print(
    f"Fraction of variance in EEG signal explained by first component: "
    f"{ratio_percent}%"
)


datos.load_data()
ica.plot_sources(datos, show_scrollbars=False)  # Plotear los componentes del ICA.

ica.plot_components()  # Gráfico. Pero no sale


# Corregido
ica.plot_overlay(datos, exclude=[0], picks="eeg")


# En teoría, podemos escoger qué componentes del ICA están siendo excluidos con ICA.EXCLUDE

ica.exclude = [0]

# Luego de esto, en teoría, podemos usar ICA.APPLY
reconst_datos = filt_datos

ica.apply(reconst_datos)

filt_datos.plot()

# https://mne.tools/dev/auto_tutorials/preprocessing/40_artifact_correction_ica.html#sphx-glr-auto-tutorials-preprocessing-40-artifact-correction-ica-py
