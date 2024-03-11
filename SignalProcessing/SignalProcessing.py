import numpy as np
import scipy.signal
import matplotlib.pyplot as plt
from scipy import signal, fft


def pict(text, x, y, xLabel, yLabel):
    title = text
    fig, ax = plt.subplots(figsize=(21, 14))
    ax.plot(x, y, linewidth=1)
    ax.set_xlabel(xLabel, fontsize=14)
    ax.set_ylabel(yLabel, fontsize=14)
    plt.title(title, fontsize=14)
    plt.show()
    fig.savefig("./figures/" + title + ".png", dpi=600)


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

#
# pict2("Сигнал з кроком дискретизації Dt = (2, 4, 8, 16)", x, discrete_signals)
#
# pict2("Спектр сигналу з кроком дискретизації Dt = (2, 4, 8, 16)", frq2, discrete_signals_spectrums)
#
# pict2("Відновлені аналогові сигнали з кроком дискретизації Dt = (2, 4, 8, 16)", x, discrete_signals_FH4)
#
# pict("Залежність дисперсії від кроку дискретизації",
#      [2,4,8,16], discrete_signals_disp, "крок дискретизації", "Дисперсія")
#
# pict("Залежність співвідношення сигнал-шум від кроку дискретизації",
#      [2,4,8,16], discrete_signals_noise, "крок дискретизації", "ССШ")


quantum_signals = []
quantum_signals_disp = []
quantum_signals_noise = []
for M in [4,16,64,256]:
    bits = []
    delta = (np.max(y) - np.min(y)) / (M - 1)
    quantize_signal = delta * np.round(y / delta)
    quantum_signals += [list(quantize_signal)]
    quantize_levels = np.arange(np.min(quantize_signal), np.max(quantize_signal)+1, delta)
    quantize_bit = np.arange(0, M)
    quantize_bit = [format(bits, '0' + str(int(np.log(M) / np.log(2))) + 'b') for bits in quantize_bit]
    quantize_table = np.c_[quantize_levels[:M], quantize_bit[:M]]

    fig, ax = plt.subplots(figsize=(14 / 2.54, M / 2.54))
    table = ax.table(cellText=quantize_table, colLabels=['Значення сигналу', 'Кодова послідовність'], loc='center')
    table.set_fontsize(14)
    table.scale(1, 2)
    ax.axis('off')
    title = f"Таблиця квантування для {M} рівнів"
    fig.savefig("./figures/" + title + ".png", dpi=600)
    plt.show()

    for signal_value in quantize_signal:
        for index, value in enumerate(quantize_levels[:M]):
            if np.round(np.abs(signal_value - value), 0) == 0:
                bits.append(quantize_bit[index])
                break

    bits = [int(item) for item in list(''.join(bits))]

    fig, ax = plt.subplots(figsize=(21 / 2.54, 14 / 2.54))
    x_bits = np.arange(0, len(bits))
    y_bits = bits
    ax.step(x_bits, y_bits, linewidth=0.1)

    title = f"Кодова послідовність сигналу при кількості рівнів квантування {M}"
    fig.supxlabel("Біти", fontsize=14)
    fig.supylabel("Амплітуда сигналу", fontsize=14)
    fig.suptitle(title, fontsize=14)
    fig.savefig("./figures/" + title + ".png", dpi=600)
    plt.show()

    El = quantize_signal - y
    D = np.var(El)
    quantum_signals_disp += [D]
    snr = np.var(y) / D
    quantum_signals_noise += [snr]

# pict2("Цифрові сигнали за рівнями квантування (4, 16, 64, 256)", x, quantum_signals)
#
# pict("Залежність дисперсії від кількості рівнів квантування",
#      [4, 16, 64, 256], quantum_signals_disp, "Кількість рівнів квантування", "Дисперсія")
#
# pict("Залежність співвідношення сигнал-шум від кількості рівнів квантування",
#      [4, 16, 64, 256], quantum_signals_noise, "Кількість рівнів квантування", "ССШ")


