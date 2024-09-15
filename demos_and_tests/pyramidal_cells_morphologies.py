from neuron import h, gui
from neuron.units import μm, ms, mV
import itertools
import plotly.graph_objects as go
import sys


h.load_file('import3d.hoc')

print(sys.argv)


class Cell:
    def __init__(self, filename):
        self.load_morphology(filename=filename)

    def __str__(self):
        return "Cell"

    def discretize(self):
        for sec in self.all:
            sec.nseg = int(sec.L) + 1
            if sec.nseg % 2 == 0:
                sec.nseg += 1
    def load_morphology(self, filename):
        cell = h.Import3d_SWC_read()
        cell.input(filename)
        i3d = h.Import3d_GUI(cell, False)
        i3d.instantiate(self)

if __name__ == '__main__':
    c = Cell('c91662.swc')

    all_diams = list(itertools.chain.from_iterable(
        [[sec.diam3d(i) for i in range(sec.n3d())] for sec in h.allsec()]
    ))

    print(f'The minimum diameter is {min(all_diams)} μm')
    print(f'The maximum diameter is {max(all_diams)} μm')

    print(c.all)

    fig = go.Figure()
    for sec in c.all:
        rvp = h.RangeVarPlot('diam', c.soma[0](0.5), sec(1))
        rvp.plot(fig, marker_color='black')

    fig.update_layout({
        'xaxis_title': 'distance from center of soma [μm]',
        'yaxis_title': 'diameter [μm]',
        'title': 'c91662'
    })

    fig.show()

    h.pas.insert(c.all)
    for sec in c.all:
        for seg in sec:
            seg.pas.g = 1e-8

    ic = h.IClamp(c.soma[0](0.5))
    ic.amp = 1  # nA
    ic.delay = 0    # ms
    ic.dur = 100    # ms

    ps = h.PlotShape()
    ps.variable("v")
    ps.scale(-80, 60)
    ps.exec_menu("Shape Plot")

    h.flush_list.append(ps)

    h.finitialize(-65 * mV)
    h.continuerun(50 * ms)
