import math
import plotly
import plotly.graph_objects as go
from neuron import h
from neuron.units import μm, ms, mV
from matplotlib import pyplot


h.load_file('import3d.hoc')
h.load_file('stdrun.hoc')


class Cell:
    def __init__(self, filename):
        self.load_morphology(filename=filename)
        self.discretize()
        self.add_channels()

    def __str__(self):
        return "Cell"

    def add_channels(self):
        h.hh.insert(self.axon)
        h.hh.insert(self.soma)
        pas_locations = [sec for sec in self.all if sec not in self.axon and sec not in self.soma]
        h.pas.insert(pas_locations)
        for sec in pas_locations:
            for seg in sec:
                seg.pas.g = 1e-6

    def discretize(self):
        freq = 100  # Hz
        d_lambda = 0.1

        for sec in self.all:
            sec.nseg = math.ceil((sec.L / (d_lambda * h.lambda_f(freq))) / 2.) * 2 + 1
            if sec.nseg % 2 == 0:
                sec.nseg += 1
    def load_morphology(self, filename):
        cell = h.Import3d_SWC_read()
        cell.input(filename)
        i3d = h.Import3d_GUI(cell, False)
        i3d.instantiate(self)


if __name__ == '__main__':
    c = Cell(r'c91662.swc')

    syn = h.ExpSyn(c.soma[0](0.5))
    syn.e = 0 * mV
    syn.tau = 2 * ms

    ns = h.NetStim()
    ns.number = 1
    ns.start = 5 * ms

    nc = h.NetCon(ns, syn)
    nc.weight[0] = 1
    nc.delay = 0

    t = h.Vector().record(h._ref_t)
    v = h.Vector().record(c.soma[0](0.5)._ref_v)

    h.finitialize(-65 * mV)
    h.continuerun(50 * ms)

    ps = h.PlotShape(False)
    ps.variable("v")
    ps.scale(-80, 60)
    ps.plot(pyplot).show()
