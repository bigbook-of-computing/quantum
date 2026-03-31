"""Ch-11 Project 2: 2D loss landscape.
Saves: docs/chapters/chapter-11/codes/ch11_loss_landscape.png
"""
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
from qiskit.circuit.library import RealAmplitudes
from qiskit.quantum_info import Statevector, SparsePauliOp

codes_dir = Path('docs/chapters/chapter-11/codes')
codes_dir.mkdir(parents=True, exist_ok=True)

H      = SparsePauliOp.from_list([('ZZ',1.0),('X',[0.5,0])]).to_matrix()
ansatz = RealAmplitudes(2, reps=1)
n_p    = ansatz.num_parameters

np.random.seed(12)
theta0 = np.random.uniform(0, 2*np.pi, n_p)

def energy(t): 
    sv = Statevector(ansatz.assign_parameters(t)).data
    return float(np.real(sv.conj() @ H @ sv))

N = 30
t0_vals = np.linspace(0, 2*np.pi, N)
t1_vals = np.linspace(0, 2*np.pi, N)
E = np.zeros((N, N))
for i, t0 in enumerate(t0_vals):
    for j, t1 in enumerate(t1_vals):
        th = theta0.copy(); th[0] = t0; th[1] = t1
        E[i,j] = energy(th)

fig, ax = plt.subplots(figsize=(7, 5.5))
im = ax.contourf(t0_vals, t1_vals, E, levels=20, cmap='RdYlBu_r')
plt.colorbar(im, ax=ax, label='Energy')
ax.set_xlabel('θ₀ (rad)'); ax.set_ylabel('θ₁ (rad)')
ax.set_title('Chapter 11: 2D Loss Landscape (params 0 & 1 scanned)')
out = codes_dir / 'ch11_loss_landscape.png'
fig.savefig(out, dpi=160, bbox_inches='tight'); plt.close(fig)
print(f"Saved figure to: {out}")
