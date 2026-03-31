"""Ch-15 Project 3: Adam optimiser sweep for quantum circuit training."""
import numpy as np
from qiskit.circuit.library import RealAmplitudes
from qiskit.quantum_info import Statevector, SparsePauliOp

H      = SparsePauliOp.from_list([('ZZ',1.0),('Z',[0.5,0.0])]).to_matrix()
ansatz = RealAmplitudes(2, reps=2)
n_p    = ansatz.num_parameters
E_exact = np.linalg.eigvalsh(H)[0]

def energy(theta):
    sv = Statevector(ansatz.assign_parameters(theta)).data
    return float(np.real(sv.conj() @ H @ sv))

def ps_grad(theta):
    g = np.zeros(n_p)
    for k in range(n_p):
        tp,tm = theta.copy(), theta.copy(); tp[k]+=np.pi/2; tm[k]-=np.pi/2
        g[k] = 0.5*(energy(tp)-energy(tm))
    return g

def adam(lr):
    np.random.seed(1)
    theta = np.random.uniform(0, 2*np.pi, n_p)
    m = np.zeros(n_p); v = np.zeros(n_p); beta1=0.9; beta2=0.999; eps=1e-8
    best = energy(theta)
    for t in range(1, 81):
        g = ps_grad(theta)
        m = beta1*m + (1-beta1)*g; v = beta2*v + (1-beta2)*g**2
        mc = m/(1-beta1**t); vc = v/(1-beta2**t)
        theta -= lr * mc / (np.sqrt(vc)+eps)
        best = min(best, energy(theta))
    return best

print(f"{'lr':>8}  {'best energy':>14}  {'error vs exact':>16}")
for lr in [0.01, 0.05, 0.1, 0.2, 0.5]:
    best = adam(lr)
    print(f"  {lr:6.3f}  {best:14.8f}  {abs(best-E_exact):16.2e}")
