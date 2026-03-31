"""Ch-17 Project 3: VQE for H2 ground state energy."""
import numpy as np
from qiskit.circuit.library import RealAmplitudes
from qiskit.quantum_info import Statevector, SparsePauliOp

H_terms = [('II',-1.0523732),('ZI',+0.3979374),('IZ',-0.3979374),
           ('ZZ',-0.0112801),('XX',+0.1809270),('YY',+0.1809270)]
H     = SparsePauliOp.from_list(H_terms)
H_mat = H.to_matrix().real
E_exact = np.linalg.eigvalsh(H_mat)[0]

ansatz = RealAmplitudes(2, reps=2)
n_p    = ansatz.num_parameters

def energy(theta):
    sv = Statevector(ansatz.assign_parameters(theta)).data
    return float(np.real(sv.conj() @ H_mat @ sv))

np.random.seed(42)
theta = np.random.uniform(0, 2*np.pi, n_p); lr = 0.15
print(f"H2 VQE — exact ground state: {E_exact:.8f} Ha")
print(f"{'step':>5}  {'energy (Ha)':>14}  {'error (Ha)':>12}")
for step in range(80):
    grads = np.zeros(n_p)
    for k in range(n_p):
        tp, tm = theta.copy(), theta.copy()
        tp[k] += np.pi/2; tm[k] -= np.pi/2
        grads[k] = 0.5*(energy(tp) - energy(tm))
    theta -= lr * grads
    if step % 16 == 0:
        e = energy(theta)
        print(f"  {step:3d}  {e:14.8f}  {abs(e-E_exact):12.2e}")
print(f"\nFinal: {energy(theta):.8f} Ha  error={abs(energy(theta)-E_exact):.2e}")
