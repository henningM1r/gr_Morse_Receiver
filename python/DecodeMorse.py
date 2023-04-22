# -*- coding: iso-8859-1 -*-

import zmq



morse_dict = {
    "A": "._",
    "B": "_...",
    "C": "_._.",
    "D": "_..",
    "E": ".",
    "F": ".._.",
    "G": "__.",
    "H": "....",
    "I": "..",
    "J": ".__",
    "K": "_._",
    "L": "._..",
    "M": "__",
    "N": "_.",
    "O": "___",
    "P": ".__.",
    "Q": "__._",
    "R": "._.",
    "S": "...",
    "T": "_",
    "U": ".._",
    "V": "..._",
    "W": ".__",
    "X": "_.._",
    "Y": "_.__",
    "Z": "__..",
    "1": ".____",
    "2": "..___",
    "3": "...__",
    "4": "...._",
    "5": ".....",
    "6": "_....",
    "7": "__...",
    "8": "___..",
    "9": "____.",
    "0": "_____",
    ".": "._._._",
    ",": "__..__",
    ":": "___...",
    ";": "_._._.",
    "?": "..__..",
    "!": "__..__",
    "+": "._._.",
    "-": "_...._",
    "=": "_..._",
    "@": ".__._.",
    "/": "______",
    "(": "_.__.",
    ")": "_.__._",
    "_": "..__._",
    "&": "._...",
    "CH": "____",
    "KA": "_._._",   # Spruchanfang
    "BT": "_..._",   # Pause/Trennung
    "AR": "._._.",   # Spruchende
    "VE": "..._.",   # verstanden
    "SK": "..._._.", # Verkehrsende
    "AS": "._...",   # warten
    "KN": "_.__.",   # senden für bestimmte Station
}

morse_swap_dict = {v: k for k, v in morse_dict.items()}


def decode_morse_stream(morse_stream):
    symbol = ''.join(morse_stream)

    if symbol in morse_swap_dict:
        print(morse_swap_dict[symbol], end="")

    else:
        print("symbol not recognized")


def consumer():
    context = zmq.Context()
    
    consumer_receiver = context.socket(zmq.PULL)
    consumer_receiver.connect("tcp://127.0.0.1:55555")
    
    morse_stream = []
    count = 0
    while True:
        data = consumer_receiver.recv()
        received_msg = data.decode('ascii')[3:]
        
        #print(f"{received_msg}")
        
        if received_msg == ".":
            morse_stream.append(".")
        
        elif received_msg == "_":
            morse_stream.append("_")

        elif received_msg == " ":
            decode_morse_stream(morse_stream)
            morse_stream = []
            count += 1

        elif received_msg == ";":
            decode_morse_stream(morse_stream)
            morse_stream = []
            count = 0
            print("")

        if count == 20:
            print("")
            count = 0


consumer()
