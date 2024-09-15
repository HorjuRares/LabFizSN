from neuron import h
from neuron.units import ms, mV
import numpy as np
import matplotlib.pyplot as plt


def main():
  h.load_file('stdrun.hoc')

  soma = h.Section(name='soma')
  axon = h.Section(name='axon')
  axon.connect(soma(0))

  soma.nseg = 1
  soma.diam = soma.L = 18.8

  axon.nseg = 101
  axon.diam = 4
  axon.L = 1000

  stim = h.IClamp(soma(0.5))
  stim.delay = 100 * ms
  stim.dur = 1 * ms
  stim.amp = 20

  for sec in [soma, axon]:
    sec.Ra = 123
    sec.insert('hh')

  v = list()
  t = h.Vector().record(h._ref_t)
  points = np.linspace(0, 1, 10)
  for i in range(points.shape[0]):
    v.append(h.Vector().record(axon(points[i])._ref_v))

  h.finitialize(-65 * mV)
  h.continuerun(300 * ms)

  for i in range(points.shape[0]):
    plt.plot(t, v[i])

  plt.xlim((99, 110))
  plt.show()

  return 0

if __name__ == '__main__':
  main()
