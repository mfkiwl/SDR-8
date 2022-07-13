
import uhd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


usrp = uhd.usrp.MultiUSRP()

num_samps = 10000000 # number of samples received
center_freq = 2.44e9# Hz
sample_rate = 56e6 # Hz twice the BW
Fs = 56e6
gain = 40# dB
Threshhold = -60 #dB

usrp.set_rx_rate(sample_rate, 0)
usrp.set_rx_freq(uhd.libpyuhd.types.tune_request(center_freq), 0)
usrp.set_rx_gain(gain, 0)
usrp.set_rx_agc(False, 0)

batch = 1000
# Set up the stream and receive buffer
st_args = uhd.usrp.StreamArgs("fc32", "sc16")
st_args.channels = [0]
metadata = uhd.types.RXMetadata()
streamer = usrp.get_rx_stream(st_args)
recv_buffer = np.zeros((1, batch), dtype=np.complex64)

# Start Stream
stream_cmd = uhd.types.StreamCMD(uhd.types.StreamMode.start_cont)
stream_cmd.stream_now = False
streamer.issue_stream_cmd(stream_cmd)

batch = 1000
# Set up the stream and receive buffer
st_args = uhd.usrp.StreamArgs("fc32", "sc16")
st_args.channels = [0]
metadata = uhd.types.RXMetadata()
streamer = usrp.get_rx_stream(st_args)
recv_buffer = np.zeros((1, batch), dtype=np.complex64)

# t = uhd.types.TimeSpec(.005)

# Start Stream
stream_cmd = uhd.types.StreamCMD(uhd.types.StreamMode.start_cont)
stream_cmd.stream_now = True
# stream_cmd.time_spec = x

streamer.issue_stream_cmd(stream_cmd)

# Receive Samples
import numpy as np

f = open("RawIQ.iq","wb")
# f1 = open("RawIQ1.iq","wb")
# f2 = open("RawIQ2.iq","wb")
samples = np.zeros(batch, dtype=np.complex64)
# samples2 = np.zeros(batch, dtype=np.complex64)
# for i in range(num_samps//batch):
i =0
x=1000
while i <x:
    streamer.recv(recv_buffer, metadata)
    # for i in range(len(recv_buffer)):
    #     if abs(recv_buffer[0][i])< 10**(Threshhold/10):
    #         recv_buffer[0][i] = 0
    samples = recv_buffer[0]

    
    # print(max(abs(samples)))
    if sum(abs(samples))/batch > 0.04:
        # print(max(abs(samples)))
        samples.tofile(f)
        # samples2.tofile(f2)
        i+= 1
        if(i%(x/100) == 0):
            print(i/x)
    else:
        np.zeros(batch, dtype=np.complex64).tofile(f)
    

# Stop Stream
stream_cmd = uhd.types.StreamCMD(uhd.types.StreamMode.stop_cont)
streamer.issue_stream_cmd(stream_cmd)

# we will only take the FFT of the first 1024 samples, see text below


import numpy as np
import matplotlib.pyplot as plt
samples = np.fromfile('RawIQ.iq', np.complex64) # Read in file.  We have to tell it what format it is
print(len(samples))
print(sum(abs(samples))/num_samps)
# plt.figure(figsize=(10, 10), dpi=500)
# Plot constellation to make sure it looks right
plt.plot(np.abs(samples))
# # lt.grid(True)
plt.show()
plt.close()
plt.figure(figsize=(20, 20), dpi=500)
plt.plot(np.real(samples),np.imag(samples),'.')
plt.show()




