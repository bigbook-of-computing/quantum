"""Ch-15 Project 2: Gradient descent vs natural gradient convergence.
Saves: docs/chapters/chapter-15/codes/ch15_gradient_descent.png
"""
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
from qiskit.circuit.library import RealAmplitudes
from qiskit.quantum_info import Statevector, SparsePauliOp

codes_dir = Path('docs/chapters/chapter-15/codes')
codes_dir.mkdir(parents=True, exist_ok=True)

H      = SparsePauliOp.from_list([('ZZ',1.0),('X',[0.3,0.3])]).to_matrix()
ansatz = RealAmplitudes(2, reps=2)
n_p    = ansatz.num_parameters
E_exact = np.linalg.eigvalsh(H)[0]

def energy(theta):
    sv = Statevector(ansatz.assign_parameters(theta)).data
    return float(np.real(sv.conj() @ H @ sv))

def ps_gradients(theta):
    g = np.zeros(n_p)
    for k in range(n_p):
        tp,tm = theta.copy(), theta.copy(); tp[k]+=np.pi/2; tm[k]-=np.pi/2
        g[k] = 0.5*(energy(tp)-energy(tm))
    return g

def qfim_diag(theta):
    """Diagonal approximation of QFIM using parameter-shift."""
    F = np.zeros(n_p)
    for k in range(n_p):
        tp,tm = theta.copy(), theta.copy(); tp[k]+=np.pi/2; tm[k]-=np.pi/2
        sv_plus  = Statevector(ansatz.assign_parameters(tp)).data
        sv_minus = Statevector(ansatz.assign_parameters(tm)).data
        d_sv = (sv_plus - sv_minus) / 2.0
        sv   = Statevector(ansatz.assign_parameters(theta)).data
        F[k] = 4*(np.real(d_sv.conj()@d_sv) - abs(sv.conj()@d_sv)**2)
    return np.clip(F, 1e-6, None)

np.random.seed(0)
theta_gd = np.random.uniform(0, 2*np.pi, n_p)
theta_ng = theta_gd.copy()
lr_gd, lr_ng = 0.1, 0.1
e_gd, e_ng = [energy(theta_gd)], [energy(theta_ng)]

for _ in range(60):
    g = ps_gradients(theta_gd)
    theta_gd -= lr_gd * g
    e_gd.append(energy(theta_gd))
    g2 = ps_gradients(theta_ng)
    F  = qfim_diag(theta_ng)
    theta_ng -= lr_ng * g2 / F   # diagonal natural gradient
    e_ng.append(energy(theta_ng))

fig, ax = plt.subplots(figsize=(8, 4.5))
ax.plot(e_gd, 'b-', linewidth=1.5, label='Gradient Descent')
ax.plot(e_ng, 'r-', linewidth=1.5, label='Natural Gradient (diag QFIM)')
ax.axhline(E_exact, color='k', linestyle='--', linewidth=1, label=f'Exact: {E_exact:.4f}')
ax.set_xlabel('Optimisation step'); ax.set_ylabel('Energy (a.u.)')
ax.set_title('Chapter 15: GD vs Natural Gradient Convergence')
ax.legend(); ax.grid(True, alpha=0.3)
out = codes_dir / 'ch15_gradient_descent.png'
fig.savefig(out, dpi=160, bbox_inches='tight'); plt.close(fig)
print(f"Saved figure to: {out}")
print(f"Final  GD energy: {e_gd[-1]:.6f}  NG energy: {e_ng[-1]:.6f}  exact: {E_exact:.6f}")
