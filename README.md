# gr_Morse_Receiver
This is a basic Morse receiver for GNURadio, containing:
1. signal demodulation and detection of Morse signals with an SDR using GNURadio (and Python modules)
2. a simple live decoder of received symbols provided by the GNURadio Morse receiver

### Overview
The __flowgraph__ is provided in the `examples` folder:
+ `Morse_receiver.grc`
    + for SDR reception

A supplementary tool is provided in the `python` folder:
+ `DecodeMorse.py`decodes the received symbols from a specified ZMQ server upon receiving them. It shows the decoded ASCII symbols.

### Requirements
The Morse receiver was tested with:
+ gnuradio & GNURadio Companion 3.10.1.1 (Linux)
+ Python 3.10.6
    + PyQt5 5.15.7
    + pyzmq 22.2.1
    + gnuradio-osmosdr 0.2.0
+ An SDR receiver capable of receiving in the range of at least 1 kHz - 1 MHz, e.g. an _Airspy Discovery HF+_ is configured and used for this project.
+ An antenna that provides sufficiently clear Morse signals, e.g. a simple _YouLoop_ loop antenna was used for this project. Indoor reception should probably be possible. You should mount the antenna close to a window or outside.
+ The user might also need some antenna cables and adapters to connect the SDR with the antenna.
+ This project has been successfully tested in:
    + Ubuntu 22.04.2 LTS

### Instructions/Setup

#### Signal Reception with SDR
+ Set up your SDR with your computer.
+ Ensure that the raw Morse signal reception is good enough, e.g. using gqrx or another signal analysis tool. It should reach at least at approximately -95dB or better.
+ To start the Morse receiver, open the flowchart in `/examples/Morse_receiver.grc` with GNURadio Companion
    + Press `run` button.
    + Set the frequency slider values so that stronger signals in the waterfall chart get close to 0.00 (so that it begins either slightly left or right of it). Use the Mouse for the rough frequency adjustment.
        + You can further adjust and fine-tune the signal with the mouse wheel.
        + You can also zoom into the waterfall plot.
    + Adjust the Gain slider values to boost the signal (and noise) strength.
    + Adjust the low_thres and high_thres slider values, if needed.
    + Adjust the loudness, especially if the audio tone is clipped.
    + After picking a good signal, the GNURadio Companion debug console should show debug messages each for each received symbol.

+ Next, open a terminal.
    + Change to your cloned repository.
    + Run DecodeMorse with ```python3 ./python/DecodeMorse.py```.
    + The terminal should show the decoded ASCII symbols.
    + NOTE: Morse messages are is often short and technical. The messages "TEST", or "CQ", in the decoder output are a good indicator that decoding worked well.
    + NOTE: sometimes a symbol can not be decoded correctly, e.g. due to bad reception. Then the decoder will produce
    + NOTE: Some Morse signals tend to fade in and out, so that some symbols might get lost sometimes.
    + NOTE: Interfering Morse signals might disturb the decoder.
    + NOTE: The transmission speed of Morse symbols (and pauses) varies among the senders. Feel free to optimize the Morse decoder and other reception parameters according to your needs.

### REMARKS
+ This project has __not__ been tested with other SDR receivers.
+ This project has __not__ been tested with a receiver setup using a sound card.
+ This project has __not__ been tested with other antennas
+ A Low Noise Amplifier (LNA) is not needed.
+ Additional resilience of the Decoder has __not__ been implemented yet.
+ This project might also run fine under Windows, but it was not tested yet.
+ The maintainer is only a hobbyist, __not__ a Morse professional ;-).
