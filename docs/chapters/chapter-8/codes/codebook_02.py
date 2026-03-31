"""Ch-8 Project 2: Kernel matrix heatmap.
Saves: docs/chapters/chapter-8/codes/ch8_kernel_heatmap.png
"""
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
from qiskit.circuit.library import ZZFeatureMap
from qiskit.quantum_info import Statevector

codes_dir = Path('docs/chapters/chapter-8/codes')
codes_dir.mkdir(parents=True, exist_ok=True)

np.random.seed(42)
n_features, n_samples = 2, 8
X = np.random.uniform(-np.pi, np.pi, (n_samples, n_features))
fmap = ZZFeatureMap(n_features, reps=1)

def kernel_entry(x, y):
    sv_x = Statevector(fmap.assign_parameters(x))
    sv_y = Statevector(fmap.assign_parameters(y))
    return abs(sv_x.inner(sv_y))**2

K = np.array([[kernel_entry(X[i], X[j]) for j in range(n_samples)]
              for i in range(n_samples)])

fig, ax = plt.subplots(figsize=(6.5, 5.5))
im = ax.imshow(K, cmap='viridis', vmin=0, vmax=1)
plt.colorbar(im, ax=ax, label='Kernel value')
ax.set_title('Chapter 8: ZZFeatureMap Quantum Kernel Matrix')
ax.set_xlabel('Sample index'); ax.set_ylabel('Sample index')
for i in range(n_samples):
    for j in range(n_samples):
        ax.text(j, i, f'{K[i,j]:.2f}', ha='center', va='center',
                fontsize=7, color='white' if K[i,j] < 0.5 else 'black')
out = codes_dir / 'ch8_kernel_heatmap.png'
fig.savefig(out, dpi=160, bbox_inches='tight'); plt.close(fig)
print(f"Saved figure to: {out}")
