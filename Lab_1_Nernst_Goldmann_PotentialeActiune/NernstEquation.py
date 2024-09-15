"""
    Script utilizat pentru calcularea potentialului membranei neuronale utilizand ecuatia Nernst in conditii normale.
    Se preteaza studierea impactului modificarii concentratiei de K

    autor: Rares Horju
    data: septembrie, 2023
"""

import numpy as np
import matplotlib.pyplot as plt

from matplotlib.widgets import Slider


class NernstEquation:
    def __init__(self):
        self.K_in = 400     # mM
        self.K_out = 20     # mM
        self.z = 1          # valenta potasiumului

    def __call__(self, *args, **kwargs):
        # TODO: completare de catre studenti
        potential = (58 / self.z) * np.log10(self.K_out / self.K_in)

        return potential

    def set_K_in(self, new_K_in: float) -> None:
        self.K_in = new_K_in

    def get_K_in(self) -> float:
        return self.K_in

    def set_K_out(self, new_K_out) -> None:
        self.K_out = new_K_out

    def get_K_out(self) -> float:
        return self.K_out


def plot_resting_potential(ecuatie: NernstEquation) -> None:
    fig, ax = plt.subplots()
    plt.ylim([-120.0, 100.0])

    t = np.linspace(0, 1, 1000)
    line, = ax.plot(t, np.full_like(t, ecuatie()), lw=2)
    ax.set_xlabel('Time [ms]')

    fig.subplots_adjust(bottom=0.25)

    ax_K_in = fig.add_axes([0.25, 0.1, 0.65, 0.015])
    slider_K_in = Slider(
        ax=ax_K_in,
        label='[K]in [mM]',
        valmin=1.0,
        valmax=1000.0,
        valinit=ecuatie.get_K_in()
    )

    ax_K_out = fig.add_axes([0.25, 0.05, 0.65, 0.015])
    slider_K_out = Slider(
        ax=ax_K_out,
        label='[K]out [mM]',
        valmin=1.0,
        valmax=1000.0,
        valinit=ecuatie.get_K_out()
    )

    def update(val):
        ecuatie.set_K_in(slider_K_in.val)
        ecuatie.set_K_out(slider_K_out.val)
        line.set_ydata(np.full_like(t, ecuatie()))
        fig.canvas.draw_idle()

    slider_K_in.on_changed(update)
    slider_K_out.on_changed(update)

    # plt.tight_layout()
    plt.show()


def main():
    ecuatia_Nernst = NernstEquation()

    plot_resting_potential(ecuatia_Nernst)

    return 0


if __name__ == '__main__':
    main()
