"""
    Script utilizat pentru calcularea potentialului membranei neuronale utilizand ecuatia Goldmann in conditii normale.
    Se preteaza studierea impactului permeabilitatii membranei neuronale.

    autor: Rares Horju
    data: septembrie, 2023
"""

import numpy as np
import matplotlib.pyplot as plt

from matplotlib.widgets import Slider


class GoldmannEquation:
    def __init__(self):
        self.K_permeability = 1
        self.K_in = 400
        self.K_out = 20

        self.Na_permeability = 1
        self.Na_in = 50
        self.Na_out = 440

        self.Cl_permeability = 1
        self.Cl_in = 95
        self.Cl_out = 560

    def __call__(self):
        # TODO: de completat de catre studenti
        Vm = 58 * np.log10((self.K_permeability * self.K_out +
                            self.Na_permeability * self.Na_out +
                            self.Cl_permeability * self.Cl_in) /
                           (self.K_permeability * self.K_in +
                            self.Na_permeability * self.Na_in +
                            self.Cl_permeability * self.Cl_out))

        return Vm


def plot_membrane_potential(ecuatie: GoldmannEquation) -> None:
    fig, ax = plt.subplots()
    plt.ylim([-100.0, 100.0])

    t = np.linspace(0, 1, 1000)
    line, = ax.plot(t, np.full_like(t, ecuatie()), lw=2)
    ax.set_xlabel('Time [ms]')

    fig.subplots_adjust(bottom=0.3)

    ax_K_permeability = fig.add_axes([0.25, 0.15, 0.65, 0.015])
    slider_K_permeability = Slider(
        ax=ax_K_permeability,
        label='P_k',
        valmin=1e-3,
        valmax=1.0,
        valinit=ecuatie.K_permeability
    )

    ax_Na_permeability = fig.add_axes([0.25, 0.10, 0.65, 0.015])
    slider_Na_permeability = Slider(
        ax=ax_Na_permeability,
        label='P_Na',
        valmin=1e-3,
        valmax=1.0,
        valinit=ecuatie.Na_permeability
    )

    ax_Cl_permeability = fig.add_axes([0.25, 0.05, 0.65, 0.015])
    slider_Cl_permeability = Slider(
        ax=ax_Cl_permeability,
        label='P_Cl',
        valmin=1e-3,
        valmax=1.0,
        valinit=ecuatie.Cl_permeability
    )

    def update(val):
        ecuatie.K_permeability = slider_K_permeability.val
        ecuatie.Na_permeability = slider_Na_permeability.val
        ecuatie.Cl_permeability = slider_Cl_permeability.val

        line.set_ydata(np.full_like(t, ecuatie()))
        fig.canvas.draw_idle()

    slider_K_permeability.on_changed(update)
    slider_Na_permeability.on_changed(update)
    slider_Cl_permeability.on_changed(update)

    plt.show()


def main():
    ecuatia_Goldmann = GoldmannEquation()

    plot_membrane_potential(ecuatie=ecuatia_Goldmann)

    return 0


if __name__ == '__main__':
    main()
