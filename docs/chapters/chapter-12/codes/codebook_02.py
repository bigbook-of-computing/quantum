"""Ch-12 Project 2: Quantum k-means cluster scatter.
Saves: docs/chapters/chapter-12/codes/ch12_qkmeans_clusters.png
"""
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
from qiskit.quantum_info import Statevector
from qiskit.circuit.library import ZZFeatureMap

codes_dir = Path('docs/chapters/chapter-12/codes')
codes_dir.mkdir(parents=True, exist_ok=True)

np.random.seed(7)
# Two well-separated clusters in 2D
cluster_A = np.random.randn(10, 2) + np.array([2.0,  0.0])
cluster_B = np.random.randn(10, 2) + np.array([-2.0, 0.0])
X = np.vstack([cluster_A, cluster_B])
X_scaled = X / np.max(np.abs(X)) * np.pi  # scale to [-pi, pi]

fmap = ZZFeatureMap(2, reps=1)

def kernel(x, y):
    sx = Statevector(fmap.assign_parameters(x))
    sy = Statevector(fmap.assign_parameters(y))
    return abs(sx.inner(sy))**2

# Quantum k-means (k=2): assign to centroid with highest kernel value
centres = X_scaled[[0, 19]]
labels  = np.zeros(20, dtype=int)
for _ in range(5):
    for i in range(20):
        sims = [kernel(X_scaled[i], c) for c in centres]
        labels[i] = int(np.argmax(sims))
    for c in range(2):
        mask = labels == c
        if mask.any(): centres[c] = X_scaled[mask].mean(axis=0)

fig, ax = plt.subplots(figsize=(7, 5))
colors = ['steelblue', 'tomato']
for c in range(2):
    mask = labels == c
    ax.scatter(X[mask, 0], X[mask, 1], c=colors[c], s=50, label=f'Cluster {c}', alpha=0.8)
ax.scatter(*centres.T, marker='*', s=200, c=['navy','darkred'], zorder=5, label='Centroids')
ax.set_xlabel('Feature 1'); ax.set_ylabel('Feature 2')
ax.set_title('Chapter 12: Quantum k-Means Clustering (Kernel Space)')
ax.legend(); ax.grid(True, alpha=0.3)
out = codes_dir / 'ch12_qkmeans_clusters.png'
fig.savefig(out, dpi=160, bbox_inches='tight'); plt.close(fig)
print(f"Saved figure to: {out}")
