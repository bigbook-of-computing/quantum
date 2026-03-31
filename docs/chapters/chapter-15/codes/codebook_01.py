"""Ch-15 Project 1: Parameter-shift rule — exact vs finite-difference verification."""
import numpy as np
from qiskit.circuit.library import RealAmplitudes
from qiskit.quantum_info import Statevector, SparsePauliOp

H      = SparsePauliOp.from_list([('Z',[0.6, 0.0]),('XX',0.4)]).to_matrix()
ansatz = RealAmplitudes(2, reps=2)
n_p    = ansatz.num_parameters

def energy(theta):
    sv = Statevector(ansatz.assign_parameters(theta)).data
    return float(np.real(sv.conj() @ H @ sv))

np.random.seed(77)
theta0 = np.random.uniform(0, 2*np.pi, n_p)
eps    = 1e-6

print(f"{'idx':>4}  {'PS gradient':>14}  {'FD gradient':>14}  {'|diff|':>12}")
for k in range(n_p):
    tp, tm = theta0.copy(), theta0.copy()
    tp[k] += np.pi/2; tm[k] -= np.pi/2
    g_ps = 0.5*(energy(tp) - energy(tm))
    te, tf = theta0.copy(), theta0.copy()
    te[k] += eps; tf[k] -= eps
    g_fd = (energy(te) - energy(tf)) / (2*eps)
    print(f"  {k:2d}  {g_ps:14.8f}  {g_fd:14.8f}  {abs(g_ps-g_fd):12.2e}")
