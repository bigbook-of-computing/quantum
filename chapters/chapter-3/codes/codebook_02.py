"""Ch-3 Project 2: GHZ histogram.
Saves: docs/chapters/chapter-3/codes/ch3_ghz_histogram.png
"""
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator

codes_dir = Path('docs/chapters/chapter-3/codes')
codes_dir.mkdir(parents=True, exist_ok=True)

sim = AerSimulator()
fig, axes = plt.subplots(1, 3, figsize=(12, 4))

for ax, n in zip(axes, [2, 3, 4]):
    qc = QuantumCircuit(n); qc.h(0)
    for i in range(n-1): qc.cx(i, i+1)
    qc.measure_all()
    tc = transpile(qc, sim, optimization_level=0)
    counts = sim.run(tc, shots=4096).result().get_counts()
    states = sorted(counts.keys())
    probs  = [counts[s]/4096 for s in states]
    ax.bar(states, probs, color='steelblue')
    ax.set_title(f'{n}-qubit GHZ'); ax.set_ylabel('Probability')
    ax.set_ylim(0, 0.6)
    for tick in ax.get_xticklabels(): tick.set_rotation(45)

fig.suptitle('Chapter 3: GHZ State Measurement Histograms')
plt.tight_layout()
out = codes_dir / 'ch3_ghz_histogram.png'
fig.savefig(out, dpi=160, bbox_inches='tight'); plt.close(fig)
print(f"Saved figure to: {out}")
