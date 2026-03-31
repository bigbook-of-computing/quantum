"""Ch-6 Project 2: QAOA MaxCut + energy convergence.
Saves: docs/chapters/chapter-6/codes/ch6_vqe_convergence.png
"""
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
from qiskit.circuit.library import RealAmplitudes
from qiskit.quantum_info import Statevector, SparsePauliOp

codes_dir = Path('docs/chapters/chapter-6/codes')
codes_dir.mkdir(parents=True, exist_ok=True)

H     = SparsePauliOp.from_list([('XX',1.0),('YY',1.0),('ZZ',1.0)])
H_mat = H.to_matrix()
E_exact = np.linalg.eigvalsh(H_mat.real)[0]

ansatz = RealAmplitudes(2, reps=2)
n_par  = ansatz.num_parameters

def energy(theta):
    sv = Statevector(ansatz.assign_parameters(theta)).data
    return float(np.real(sv.conj() @ H_mat @ sv))

np.random.seed(0)
theta = np.random.uniform(0, 2*np.pi, n_par)
energies = [energy(theta)]
for _ in range(60):
    grads = np.zeros(n_par)
    for k in range(n_par):
        tp, tm = theta.copy(), theta.copy()
        tp[k] += np.pi/2; tm[k] -= np.pi/2
        grads[k] = 0.5*(energy(tp) - energy(tm))
    theta -= 0.2*grads
    energies.append(energy(theta))

fig, ax = plt.subplots(figsize=(8, 4.5))
ax.plot(energies, 'b-o', markersize=3, label='VQE energy')
ax.axhline(E_exact, color='red', linestyle='--', linewidth=1.5, label=f'Exact: {E_exact:.4f}')
ax.set_xlabel('Optimisation step'); ax.set_ylabel('Energy (a.u.)')
ax.set_title('Chapter 6: VQE Convergence — Heisenberg 2-qubit')
ax.legend(); ax.grid(True, alpha=0.3)
out = codes_dir / 'ch6_vqe_convergence.png'
fig.savefig(out, dpi=160, bbox_inches='tight'); plt.close(fig)
print(f"Saved figure to: {out}")
print(f"Final VQE energy: {energies[-1]:.6f}  exact: {E_exact:.6f}")
