"""Ch-18 Project 2: Gaussian amplitude distribution bar chart.
Saves: docs/chapters/chapter-18/codes/ch18_gaussian_encoding.png
"""
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector

codes_dir = Path('docs/chapters/chapter-18/codes')
codes_dir.mkdir(parents=True, exist_ok=True)

def load_gaussian(n_q, mu=0.0, sigma=1.0):
    N = 2**n_q
    x = np.linspace(-3, 3, N)
    p = np.exp(-0.5*((x-mu)/sigma)**2)
    p /= np.linalg.norm(p)
    qc = QuantumCircuit(n_q)
    qc.initialize(p, range(n_q))
    sv = Statevector(qc).data
    return x, p**2, np.abs(sv)**2

fig, axes = plt.subplots(1, 3, figsize=(14, 4))
for ax, n_q in zip(axes, [3, 4, 5]):
    x, p_target, p_loaded = load_gaussian(n_q)
    ax.bar(range(len(x)), p_loaded, alpha=0.6, color='steelblue', label='Loaded')
    ax.plot(range(len(x)), p_target, 'r-', linewidth=1.5, label='Target')
    ax.set_title(f'{n_q} qubits ({2**n_q} bins)')
    ax.set_xlabel('Bin index'); ax.set_ylabel('Probability')
    ax.legend(fontsize=8)

fig.suptitle('Chapter 18: Gaussian Amplitude Encoding Quality')
plt.tight_layout()
out = codes_dir / 'ch18_gaussian_encoding.png'
fig.savefig(out, dpi=160, bbox_inches='tight'); plt.close(fig)
print(f"Saved figure to: {out}")
