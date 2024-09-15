from neuron import h
from numpy import pi


class Cell:
    """cell with hh"""
    def __init__(self):
        # topology
        self.soma = h.Section(name='soma', cell=self)

        # geometry
        self.soma.diam = 10
        self.soma.L = 100 / self.soma.diam / pi
        self.soma.nseg = 1

        # biophysics
        self.soma.insert(h.hh)

        # miscellaneous
        self.root = self.soma
        self.all = self.soma.wholetree()