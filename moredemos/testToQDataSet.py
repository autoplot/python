import autoplot as ap
import datetime
import numpy as np

# import matplotlib.pyplot as plt

tt = [datetime.datetime.now()]
tt.append(tt[len(tt) - 1] + datetime.timedelta(seconds=3))
tt.append(tt[len(tt) - 1] + datetime.timedelta(seconds=3))
tt.append(tt[len(tt) - 1] + datetime.timedelta(seconds=3))
tt.append(tt[len(tt) - 1] + datetime.timedelta(seconds=3))

dd = [5.6, 6.3, 6.8, 7.2, 8.1]

ap.start()
ap.plot(tt, dd)
a = input('Press key to continue')

data = np.random.random((1024, 256))
spectrogram = np.log(data ** 2 + 1e-6)
# plt.imshow(spectrogram, cmap="jet")
# plt.colorbar()
# plt.title("Spectrogram")
# plt.xlabel("Time (seconds)")
# plt.ylabel("Frequency (Hz)")
# plt.show()

ap.plot(data)
a = input('Press key to continue')
