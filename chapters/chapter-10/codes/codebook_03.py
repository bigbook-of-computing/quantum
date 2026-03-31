"""Ch-10 Project 3: Expressibility scan across depths."""
import numpy as np
from qiskit.circuit.library import EfficientSU2
from qiskit.quantum_info import Statevector, state_fidelity

np.random.seed(1)
print(f"{'reps':>6}  {'n_params':>9}  {'expr_score(1-avg_fid)':>23}")
for reps in range(1, 6):
    ansatz = EfficientSU2(2, reps=reps)
    n_p = ansatz.num_parameters
    fids = []
    for _ in range(200):
        th = np.random.uniform(0, 2*np.pi, n_p)
        sv = Statevector(ansatz.assign_parameters(th))
        fids.append(float(state_fidelity(sv, Statevector.from_label('00'))))
    score = 1 - np.mean(fids)
    print(f"  {reps:4d}  {n_p:9d}  {score:23.6f}")
print("\nHigher expressibility score => ansatz explores more of Hilbert space.")
