# STEPS:    1.
#           2.
#           3.
# COMMUNICATION BETWEEN CELLS:  1. GAP JUNCTIONS
#                               2. SYNAPTIC TRANSMISSION - GRADED   gsyn_post = f(V_pre)
#                                                                   in NEURON: pointers
#                                                        - SPIKING  spike in presynaptic terminal triggers transmiter
#                                                                   release
#                                                                   postsynaptic effect described by DE or kinectic
#                                                                   scheme that is perturbed by the occurence of a
#                                                                   presynaptic spike
# Efficient divergence
# Efficient convergence

"""
    LABORATORUL NR. 4: RETELE DE NEURONI
    Autor: Horju Rares
    Data: 30.10.2023
"""

PASSIVEMODEL = True

from neuron import h, gui
import numpy as np

if PASSIVEMODEL:
    from passive_cell import Cell
    PRESTART = 5    # ms
    WEIGHT = -7.2e-6 # elicits 1 mV EPSP in passive model
else:
    from hh_cell import Cell
    PRESTART = 25       # ms
    WEIGHT = -1.57e-5    # elicits 1 mV EPSP


if __name__ == '__main__':
    cell = Cell()
    # synaptic mechanism
    syn = h.ExpSyn(cell.soma(0.5), sec=cell.soma)
    syn.tau = 3
    syn.e = 0

    # presynaptic spike source
    pre = h.NetStim()
    pre.start = PRESTART
    pre.interval = 10
    pre.number = 1
    pre.noise = 0   # fully deterministic behaviour

    nc = h.NetCon(pre, syn)
    nc.delay = 1
    nc.weight[0] = WEIGHT

    h.load_file("rig.ses")