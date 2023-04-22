# gr_Morse_Receiver
This is a basic Morse receiver for GNURadio, containing:
1. signal demodulation and detection of Morse signals with an SDR using GNURadio (and Python modules)
2. a simple live decoder of received symbols provided by the GNURadio Morse receiver

### Overview
The __flowgraph__ is provided in the `examples` folder:
+ `Morse_receiver.grc`
    + for SDR reception

A supplementary tool is provided in the `python` folder:
+ `DecodeMorse.py` decodes the received symbols from a specified ZMQ server upon receiving them. It shows the decoded ASCII symbols.

### Requirements
The Morse receiver was tested with:
+ gnuradio & GNURadio Companion 3.10.1.1 (Linux)
+ Radioconda 2023.02.24 & gnuradio & GNURadio Companion 3.10.5.1 (Windows)
+ Python 3.10.6
    + PyQt5 5.15.7
    + pyzmq 23.1.0
    + gnuradio-osmosdr 0.2.0
+ An SDR receiver capable of receiving in the range of at least 1 kHz - 1 MHz, e.g. an _Airspy Discovery HF+_ is configured and used for this project.
+ An antenna that provides sufficiently clear Morse signals, e.g. a simple _YouLoop_ loop antenna was used for this project. Indoor reception should probably be possible. You should mount the antenna close to a window or outside.
+ The user might also need some antenna cables and adapters to connect the SDR with the antenna.
+ This project has been successfully tested in:
    + Ubuntu 22.04.2 LTS
    + MS Windows 11

### Instructions/Setup
#### Signal Reception with SDR
+ Set up your SDR with your computer.
+ Ensure that the raw Morse signal reception is good enough, e.g. using gqrx or another signal analysis tool. It should reach at least at approximately -95dB or better.
+ To start the Morse receiver, open the flowchart in `/examples/Morse_receiver.grc` with GNURadio Companion
    + Press `run` button.
    + Set the CW band entry frequency if needed in the edit box entitled _CW band entry frequency_.
    + Set the _frequency_ slider values so that stronger signals in the waterfall chart get close to 0.00 (so that it begins either slightly left or right of it). Use the mouse to drag the slider for the rough frequency adjustment.
        + You can further adjust and fine-tune the frequency with the mouse wheel, to improve signal reception.
        + You can also zoom into the waterfall plot.
    + Adjust the _gain_ slider values to boost or dampen the signal (and noise) strength.
    + Adjust the _low_thres_ and _high_thres_ slider values, if needed.
    + The theshold limits will be shown in the time signal plot.
    + Adjust the _loudness_, especially if the audio tone is clipped.
    + Activate checkbox _print durations of ON_ to view the signal durations during OFF.
    + Set the _short mark_ slider, _long mark_ slider and _tolerance_ sliders, accordingly.
    + Deactivate checkbox _print durations of ON_.
    + Activate checkbox _print durations of OFF_ to view the signal durations during OFF.
    + Set the _element space_ slider, _letter space_ slider and _word space_ slider accordingly.
    + Deactivate checkbox _print durations of OFF_.
    + Activate checkbox _print symbols_ to show the detected Morse symbols. After picking a good signal, the GNURadio Companion debug console should show debug messages each for each received symbol (streams of . and _).

+ Next, open a terminal.
    + Change to your cloned repository.
    + Run DecodeMorse with ```python3 ./python/DecodeMorse.py```.
    + The terminal should show the decoded ASCII symbols.
    + NOTE: Morse messages are often shortened and technical. The messages "TEST", or "CQ", in the decoder output are a good indicator that decoding worked sufficiently well.
    + NOTE: Sometimes a symbol can not be decoded correctly, e.g. due to bad reception. Then the decoder will produce decoding errors.
    + NOTE: Some Morse signals tend to fade in and out, so that some symbols might get lost sometimes.
    + NOTE: Interfering Morse signals might disturb the decoder.
    + NOTE: The transmission speed of Morse symbols (and pauses) varies among different senders. Feel free to optimize the Morse decoder timing and other reception parameters according to your needs.

### REMARKS
+ This project has __not__ been tested with other SDR receivers.
+ This project has __not__ been tested with a receiver setup using a sound card.
+ This project has __not__ been tested with other antennas.
+ A Low Noise Amplifier (LNA) is not needed.
+ Additional resilience of the Decoder has __not__ been implemented yet.
+ The maintainer is only a hobbyist, __not__ a Morse professional ;-).
