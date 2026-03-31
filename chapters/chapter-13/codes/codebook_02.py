"""Ch-13 Project 2: Q-table convergence line plot.
Saves: docs/chapters/chapter-13/codes/ch13_qtable_convergence.png
"""
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
from qiskit.circuit.library import RealAmplitudes
from qiskit.quantum_info import Statevector, SparsePauliOp

codes_dir = Path('docs/chapters/chapter-13/codes')
codes_dir.mkdir(parents=True, exist_ok=True)

np.random.seed(2)
n_q    = 2
ansatz = RealAmplitudes(n_q, reps=2)
n_p    = ansatz.num_parameters

# Quantum approximate Q-function: 4 actions = 4 Pauli observables
Hs = [SparsePauliOp(p).to_matrix() for p in ['ZI','IZ','XX','YY']]

def q_values(theta):
    sv = Statevector(ansatz.assign_parameters(theta)).data
    return [float(np.real(sv.conj() @ H @ sv)) for H in Hs]

# Simulate Q-learning update with a simple 1-state MDP, 4 actions, reward=+1 for action 2
theta = np.random.uniform(0, 2*np.pi, n_p); lr=0.1; gamma=0.9
mse_history = []
true_Q = [0.1, 0.1, 1.0/(1-gamma), 0.1]

for step in range(60):
    qv  = q_values(theta)
    mse = sum((qv[a]-true_Q[a])**2 for a in range(4)) / 4
    mse_history.append(mse)
    grads = np.zeros(n_p)
    for a, tq in enumerate(true_Q):
        delta = qv[a] - tq
        for k in range(n_p):
            tp,tm = theta.copy(), theta.copy(); tp[k]+=np.pi/2; tm[k]-=np.pi/2
            sv_p = Statevector(ansatz.assign_parameters(tp)).data
            sv_m = Statevector(ansatz.assign_parameters(tm)).data
            dHdth = 0.5*(float(np.real(sv_p.conj()@Hs[a]@sv_p)) -
                         float(np.real(sv_m.conj()@Hs[a]@sv_m)))
            grads[k] += delta * dHdth
    theta -= lr * grads

fig, ax = plt.subplots(figsize=(8, 4.5))
ax.plot(mse_history, 'b-o', markersize=3)
ax.set_xlabel('Training step'); ax.set_ylabel('MSE vs target Q-values')
ax.set_title('Chapter 13: Quantum Q-Table Convergence')
ax.grid(True, alpha=0.3)
out = codes_dir / 'ch13_qtable_convergence.png'
fig.savefig(out, dpi=160, bbox_inches='tight'); plt.close(fig)
print(f"Saved figure to: {out}")
print(f"Initial MSE: {mse_history[0]:.4f}  Final MSE: {mse_history[-1]:.4f}")
