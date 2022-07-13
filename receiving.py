
import uhd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


usrp = uhd.usrp.MultiUSRP()

num_samps = 10000000 # number of samples received
center_freq = 2.44e9# Hz
sample_rate = 56e6 # Hz twice the BW
# gain = 40# dB
Threshhold = 0.04

usrp.set_rx_rate(sample_rate, 0)
usrp.set_rx_freq(uhd.libpyuhd.types.tune_request(center_freq), 0)
# usrp.set_rx_gain(gain, 0)
usrp.set_rx_agc(True, 0)

batch = 1000
# Set up the stream and receive buffer
st_args = uhd.usrp.StreamArgs("fc32", "sc16")
st_args.channels = [0]
metadata = uhd.types.RXMetadata()
streamer = usrp.get_rx_stream(st_args)
recv_buffer = np.zeros((1, batch), dtype=np.complex64)

# Start Stream
stream_cmd = uhd.types.StreamCMD(uhd.types.StreamMode.start_cont)
stream_cmd.stream_now = True
streamer.issue_stream_cmd(stream_cmd)


# Receive Samples
import numpy as np
Threshhold
def thresh(x):
    if abs(x) < Threshhold:
        return 0
    else:
        return x

f = open("RawIQ.iq","wb")
samples = np.zeros(batch, dtype=np.complex64)



i =0
x=1000
while i <x:
    streamer.recv(recv_buffer, metadata)
    samples = recv_buffer[0]
    if sum(abs(samples))/batch > 0.04:
        samples = np.array([thresh(x) for x in samples])
        samples.tofile(f)
        i+= 1
    else:
        np.zeros(batch, dtype=np.complex64).tofile(f)
    

# Stop Stream
stream_cmd = uhd.types.StreamCMD(uhd.types.StreamMode.stop_cont)
streamer.issue_stream_cmd(stream_cmd)






