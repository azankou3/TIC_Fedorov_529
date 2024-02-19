import numpy as np
import scipy.signal
import matplotlib.pyplot as plt
from scipy import signal, fft

Fs = 1000
F_max = 29
n = 500
a = 0
b = 10


random = np.random.normal(a, b, n)
x = np.arange(n)/Fs
w = F_max/(Fs/2)
parameters_filter = scipy.signal.butter(3, w, 'low', output='sos')

y = scipy.signal.sosfiltfilt(parameters_filter, random)

title = f"Сигнал з максимальною частотою F_max = {F_max} Гц"
fig, ax = plt.subplots(figsize=(21, 14))
ax.plot(x, y, linewidth=1)
ax.set_xlabel("Час (секунди)", fontsize=14)
ax.set_ylabel("Амплітуда сигналу", fontsize=14)
plt.title(title, fontsize=14)
plt.show()
fig.savefig("./figures/" + title + ".png", dpi=600)

spectr = scipy.fft.fft(y)
spectr = np.abs(scipy.fft.fftshift(spectr))
length_signal = n
frq = scipy.fft.fftfreq(length_signal, 1/length_signal)
frq2 = scipy.fft.fftshift(frq)

title = f"Спектр сигналу з максимальною частотою F_max = {F_max} Гц"
fig, ax = plt.subplots(figsize=(21, 14))
ax.plot(frq2, spectr, linewidth=1)
ax.set_xlabel("Частота (Гц)", fontsize=14)
ax.set_ylabel("Амплітуда Спектру", fontsize=14)
plt.title(title, fontsize=14)
plt.show()
fig.savefig("./figures/" + title + ".png", dpi=600)


