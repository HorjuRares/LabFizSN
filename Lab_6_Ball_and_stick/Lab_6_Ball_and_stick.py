from neuron import h, gui

h.nrnmpi_init()

pc = h.ParallelContext()

print(f"Hello. I am {pc.id()} of {pc.nhost()}")