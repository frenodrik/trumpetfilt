from scipy import signal
import numpy as np
import matplotlib.pyplot as plt
import soundfile as sf

# filter för en given knappkombination
overtones = [3/4, 1, 3/2] + list(range(2, 9))

# insignal
x, fs = sf.read(r'Z:\Användarmappar\Fredrik\brussvep.wav')
f0 = 233.082  # Frequency to be retained (Hz) (Bb3)
Q = 200.0  # Quality factor
w0 = f0/(fs/2)  # Normalized Frequency
print('sample rate: {}'.format(fs))

fig, ax = plt.subplots(2, 1, figsize=(8, 6))
# Design peak filters
for ii, factor in enumerate(overtones):
    b, a = signal.iirpeak(w0 * factor, Q)
    if ii == 0:
        y = signal.lfilter(b, a, x)
    else:
        y = signal.lfilter(b, a, y)
    # normalisera (nivån sjunker lite för varje filtrering)
    y = .997 * y / np.linalg.norm(y)

    # Frequency response
    w, h = signal.freqz(b, a)
    # Generate frequency axis
    freq = w*fs/(2*np.pi)
    # Plot
    ax[0].semilogx(freq, 20*np.log10(abs(h)), color='blue')
    ax[1].semilogx(freq, np.unwrap(np.angle(h)) * 180 / np.pi, color='green')

# normalisera igen
y = .997 * y / np.linalg.norm(y)

print([20 * np.log10(y_) for y_ in y])
sf.write(r'Z:\Användarmappar\Fredrik\brussvep_filtered.wav', y, fs)

ax[0].set_title("Frequency Response")
ax[0].set_ylabel("Amplitude (dB)", color='blue')
ax[0].set_xlim([20, fs / 2])
ax[0].set_ylim([-50, 10])
ax[0].grid()
ax[1].set_ylabel("Angle (degrees)", color='green')
ax[1].set_xlabel("Frequency (Hz)")
ax[1].set_xlim([20, fs / 2])
ax[1].set_yticks([-90, -60, -30, 0, 30, 60, 90])
ax[1].set_ylim([-90, 90])
ax[1].grid()
plt.show()
