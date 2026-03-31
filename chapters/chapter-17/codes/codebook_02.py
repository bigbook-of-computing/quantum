"""Ch-17 Project 2: Trotter time evolution fidelity vs time.
Saves: docs/chapters/chapter-17/codes/ch17_trotter_fidelity.png
"""
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
from qiskit import QuantumCircuit, transpile
from qiskit.quantum_info import Statevector
from scipy.linalg import expm

codes_dir = Path('docs/chapters/chapter-17/codes')
codes_dir.mkdir(parents=True, exist_ok=True)

# 2-qubit Heisenberg Hamiltonian
from qiskit.quantum_info import SparsePauliOp
H = SparsePauliOp.from_list([('XX',1.0),('YY',1.0),('ZZ',0.5)]).to_matrix().real
psi0 = Statevector.from_label('01')

t_vals   = np.linspace(0, 2*np.pi, 25)
fid_1    = []   # 1st-order Trotter, dt=0.1
fid_2    = []   # 2nd-order (Suzuki)

n_steps_per_t = 8  # fixed slices per time point

IX = SparsePauliOp.from_list([('XX',1.0)]).to_matrix().real
IY = SparsePauliOp.from_list([('YY',1.0)]).to_matrix().real
IZ = SparsePauliOp.from_list([('ZZ',0.5)]).to_matrix().real

for t in t_vals:
    # Exact
    U_exact = expm(-1j*H*t); sv_exact = Statevector(U_exact @ psi0.data)
    # 1st-order Trotter
    dt = t / n_steps_per_t
    U1 = expm(-1j*IX*dt) @ expm(-1j*IY*dt) @ expm(-1j*IZ*dt)
    U1_t = np.linalg.matrix_power(U1, n_steps_per_t)
    sv1  = Statevector(U1_t @ psi0.data)
    fid_1.append(float(abs(sv_exact.inner(sv1))**2))
    # 2nd-order Suzuki-Trotter
    U2 = (expm(-1j*IX*dt/2) @ expm(-1j*IY*dt/2) @ expm(-1j*IZ*dt)
          @ expm(-1j*IY*dt/2) @ expm(-1j*IX*dt/2))
    U2_t = np.linalg.matrix_power(U2, n_steps_per_t)
    sv2  = Statevector(U2_t @ psi0.data)
    fid_2.append(float(abs(sv_exact.inner(sv2))**2))

fig, ax = plt.subplots(figsize=(8, 4.5))
ax.plot(t_vals, fid_1, 'r-o', markersize=4, label='1st-order Trotter')
ax.plot(t_vals, fid_2, 'b-s', markersize=4, label='2nd-order Suzuki')
ax.set_xlabel('Evolution time t'); ax.set_ylabel('Fidelity with exact')
ax.set_ylim(0, 1.05)
ax.set_title('Chapter 17: Trotter Fidelity vs Evolution Time')
ax.legend(); ax.grid(True, alpha=0.3)
out = codes_dir / 'ch17_trotter_fidelity.png'
fig.savefig(out, dpi=160, bbox_inches='tight'); plt.close(fig)
print(f"Saved figure to: {out}")
