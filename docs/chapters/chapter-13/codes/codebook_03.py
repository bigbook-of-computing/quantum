"""Ch-13 Project 3: Action-selection reward landscape."""
import numpy as np
from qiskit.circuit.library import RealAmplitudes
from qiskit.quantum_info import Statevector, SparsePauliOp

np.random.seed(9)
n_q    = 2
ansatz = RealAmplitudes(n_q, reps=1)
n_p    = ansatz.num_parameters

H_reward = SparsePauliOp.from_list([('ZI',0.5),('ZZ',0.5)]).to_matrix()

N = 20
t0 = np.linspace(0, 2*np.pi, N); t1 = np.linspace(0, 2*np.pi, N)
base = np.random.uniform(0, 2*np.pi, n_p)
print("Reward landscape (θ₀ vs θ₁ slice):")
print("  θ₀\θ₁  ", '  '.join(f'{t:.2f}' for t in t1[:5]), '...')
for i, a0 in enumerate(t0[:5]):
    row = [f'{a0:.2f} |']
    for j, a1 in enumerate(t1[:5]):
        th = base.copy(); th[0]=a0; th[1]=a1
        sv = Statevector(ansatz.assign_parameters(th)).data
        r  = float(np.real(sv.conj() @ H_reward @ sv))
        row.append(f'{r:+.3f}')
    print('  '.join(row))
print("  ...")
