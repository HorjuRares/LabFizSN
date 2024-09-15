from neuron import h
from neuron.units import um, ms, mV
import matplotlib.pyplot as plt

h.load_file('stdrun.hoc')


class BallAndStick:
    def __init__(self, gid):
        self.gid = gid
        self.soma = h.Section(name="soma", cell=self)
        self.dend = h.Section(name="dend", cell=self)
        self.dend.connect(self.soma)

        self.soma.L = self.soma.diam = 10 * um
        self.dend.diam = 2 * um
        self.dend.L = 50 * um

        self.soma.nseg = 1
        self.dend.nseg = 3

        h.hh.insert(self.soma)
        h.pas.insert(self.dend)

        self.syn = h.ExpSyn(self.dend(0.5))
        self.syn.e = 0 * mV
        self.syn.tau = 2 * ms

        self.nc = h.NetCon(self.soma(0.5)._ref_v, None, sec=self.soma)
        self.spiketimes = h.Vector()
        self.nc.record(self.spiketimes)

    def __repr__(self):
        return f"BallAndStick[{self.gid}]"


if __name__ == '__main__':
    cell = BallAndStick(1)
    print(h.topology())

    ns = h.NetStim()
    ns.number = 1
    ns.start = 5 * ms

    nc = h.NetCon(ns, cell.syn)
    nc.weight[0] = 0.002
    nc.delay = 1 * ms

    t = h.Vector().record(h._ref_t)
    v = h.Vector().record(cell.soma(0.5)._ref_v)

    h.finitialize(-65 * mV)
    h.continuerun(20 * ms)

    print(f"spike times: {list(cell.spiketimes)}")

    plt.plot(t, v)
    plt.show()