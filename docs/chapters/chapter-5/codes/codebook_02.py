"""Ch-5 Project 2: QFT period finding histogram.
Saves: docs/chapters/chapter-5/codes/ch5_qft_histogram.png
"""
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
from qiskit import QuantumCircuit, transpile
from qiskit.circuit.library import QFT
from qiskit_aer import AerSimulator

codes_dir = Path('docs/chapters/chapter-5/codes')
codes_dir.mkdir(parents=True, exist_ok=True)
sim = AerSimulator()

# Prepare periodic state |x> + |x+r> + |x+2r> via phase kickback, then QFT
# Simplified: use column of phase oracle to create periodic state
n = 4
periods = [2, 4]
fig, axes = plt.subplots(1, 2, figsize=(11, 4.5))

for ax, period in zip(axes, periods):
    # Build periodic state manually
    amps = np.zeros(2**n)
    for k in range(0, 2**n, period): amps[k] = 1.0
    amps /= np.linalg.norm(amps)
    qc = QuantumCircuit(n)
    qc.initialize(amps, range(n))
    qc.compose(QFT(n), inplace=True)
    qc.measure_all()
    tc = transpile(qc, sim, optimization_level=0)
    counts = sim.run(tc, shots=4096).result().get_counts()
    top10 = sorted(counts.items(), key=lambda x: -x[1])[:8]
    bitstrings = [b for b,_ in top10]
    probs = [c/4096 for _,c in top10]
    ax.bar(range(len(bitstrings)), probs, color='steelblue')
    ax.set_xticks(range(len(bitstrings))); ax.set_xticklabels(bitstrings, rotation=45, fontsize=8)
    ax.set_title(f'Period r={period}: top peaks at multiples of {2**n//period}')
    ax.set_ylabel('Probability')

fig.suptitle('Chapter 5: QFT Period Finding — Frequency Peaks Reveal Period')
plt.tight_layout()
out = codes_dir / 'ch5_qft_histogram.png'
fig.savefig(out, dpi=160, bbox_inches='tight'); plt.close(fig)
print(f"Saved figure to: {out}")
