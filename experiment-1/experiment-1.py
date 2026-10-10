import sys
sys.path.append("..")

import tools.spice as spice
import tools.latex as latex

spice.set_filename("experiment-1")
latex.set_filename("experiment-1")

variables = {}
spice.get_variables(variables)
latex.generate_variables(variables)

spice.plot_voltage(
    "in",
    "out",
    plotname="input-output",
    show_points=(
        ("out", 5e-3, "V(out)max"),
        ("out", 0, "V(out)min"),
    )
)

spice.plot_current(
    "D1", "D2",
    plotname="diode-currents",
    show_points=(
        ("D1", 7.7e-3, "D1 ON"),
        ("D1", 2.3e-3, "D1 OFF"),
        ("D2", 3.7e-3, "D2 ON"),
        ("D2", 6.3e-3, "D2 OFF")
    )
)