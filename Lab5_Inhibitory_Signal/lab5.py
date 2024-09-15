"""
    LABORATORUL NR. 5: RETELE DE NEURONI
    Autor: Horju Rares
    Data: 07.11.2023
"""

from neuron import h
from neuron.units import ms, mV
import matplotlib.pyplot as plt
from Lab4_Nets.passive_cell import Cell

h.load_file('stdrun.hoc')

if __name__ == '__main__':
    # initialize the passive cell
    my_cell = Cell()

    # define the synaptic mechanism
    syn = h.ExpSyn(my_cell.soma(0.5), sec=my_cell.soma)
    syn.tau = 2
    syn.e = -66

    pre_syn = h.NetStim()
    pre_syn.start = 5 * ms
    pre_syn.interval = 10 * ms
    pre_syn.number = 1  # average number of spikes
    pre_syn.noise = 0   # fully deterministic behaviour

    nc = h.NetCon(pre_syn, syn)
    nc.weight[0] = 1.57e-2
    nc.delay = 1 * ms

    t = h.Vector().record(h._ref_t)
    v = h.Vector().record(my_cell.soma(0.5)._ref_v)

    h.finitialize(-65 * mV)
    h.continuerun(100 * ms)

    # plt.ylim([-100, 50])
    plt.plot(t, v)
    plt.show()