"""
Embedded Python Blocks:

Each time this file is saved, GRC will instantiate the first class it finds
to get ports and parameters of your block. The arguments to __init__  will
be the parameters. All of them are required to have default values!
"""

import numpy as np
from gnuradio import gr
import pmt



# counts number of ones of current status
_num_ones  = 0

# counts number of zeros of current status
_num_zeros = 0

# stores current on/off status
_sync = -1


class blk(gr.sync_block):

    def __init__(self, OOK_pause=270, ASCII_pause=825, short_sym=280, long_sym=870, break_pause=1200, tolerance=40, print_symbols=True, print_1duration=False, print_0duration=False):

        gr.sync_block.__init__(
            self,
            name='Morse Decoder',
            in_sig=[np.float32],
            out_sig=[np.float32]
        )
        
        # durations of the symbols and pauses
        self.tolerance   = tolerance
        self.OOK_pause   = OOK_pause
        self.ASCII_pause = ASCII_pause
        self.short_sym   = short_sym
        self.long_sym    = long_sym
        self.break_pause = break_pause

        # verbose output
        self.print_symbols   = print_symbols
        self.print_1duration = print_1duration
        self.print_0duration = print_0duration

        if self.print_symbols == True:
            print("short mark (.): ", self.short_sym)
            print("long mark (_): ", self.long_sym)
            print("element-space (^)", self.OOK_pause)
            print("letter-space (~): ", self.ASCII_pause)
            print("word-space (;): ", self.break_pause)
            print("tolerance: ", self.tolerance)
            

        # output message
        self.message_port_register_out(pmt.intern('msg_out'))
        

    def work(self, input_items, output_items):
        global _num_zeros
        global _num_ones
        global _sync

        inp = input_items[0]

        for idx in range(len(inp)):
            ch = inp[idx]

            if ch == 1:
                _num_ones += 1

            else: # ch == 0
                _num_zeros += 1

            # out of sync status
            if _sync == -1:
                _num_zeros = 0
                _num_ones = 0

                if ch == 0:
                    _sync = 0
                
                elif ch == 1:
                    _sync = 1
            
            # status: currently off
            elif _sync == 0:
                # status remains identical
                if ch == 0:
                    pass
                
                elif ch == 1:
                    _sync = 1
                    # WARN: this print is very slow, and may cause GNURadio to crash
                    if self.print_0duration:
                        print(f"#zeros: {_num_zeros}")

                    # detect OOK pause
                    if (_num_zeros >= self.OOK_pause - self.tolerance and
                        _num_zeros <= self.OOK_pause + self.tolerance):
                        
                        if self.print_symbols:
                            #print(f"^")
                            pass

                        # marking detected OOK_pause
                        key = pmt.intern(" ")
                        value = pmt.intern("^")
                        self.add_item_tag(0,
                            self.nitems_written(0) + idx,
                            key,
                            value
                        )

                    # detect ASCII pause
                    elif (_num_zeros >= self.ASCII_pause - self.tolerance and
                          _num_zeros <= self.ASCII_pause + self.tolerance):
                        
                        if self.print_symbols:
                            print("~")

                        # for further processing outside this block
                        self.message_port_pub(pmt.intern("msg_out"), pmt.intern(" "))

                        # marking detected ASCII pause
                        key = pmt.intern(" ")
                        value = pmt.intern("~")
                        self.add_item_tag(0,
                            self.nitems_written(0) + idx,
                            key,
                            value
                        )

                    # detect break pause
                    elif (_num_zeros >= self.break_pause - self.tolerance):
                        
                        if self.print_symbols:
                            print(";")
                            #print(f"symbol end, break")
                        
                        # for further processing outside this block 
                        self.message_port_pub(pmt.intern("msg_out"), pmt.intern(";"))
                        
                        # marking detected break pause
                        key = pmt.intern(" ")
                        value = pmt.intern("°")
                        self.add_item_tag(0,
                            self.nitems_written(0) + idx,
                            key,
                            value
                        )

                    _num_zeros = 0
            
            # status: currently on
            elif _sync == 1:
                # status changes
                if ch == 0:
                    _sync = 0
                    # WARN: this print is very slow, and may cause GNURadio to crash
                    if self.print_1duration:
                        print(f"#ones: {_num_ones}")
                    
                    # detect short symbol
                    if (_num_ones >= self.short_sym - self.tolerance and
                        _num_ones <= self.short_sym + self.tolerance):
                        
                        if self.print_symbols:
                            print(f".", end="")
                        
                        # for further processing outside this block
                        self.message_port_pub(pmt.intern("msg_out"), pmt.intern("."))

                        # marking detected short symbol
                        key = pmt.intern(".")
                        value = pmt.intern(".")
                        self.add_item_tag(0,
                            self.nitems_written(0) + idx,
                            key,
                            value
                        )

                    # detect long symbol
                    elif (_num_ones >= self.long_sym - self.tolerance and
                          _num_ones <= self.long_sym + self.tolerance):
                        
                        if self.print_symbols:
                            print(f"_", end="")

                        # for further processing outside this block
                        self.message_port_pub(pmt.intern("msg_out"), pmt.intern("_"))

                        # marking detected long symbol
                        key = pmt.intern("_")
                        value = pmt.intern("_")
                        self.add_item_tag(0,
                            self.nitems_written(0) + idx,
                            key,
                            value
                        )

                    _num_ones = 0

                # status remains identical
                elif ch == 1:
                    pass
            
            # reset zeros during longer pauses
            if _num_zeros >= 200000:
                _sync = -1
                _num_zeros = 0
                _num_ones = 0

            # this should not happen anyway
            if _num_ones >= 200000:
                _sync = -1
                _num_zeros = 0
                _num_ones = 0

        # simply pass through original signal with tags attached
        output_items[0][:] = input_items[0]

        return len(output_items[0])
