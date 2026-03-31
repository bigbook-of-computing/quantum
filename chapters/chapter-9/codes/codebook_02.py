"""Ch-9 Project 2: ZZFeatureMap Gram matrix heatmap.
Saves: docs/chapters/chapter-9/codes/ch9_gram_matrix.png
"""
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
from qiskit.circuit.library import ZZFeatureMap
from qiskit.quantum_info import Statevector

codes_dir = Path('docs/chapters/chapter-9/codes')
codes_dir.mkdir(parents=True, exist_ok=True)

np.random.seed(0)
n_q = 2; n_pts = 7
X   = np.random.uniform(-np.pi, np.pi, (n_pts, n_q))
fmap = ZZFeatureMap(n_q, reps=2)

def k(x, y):
    sx = Statevector(fmap.assign_parameters(x))
    sy = Statevector(fmap.assign_parameters(y))
    return abs(sx.inner(sy))**2

G = np.array([[k(X[i], X[j]) for j in range(n_pts)] for i in range(n_pts)])

fig, ax = plt.subplots(figsize=(6, 5))
im = ax.imshow(G, cmap='plasma', vmin=0, vmax=1)
plt.colorbar(im, ax=ax, label='⟨φ(x)|φ(y)⟩²')
ax.set_title('Chapter 9: ZZFeatureMap Gram Matrix')
ax.set_xlabel('Sample index'); ax.set_ylabel('Sample index')
out = codes_dir / 'ch9_gram_matrix.png'
fig.savefig(out, dpi=160, bbox_inches='tight'); plt.close(fig)
print(f"Saved figure to: {out}")
