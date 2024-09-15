import numpy as np
import matplotlib.pyplot as plt


class HodgkinHuxleyModel:
    """
    Modelul Hodgkin-Huxley urmareste determinarea potentialului trans-membrana prin studierea efectului intensitatii
    curentului total ce este aplicat asupra celulei (extern + Na + K + Cl). Modificarea conductantei fiecarui element
    chimic duce la modificarea potentialului membranei neuronale.
    """

    class IonGate:
        """
        Clasa utilizata pentru a simula functionarea portilor ionice, acestea respectand kinetica de ordinul intai
        d.p.d.v. al reactiilor chimice
        """
        def __init__(self):
            self.alpha = 0
            self.beta = 0
            self.state = 0

        def update(self, delta_T_ms: float = 0.05):
            alpha_state = self.alpha * (1.0 - self.state)
            beta_state = self.beta * self.state
            self.state += delta_T_ms * (alpha_state - beta_state)

        def set_infinite_state(self):
            self.state = self.alpha / (self.alpha + self.beta)

    def __init__(self, starting_voltage: float = 0):
        self.E_Na = 115
        self.E_K = -12
        self.E_K_leak = 10.6

        self.g_Na = 120
        self.g_K = 36
        self.g_K_leak = 0.3

        self.C = 1

        self.V_m = starting_voltage

        self.m = self.IonGate()
        self.n = self.IonGate()
        self.h = self.IonGate()

        self.update_gate_time_constants()

        self.m.set_infinite_state()
        self.n.set_infinite_state()
        self.h.set_infinite_state()

    def update_gate_time_constants(self) -> None:
        """
        metoda ce realizeaza actualizare constantelor de timp pentru fiecare tip de poarta ionica
        :param V_m: potentialul membranei
        :return: None
        """
        self.n.alpha = 0.01 * ((10 - self.V_m) / (np.exp((10 - self.V_m) / 10) -1))
        self.n.beta = 0.125 * np.exp(-self.V_m / 80)

        self.m.alpha = 0.1 * ((25 - self.V_m) / (np.exp((25 - self.V_m) / 10) - 1))
        self.m.beta = 4 * np.exp(-self.V_m / 18)

        self.h.alpha = 0.07 * np.exp(-self.V_m / 20)
        self.h.beta = 1 / (np.exp((30 - self.V_m) / 10) + 1)

    def update_cell_voltage(self, stimulus_current: float = 0, delta_T_ms: float = 0.05) -> None:
        """
        metoda folosita pentru determinarea curentilor utilizand
        constantele de timp recent calculate ale portilor ionice
        :param stimulus_current: curentul stimulator extern
        :param delta_T_ms: constanta de timp
        :return: None
        """
        I_Na = np.power(self.m.state, 3) * self.g_Na * self.h.state * (self.V_m - self.E_Na)
        I_K = np.power(self.n.state, 4) * self.g_K * (self.V_m - self.E_K)
        I_K_leak = self.g_K_leak * (self.V_m - self.E_K_leak)
        I_sum = stimulus_current - I_Na - I_K - I_K_leak

        self.V_m += I_sum * delta_T_ms / self.C

    def update_gate_states(self, delta_T_ms: float = 0.05) -> None:
        """
        metoda utilizata pentru determinarea gradului de deschidere a
        portilor ionice in functie de cea mai recenta valoare a lui V_m
        :param delta_T_ms: constanta de timp
        :return: None
        """
        self.m.update(delta_T_ms=delta_T_ms)
        self.h.update(delta_T_ms=delta_T_ms)
        self.n.update(delta_T_ms=delta_T_ms)

    def update_on_iteration(self, stimulus_current: float = 0, delta_T_ms: float = 0.05):
        self.update_gate_time_constants()
        self.update_cell_voltage(stimulus_current=stimulus_current, delta_T_ms=delta_T_ms)
        self.update_gate_states(delta_T_ms=delta_T_ms)


def main():
    hh_model = HodgkinHuxleyModel(starting_voltage=0)

    pointCount = 5000
    voltages = np.empty(pointCount)
    times = np.arange(pointCount) * 0.05
    stim = np.zeros(pointCount)
    stim[1200:1800] = 0    # creaza un impuls treapta unitara

    for i in range(len(times)):
        hh_model.update_on_iteration(stimulus_current=stim[i], delta_T_ms=0.05)
        voltages[i] = hh_model.V_m

    f, (ax1, ax2) = plt.subplots(2, 1, sharex=True, figsize=(8, 5),
                                 gridspec_kw={'height_ratios': [3, 1]})

    ax1.plot(times, voltages - 70, 'b')
    ax1.set_ylabel("Membrane Potential (mV)")
    ax1.set_title("Hodgkin-Huxley Spiking Neuron Model")
    ax1.spines['right'].set_visible(False)
    ax1.spines['top'].set_visible(False)
    ax1.spines['bottom'].set_visible(False)
    ax1.tick_params(bottom=False)

    ax2.plot(times, stim, 'r')
    ax2.set_ylabel("Stimulus (µA/cm²)")
    ax2.set_xlabel("Simulation Time (milliseconds)")
    ax2.spines['right'].set_visible(False)
    ax2.spines['top'].set_visible(False)

    plt.margins(0, 0.1)
    plt.tight_layout()
    plt.show()

    return 0


if __name__ == '__main__':
    main()
