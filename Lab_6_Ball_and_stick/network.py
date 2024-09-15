from neuron import h
from neuron.units import ms, mV
from ballandstick import BallAndStick
import matplotlib.pyplot as plt

pc = h.ParallelContext()


class RingNet:
    def __init__(self, n):
        self.cells = [BallAndStick(i) for i in range(n)]

        for cell in self.cells:
            pc.set_gid2node(cell.gid, pc.id())
            pc.cell(cell.gid, cell.nc)

        self.ncs = []
        for postcell in self.cells:
            nc = pc.gid_connect((postcell.gid - 1) % n, postcell.syn)
            nc.delay = 1 * ms
            nc.weight[0] = 0.002
            self.ncs.append(nc)


if __name__ == '__main__':
    net = RingNet(5)
    print(net.cells)

    ns = h.NetStim()
    ns.number = 1
    ns.start = 5 * ms

    nc = h.NetCon(ns, net.cells[0].syn)
    nc.weight[0] = 0.02
    nc.delay = 1 * ms

    h.finitialize(-65 * mV)
    h.continuerun(200 * ms)

    for cell in net.cells:
        print(cell.gid, list(cell.spiketimes))
