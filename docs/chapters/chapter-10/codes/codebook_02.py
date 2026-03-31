"""Ch-10 Project 2: Parameter-shift gradient validation plot.
Saves: docs/chapters/chapter-10/codes/ch10_parameter_shift.png
"""
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
from qiskit.circuit.library import RealAmplitudes
from qiskit.quantum_info import Statevector, SparsePauliOp

codes_dir = Path('docs/chapters/chapter-10/codes')
codes_dir.mkdir(parents=True, exist_ok=True)

H     = SparsePauliOp.from_list([('ZZ',0.5),('Z',[-0.3,0.0])]).to_matrix()
ansatz = RealAmplitudes(2, reps=2)
n_p    = ansatz.num_parameters

def energy(theta):
    sv = Statevector(ansatz.assign_parameters(theta)).data
    return float(np.real(sv.conj() @ H @ sv))

np.random.seed(3)
theta0 = np.random.uniform(0, 2*np.pi, n_p)
eps    = 1e-5

grad_ps = np.zeros(n_p)
grad_fd = np.zeros(n_p)
for k in range(n_p):
    tp, tm = theta0.copy(), theta0.copy()
    tp[k] += np.pi/2; tm[k] -= np.pi/2
    grad_ps[k] = 0.5*(energy(tp) - energy(tm))
    te, tf = theta0.copy(), theta0.copy()
    te[k] += eps; tf[k] -= eps
    grad_fd[k] = (energy(te) - energy(tf)) / (2*eps)

fig, axes = plt.subplots(1, 2, figsize=(10, 4.5))
axes[0].scatter(grad_fd, grad_ps, s=30, color='teal', alpha=0.8)
mn, mx = min(grad_fd.min(), grad_ps.min()), max(grad_fd.max(), grad_ps.max())
axes[0].plot([mn,mx],[mn,mx], 'r--', linewidth=1); axes[0].set_aspect('equal')
axes[0].set_xlabel('Finite-difference gradient'); axes[0].set_ylabel('Parameter-shift gradient')
axes[0].set_title('PS vs FD gradient (should lie on y=x)')

axes[1].bar(range(n_p), np.abs(grad_ps - grad_fd), color='salmon')
axes[1].set_xlabel('Parameter index'); axes[1].set_ylabel('|PS − FD|')
axes[1].set_title('Gradient residuals')

fig.suptitle('Chapter 10: Parameter-Shift Gradient Validation')
plt.tight_layout()
out = codes_dir / 'ch10_parameter_shift.png'
fig.savefig(out, dpi=160, bbox_inches='tight'); plt.close(fig)
print(f"Saved figure to: {out}")
print(f"Max |PS-FD| residual: {np.max(np.abs(grad_ps-grad_fd)):.2e}")
