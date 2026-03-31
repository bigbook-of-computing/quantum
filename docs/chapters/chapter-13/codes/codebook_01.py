"""Ch-13 Project 1: Variational quantum policy gradient."""
import numpy as np
from qiskit.circuit.library import RealAmplitudes
from qiskit.quantum_info import Statevector, SparsePauliOp

np.random.seed(2)
n_q = 2
ansatz = RealAmplitudes(n_q, reps=2)
n_p    = ansatz.num_parameters

H_reward = SparsePauliOp('ZZ').to_matrix()  # reward = <ZZ>

def policy_score(theta):
    sv = Statevector(ansatz.assign_parameters(theta)).data
    return float(np.real(sv.conj() @ H_reward @ sv))

theta = np.random.uniform(0, 2*np.pi, n_p); lr=0.15
print(f"{'step':>5}  {'reward':>10}")
for step in range(50):
    grads = np.zeros(n_p)
    for k in range(n_p):
        tp,tm = theta.copy(), theta.copy(); tp[k]+=np.pi/2; tm[k]-=np.pi/2
        grads[k] = 0.5*(policy_score(tp)-policy_score(tm))
    theta += lr*grads  # gradient ASCENT for reward
    if step % 10 == 0:
        print(f"  {step:3d}  {policy_score(theta):10.6f}")
print(f"\nFinal reward: {policy_score(theta):.6f}  (max possible: 1.0)")
