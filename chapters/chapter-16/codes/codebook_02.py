"""Ch-16 Project 2: Fidelity vs depolarising noise rate.
Saves: docs/chapters/chapter-16/codes/ch16_noise_fidelity.png
"""
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
from qiskit_aer.noise import NoiseModel, depolarizing_error
from qiskit.quantum_info import Statevector

codes_dir = Path('docs/chapters/chapter-16/codes')
codes_dir.mkdir(parents=True, exist_ok=True)

sim = AerSimulator()
noise_rates = np.linspace(0, 0.15, 16)

# Circuit under test: GHZ state
def ghz_circuit(n):
    qc = QuantumCircuit(n); qc.h(0)
    for i in range(n-1): qc.cx(i, i+1)
    return qc

sv_ideal = {n: Statevector(ghz_circuit(n)) for n in [2,3,4]}
fidelities = {n: [] for n in [2,3,4]}

for p in noise_rates:
    for n in [2,3,4]:
        if p == 0:
            fidelities[n].append(1.0)
        else:
            nm = NoiseModel()
            nm.add_all_qubit_quantum_error(depolarizing_error(p, 1), ['h'])
            nm.add_all_qubit_quantum_error(depolarizing_error(p, 2), ['cx'])
            qc = ghz_circuit(n); qc.save_statevector()
            tc = transpile(qc, sim, optimization_level=0)
            sv_noisy = sim.run(tc, noise_model=nm).result().get_statevector()
            fid = float(abs(sv_ideal[n].inner(Statevector(sv_noisy)))**2)
            fidelities[n].append(fid)

fig, ax = plt.subplots(figsize=(8, 4.5))
for n in [2,3,4]:
    ax.plot(noise_rates, fidelities[n], '-o', markersize=4, label=f'{n}-qubit GHZ')
ax.set_xlabel('Depolarising error rate p'); ax.set_ylabel('State fidelity')
ax.set_title('Chapter 16: GHZ Fidelity vs Depolarising Noise')
ax.legend(); ax.grid(True, alpha=0.3)
out = codes_dir / 'ch16_noise_fidelity.png'
fig.savefig(out, dpi=160, bbox_inches='tight'); plt.close(fig)
print(f"Saved figure to: {out}")
