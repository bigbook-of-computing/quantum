"""Ch-4 Project 2: Bernstein-Vazirani probability histogram.
Saves: docs/chapters/chapter-4/codes/ch4_bv_histogram.png
"""
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator

codes_dir = Path('docs/chapters/chapter-4/codes')
codes_dir.mkdir(parents=True, exist_ok=True)
sim = AerSimulator()

secrets = ['101', '110', '011', '111']
fig, axes = plt.subplots(1, 4, figsize=(14, 4))

for ax, s in zip(axes, secrets):
    n = len(s)
    qc = QuantumCircuit(n+1, n)
    qc.x(n); qc.h(range(n+1))
    for i, b in enumerate(reversed(s)):
        if b == '1': qc.cx(i, n)
    qc.h(range(n)); qc.measure(range(n), range(n))
    tc = transpile(qc, sim, optimization_level=0)
    counts = sim.run(tc, shots=1024).result().get_counts()
    ax.bar(counts.keys(), [v/1024 for v in counts.values()], color='teal')
    ax.set_title(f's = {s}'); ax.set_ylim(0, 1.05)
    ax.set_xlabel('Output bitstring')
    for tick in ax.get_xticklabels(): tick.set_rotation(45)

fig.suptitle("Chapter 4: Bernstein-Vazirani — Output matches secret string")
plt.tight_layout()
out = codes_dir / 'ch4_bv_histogram.png'
fig.savefig(out, dpi=160, bbox_inches='tight'); plt.close(fig)
print(f"Saved figure to: {out}")
