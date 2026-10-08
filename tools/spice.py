import matplotlib.pyplot as plt
from matplotlib.ticker import EngFormatter, MaxNLocator
from spicelib import SpiceEditor
from spicelib import RawRead
import os

filename = None

def set_filename(name: str):
    global filename 
    filename = name

def get_variables(variables: dict):
    netlist = SpiceEditor(f"{filename}.cir")

    for component in netlist.get_components():
        value = netlist.get_component_value(component)
        if value.startswith("PULSE("):
            params = value.removeprefix("PULSE(").removesuffix(")").split()
            variables[f"{component}Min"] = params[0]
            variables[f"{component}Max"] = params[1]
            variables[f"{component}Tdelay"] = params[2]
            variables[f"{component}Trise"] = params[3]
            variables[f"{component}Tfall"] = params[4]
            variables[f"{component}Ton"] = params[5]
            variables[f"{component}Tperiod"] = params[6]
            variables[f"{component}PP"] = f"{float(params[1]) - float(params[0]):g}"
        else:
            variables[component] = value

def plot_current(*components, plotname):
    os.makedirs("figures", exist_ok=True)

    raw = RawRead(f"{filename}.raw")

    time = raw.get_trace("time").get_wave()
    for component in components:
        current = raw.get_trace(f"I({component})").get_wave()
        plt.plot(time, current, linewidth=2.0, label=f"I({component})")

    plt.ylabel("Current", fontsize=10)
    plt.gca().yaxis.set_major_locator(MaxNLocator(nbins=10))
    plt.gca().yaxis.set_major_formatter(EngFormatter(unit="A"))

    plt.xlabel("Time", fontsize=10)
    plt.gca().xaxis.set_major_locator(MaxNLocator(nbins=11))
    plt.gca().xaxis.set_major_formatter(EngFormatter(unit="s"))
    plt.xlim(time[0], time[-1])

    plt.axhline(0, color='gray', linestyle='--', linewidth=0.8, alpha=0.6)
    
    plt.grid(True, linestyle=':', alpha=0.6)
    plt.tight_layout()

    plt.legend(loc="upper right")

    plt.savefig(f"figures/{filename}-{plotname}.pdf", bbox_inches="tight")

def plot_voltage(*measurements, plotname):
    raw = RawRead(f"{filename}.raw")

    time = raw.get_trace("time").get_wave()
    for measurement in measurements:
        if isinstance(measurement, str):
            positive = measurement
            negative = "0"
        elif isinstance(measurement, tuple) and len(measurement) == 2:
            positive, negative = measurement
        else:
            raise ValueError("Voltage measurement must be a node string or a pair of nodes.")

        positive_voltage = raw.get_trace(f"V({positive})").get_wave()

        if negative == "0":
            voltage = positive_voltage
            label = f"V({positive})"
        else:
            negative_voltage = raw.get_trace(f"V({negative})").get_wave()
            voltage = positive_voltage - negative_voltage
            label = f"V({positive}) - V({negative})"

        plt.plot(time, voltage, linewidth=2.0, label=label)

    plt.ylabel("Voltage", fontsize=10)
    plt.gca().yaxis.set_major_locator(MaxNLocator(nbins=10))
    plt.gca().yaxis.set_major_formatter(EngFormatter(unit="V"))

    plt.xlabel("Time", fontsize=10)
    plt.gca().xaxis.set_major_locator(MaxNLocator(nbins=11))
    plt.gca().xaxis.set_major_formatter(EngFormatter(unit="s"))
    plt.xlim(time[0], time[-1])

    plt.axhline(0, color='gray', linestyle='--', linewidth=0.8, alpha=0.6)

    plt.grid(True, linestyle=":", alpha=0.6)
    plt.tight_layout()

    plt.legend(loc="upper right")

    plt.savefig(f"figures/{filename}-{plotname}.pdf", bbox_inches="tight")