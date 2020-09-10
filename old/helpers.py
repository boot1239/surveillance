import math
import random

from tkinter import CURRENT


class HyperlinkManager:
    def __init__(self, text):

        self.text = text

        self.text.tag_config("hyper")

        self.text.tag_bind("hyper", "<Enter>", self._enter)
        self.text.tag_bind("hyper", "<Leave>", self._leave)
        self.text.tag_bind("hyper", "<Button-1>", self._click)
        self.links = {}
        self.reset()

    def reset(self):
        self.links = {}

    def add(self, action, args):
        # add an action to the manager.  returns tags to use in
        # associated text widget
        tag = "hyper-%d" % len(self.links)
        self.links[tag] = (action, args)
        return "hyper", tag

    def _enter(self, event):
        self.text.config(cursor="hand2")

    def _leave(self, event):
        self.text.config(cursor="")

    def _click(self, event):
        for tag in self.text.tag_names(CURRENT):
            if tag[:6] == "hyper-":
                self.links[tag][0](self.links[tag][1], clicked=True)
                return


def print_progress_bar(
        iteration, total, prefix='progress', suffix='complete', decimals=1,
        length=50, fill='█', print_end="\r"
):
    percent = (
        ("{0:." + str(decimals) + "f}")
            .format(100 * (iteration / float(total)))
    )
    filled_length = int(length * iteration // total)
    bar = fill * filled_length + '-' * (length - filled_length)
    print('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix), end=print_end)
    if iteration == total:
        print()


def random_range(start, stop=None, step=None):
    # Set a default values the same way "range" does.
    if stop is None:
        start, stop = 0, start
    if step is None:
        step = 1

    # Use a mapping to convert a standard range into the desired range.

    def mapping(i):
        return (i * step) + start

    # Compute the number of numbers in this range.
    maximum = (stop - start) // step
    # Seed range with a random integer.
    value = random.randint(0, maximum)

    # Construct an offset, multiplier, and modulus for a linear
    # congruential generator. These generators are cyclic and
    # non-repeating when they maintain the properties:
    #   1) "modulus" and "offset" are relatively prime.
    #   2) ["multiplier" - 1] is divisible by all prime factors of "modulus".
    #   3) ["multiplier" - 1] is divisible by 4 if "modulus" is divisible by 4.

    # Pick a random odd-valued offset.
    offset = random.randint(0, maximum) * 2 + 1

    # Pick a multiplier 1 greater than a multiple of 4.
    multiplier = 4 * (maximum // 4) + 1
    # Pick a modulus just big enough to generate all numbers (power of 2).
    modulus = int(2 ** math.ceil(math.log2(maximum)))
    # Track how many random numbers have been returned.
    found = 0
    while found < maximum:
        # If this is a valid value, yield it in generator fashion.
        if value < maximum:
            found += 1
            yield mapping(value)

        # Calculate the next value in the sequence.
        value = (value * multiplier + offset) % modulus
