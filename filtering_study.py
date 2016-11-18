import numpy as np
import matplotlib.pyplot as plt



npts = 1024

end = 8
f_samp = end/float(npts)


f_ny = 0.5/f_samp
sigma = 0.5


# integer is seconds
fa = 1    / float(npts)
fb = 15   / float(npts)
fc = 50   / float(npts)




x = np.linspace(0,end,npts)

n = np.random.normal(scale = sigma, size=(npts))

s = np.sin(2*np.pi*fa/f_samp*x) + np.sin( 2*np.pi*fb/f_samp*x) + np.sin(2*np.pi*fc/f_samp*x)

y = s+ n






#filter
f_low = 5 / float(npts)
f_high = 25 / float(npts)
b = 5 / float(npts)

N = int(np.ceil(4/b))
if not N % 2: N+=1 #make N odd
n = np.arange(N)

 # Compute a low-pass filter with cutoff frequency fL.
hlpf = np.sinc(2 * f_low * (n - (N - 1) / 2.))
hlpf *= np.blackman(N)
hlpf /= np.sum(hlpf)

# Compute a high-pass filter with cutoff frequency fH.
hhpf = np.sinc(2 * f_high * (n - (N - 1) / 2.))
hhpf *= np.blackman(N)
hhpf /= np.sum(hhpf)
hhpf = -hhpf
hhpf[(N - 1) / 2] += 1

# Add both filters.
h = hlpf + hhpf


s_f = np.convolve(s,h, mode="same")

plt.plot(x,s)
plt.plot(x,s_f)
plt.show(block=True)
