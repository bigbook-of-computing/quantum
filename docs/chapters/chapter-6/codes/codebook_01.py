"""Ch-6 Project 1: VQE for 1D Heisenberg model."""
import numpy as np
from qiskit.circuit.library import RealAmplitudes
from qiskit.quantum_info import Statevector, SparsePauliOp

H = SparsePauliOp.from_list([('XX',1.0),('YY',1.0),('ZZ',1.0)])
H_mat = H.to_matrix()
E_exact = np.linalg.eigvalsh(H_mat.real)[0]

ansatz = RealAmplitudes(2, reps=2)
n_par  = ansatz.num_parameters

def energy(theta):
    sv = Statevector(ansatz.assign_parameters(theta)).data
    return float(np.real(sv.conj() @ H_mat @ sv))

np.random.seed(0)
theta = np.random.uniform(0, 2*np.pi, n_par)
print(f"Heisenberg ZZ+XX+YY  Exact ground state: {E_exact:.6f}")
print(f"{'Step':>5}  {'VQE energy':>12}  {'Error':>10}")
for step in range(50):
    grads = np.zeros(n_par)
    for k in range(n_par):
        tp, tm = theta.copy(), theta.copy()
        tp[k] += np.pi/2; tm[k] -= np.pi/2
        grads[k] = 0.5*(energy(tp) - energy(tm))
    theta -= 0.2*grads
    if step % 10 == 0:
        e = energy(theta)
        print(f"  {step:3d}  {e:12.6f}  {abs(e-E_exact):10.6f}")
print(f"\nFinal VQE energy: {energy(theta):.6f}  (exact: {E_exact:.6f})")
