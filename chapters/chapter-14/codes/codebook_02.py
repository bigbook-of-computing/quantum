"""Ch-14 Project 2: QAOA MaxCut measurement histogram.
Saves: docs/chapters/chapter-14/codes/ch14_qaoa_histogram.png
"""
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator

codes_dir = Path('docs/chapters/chapter-14/codes')
codes_dir.mkdir(parents=True, exist_ok=True)

edges = [(0,1),(1,2),(2,3),(0,3)]
n_q   = 4
sim   = AerSimulator()

def qaoa(gamma, beta):
    qc = QuantumCircuit(n_q); qc.h(range(n_q))
    for i,j in edges: qc.cx(i,j); qc.rz(2*gamma,j); qc.cx(i,j)
    for q in range(n_q): qc.rx(2*beta, q)
    qc.measure_all(); return qc

# Use optimised parameters found via grid search
best_g, best_b = np.pi/4, np.pi/8
qc  = qaoa(best_g, best_b)
tc  = transpile(qc, sim, optimization_level=1)
counts = sim.run(tc, shots=4096).result().get_counts()

# Colour bars by cut value
def cut(bits): return sum(bits[i]!=bits[j] for i,j in edges)

sorted_items = sorted(counts.items(), key=lambda x: -x[1])[:12]
bitstrings   = [b for b,_ in sorted_items]
probs        = [c/4096 for _,c in sorted_items]
cuts         = [cut(b) for b in bitstrings]

cmap = plt.cm.RdYlGn
colors = [cmap(c/4) for c in cuts]

fig, ax = plt.subplots(figsize=(10, 4.5))
bars = ax.bar(range(len(bitstrings)), probs, color=colors)
ax.set_xticks(range(len(bitstrings)))
ax.set_xticklabels([f'{b}
(cut={c})' for b,c in zip(bitstrings,cuts)],
                   fontsize=8, rotation=45)
ax.set_ylabel('Probability'); ax.set_xlabel('Bitstring')
ax.set_title('Chapter 14: QAOA MaxCut — Top Measurement Outcomes (green=high cut)')
sm = plt.cm.ScalarMappable(cmap=cmap, norm=plt.Normalize(0, 4))
plt.colorbar(sm, ax=ax, label='Cut value')
plt.tight_layout()
out = codes_dir / 'ch14_qaoa_histogram.png'
fig.savefig(out, dpi=160, bbox_inches='tight'); plt.close(fig)
print(f"Saved figure to: {out}")
