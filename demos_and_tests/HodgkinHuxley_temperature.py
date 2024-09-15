from neuron import h
from neuron.units import μm, ms, mV
import plotly.graph_objects as go
import efel


h.load_file("stdrun.hoc")

efel.setDoubleSetting("DownDerivativeThreshold", 0)
efel.setDoubleSetting("interp_step", 0.005)

soma = h.Section(name='soma')
soma.L = soma.diam = 10 * μm
h.hh.insert(soma)

syn = h.ExpSyn(soma(0.5))
syn.e = 0 * mV
syn.tau = 2 * ms

ns = h.NetStim()
ns.start = 5 * ms
ns.number = 1

nc = h.NetCon(ns, syn)
nc.weight[0] = 0.001
nc.delay = 0.0

t = h.Vector().record(h._ref_t)
v = h.Vector().record(soma(0.5)._ref_v)

data = {
    'AP_duration': [],
    'spike_half_width': [],
    'celsius': []
}

for h.celsius in [i * 1 for i in range(10)]:
    h.finitialize(-65 * mV)
    h.continuerun(50 * ms)

    go.Figure().add_trace(go.Scatter(x=t, y=v)).show()

    trace = {"T": t, "V": v, "stim_start": [5 * ms], "stim_end": [50 * ms]}
    traces = [trace]

    features = efel.getFeatureValues(traces, ["AP_duration", "spike_half_width"])[0]

    data['AP_duration'].extend(features['AP_duration'])
    data['spike_half_width'].extend(features['spike_half_width'])
    data['celsius'].append(h.celsius)

for yvar in ["AP_duration", "spike_half_width"]:
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=data["celsius"], y=data[yvar]))
    fig.update_layout({
        "xaxis_title": "Celsius",
        "yaxis_title":yvar
    })
    fig.show()
