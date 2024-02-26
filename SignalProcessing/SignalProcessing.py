import numpy as np
import scipy.signal
import matplotlib.pyplot as plt
from scipy import signal, fft

Fs = 1000
F_max = 29
F_filter = 36
n = 500
a = 0
b = 10


random = np.random.normal(a, b, n)
x = np.arange(n)/Fs
w = F_max/(Fs/2)
parameters_filter = scipy.signal.butter(3, w, 'low', output='sos')

y = scipy.signal.sosfiltfilt(parameters_filter, random)

# title = f"Сигнал з максимальною частотою F_max = {F_max} Гц"
# fig, ax = plt.subplots(figsize=(21, 14))
# ax.plot(x, y, linewidth=1)
# ax.set_xlabel("Час (секунди)", fontsize=14)
# ax.set_ylabel("Амплітуда сигналу", fontsize=14)
# plt.title(title, fontsize=14)
# plt.show()
# fig.savefig("./figures/" + title + ".png", dpi=600)

spectr = scipy.fft.fft(y)
spectr = np.abs(scipy.fft.fftshift(spectr))
length_signal = n
frq = scipy.fft.fftfreq(length_signal, 1/length_signal)
frq2 = scipy.fft.fftshift(frq)

def pict(text, x, y, xLabel, yLabel):
    title = text
    fig, ax = plt.subplots(figsize=(21, 14))
    ax.plot(x, y, linewidth=1)
    ax.set_xlabel(xLabel, fontsize=14)
    ax.set_ylabel(yLabel, fontsize=14)
    plt.title(title, fontsize=14)
    plt.show()
    fig.savefig("./figures/" + title + ".png", dpi=600)

# pict(f"Спектр сигналу з максимальною частотою F_max = {F_max} Гц",
#      frq2, spectr, "Частота (Гц)", "Амплітуда спектру" )


discrete_signals = []
discrete_signals_spectrums = []
discrete_signals_FH4 = []
discrete_signals_disp = []
discrete_signals_noise = []
for Dt in [2, 4, 8, 16]:
    discrete_signal = np.zeros(n)
    for i in range(0, round(n/Dt)):
        discrete_signal[i * Dt] = y[i * Dt]
    discrete_signals += [list(discrete_signal)]
    discrete_signal_spectrum = scipy.fft.fft(discrete_signal)
    discrete_signal_spectrum = np.abs(scipy.fft.fftshift(discrete_signal_spectrum))
    discrete_signals_spectrums += [list(discrete_signal_spectrum)]
    w = F_filter/(Fs/2)
    parameters_filter = scipy.signal.butter(3, w, 'low', output='sos')
    y_discrete = scipy.signal.sosfiltfilt(parameters_filter, discrete_signal)
    discrete_signals_FH4 += [list(y_discrete)]
    El = y_discrete - y
    D = np.var(El)
    discrete_signals_disp += [D]
    snr = np.var(y)/D
    discrete_signals_noise += [snr]


def pict2(text, x, y):
    title = text
    fig, ax = plt.subplots(2, 2, figsize=(16/2.54, 14/2.54))
    s = 0
    for i in range(0, 2):
        for j in range(0, 2):
            ax[i][j].plot(x, y[s], linewidth=1)
            s += 1
    fig.supxlabel("Час (секунди)", fontsize=14)
    fig.supylabel("Амплітуда сигналу", fontsize=14)
    fig.suptitle(title, fontsize=14)
    fig.savefig("./figures/" + title + ".png", dpi=600)
    plt.show()

pict2("Сигнал з кроком дискретизації Dt = (2, 4, 8, 16)", x, discrete_signals)

pict2("Спектр сигналу з кроком дискретизації Dt = (2, 4, 8, 16)", frq2, discrete_signals_spectrums)

pict2("Відновлені аналогові сигнали з кроком дискретизації Dt = (2, 4, 8, 16)", x, discrete_signals_FH4)

pict("Залежність дисперсії від кроку дискретизації",
     [2,4,8,16], discrete_signals_disp, "крок дискретизації", "Дисперсія")

pict("Залежність співвідношення сигнал-шум від кроку дискретизації",
     [2,4,8,16], discrete_signals_noise, "крок дискретизації", "ССШ")
