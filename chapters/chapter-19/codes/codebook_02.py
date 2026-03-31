"""Ch-19 Project 2: T1/T2 decoherence decay curves.
Saves: docs/chapters/chapter-19/codes/ch19_decoherence.png
"""
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
from qiskit_aer.noise import NoiseModel, thermal_relaxation_error

codes_dir = Path('docs/chapters/chapter-19/codes')
codes_dir.mkdir(parents=True, exist_ok=True)

sim = AerSimulator()
T1, T2 = 50e-6, 30e-6   # seconds (50 μs, 30 μs)
t_vals  = np.linspace(0, 5*T1, 30)
pop1_t1 = []  # population in |1> after T1 decay
pop1_t2 = []  # coherence decay via T2

for t in t_vals:
    # T1 decay: start in |1>, let it relax
    if t == 0:
        pop1_t1.append(1.0); pop1_t2.append(1.0); continue
    nm = NoiseModel()
    err = thermal_relaxation_error(T1, T2, t)
    nm.add_all_qubit_quantum_error(err, ['id'])
    qc_t1 = QuantumCircuit(1)
    qc_t1.x(0); qc_t1.id(0); qc_t1.measure_all()
    tc = transpile(qc_t1, sim, optimization_level=0)
    counts = sim.run(tc, noise_model=nm, shots=2048).result().get_counts()
    pop1_t1.append(counts.get('1',0)/2048)

    # T2 Ramsey: start in |+>, let it dephase
    qc_t2 = QuantumCircuit(1)
    qc_t2.h(0); qc_t2.id(0); qc_t2.h(0); qc_t2.measure_all()
    tc = transpile(qc_t2, sim, optimization_level=0)
    counts = sim.run(tc, noise_model=nm, shots=2048).result().get_counts()
    pop1_t2.append(counts.get('0',0)/2048)  # should decay with T2

t_us = t_vals * 1e6  # convert to μs
exp_T1 = np.exp(-t_vals/T1)
exp_T2 = 0.5*(1 + np.exp(-t_vals/T2))

fig, axes = plt.subplots(1, 2, figsize=(11, 4.5))
axes[0].plot(t_us, exp_T1, 'r--', linewidth=1.5, label='Theory: e^(-t/T1)')
axes[0].scatter(t_us, pop1_t1, s=20, color='red', alpha=0.8, label='Simulation')
axes[0].set_xlabel('Time (μs)'); axes[0].set_ylabel('P(|1⟩)')
axes[0].set_title(f'T1 Relaxation (T1={T1*1e6:.0f} μs)'); axes[0].legend()
axes[0].grid(True, alpha=0.3)

axes[1].plot(t_us, exp_T2, 'b--', linewidth=1.5, label='Theory: ½(1+e^(-t/T2))')
axes[1].scatter(t_us, pop1_t2, s=20, color='blue', alpha=0.8, label='Simulation')
axes[1].set_xlabel('Time (μs)'); axes[1].set_ylabel('P(|0⟩) Ramsey')
axes[1].set_title(f'T2 Dephasing (T2={T2*1e6:.0f} μs)'); axes[1].legend()
axes[1].grid(True, alpha=0.3)

fig.suptitle('Chapter 19: Qubit Decoherence — T1 and T2 Decay Curves')
plt.tight_layout()
out = codes_dir / 'ch19_decoherence.png'
fig.savefig(out, dpi=160, bbox_inches='tight'); plt.close(fig)
print(f"Saved figure to: {out}")
