
import numpy as np
from gnuradio import gr


"""
Embedded Python Blocks:

Each time this file is saved, GRC will instantiate the first class it finds
to get ports and parameters of your block. The arguments to __init__  will
be the parameters. All of them are required to have default values!
"""


class blk(gr.sync_block):

    def __init__(self, threshold=0.0, mode=0, coeff=0.15):
        gr.sync_block.__init__(
            self,
            name='Envelope Detector',
            in_sig=[np.float32],
            out_sig=[np.float32]
        )
        self.ry = 0
        self.threshold = threshold
        self.mode = mode
        self.coeff = coeff

    def work(self, input_items, output_items):
        output_items[0][:] = input_items[0]

        buf = [0] * len(input_items[0])
        a0 = self.coeff
        b1 = 1 - a0

        for i in range(0, len(input_items[0])):
            if self.mode == 1:
                buf[i] = abs(input_items[0][i])
            else:
                if input_items[0][i] > self.threshold:
                    buf[i] = input_items[0][i]
                else:
                    buf[i] = 0

        for i in range(0, len(input_items[0])):
            if i == 0:
                output_items[0][i] = a0*buf[i] + b1*self.ry
            else:   # i >= 1
                output_items[0][i] = a0*buf[i] + b1*output_items[0][i-1]

        i = len(output_items[0]) - 1
        self.ry = output_items[0][i]

        return len(output_items[0])
