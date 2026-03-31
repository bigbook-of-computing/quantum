"""Ch-10 Project 1: Hardware-efficient ansatz expressibility analysis."""
import numpy as np
from qiskit.circuit.library import RealAmplitudes, TwoLocal, EfficientSU2
from qiskit.quantum_info import Statevector, state_fidelity

np.random.seed(5)
ansatze = {
    'RealAmplitudes(r=1)': RealAmplitudes(2, reps=1),
    'RealAmplitudes(r=3)': RealAmplitudes(2, reps=3),
    'EfficientSU2(r=2)':   EfficientSU2(2, reps=2),
}

print(f"{'Ansatz':28}  {'n_params':>9}  {'avg_fid from |0>':>18}")
for name, ansatz in ansatze.items():
    n_p = ansatz.num_parameters
    fids = []
    for _ in range(50):
        th = np.random.uniform(0, 2*np.pi, n_p)
        sv = Statevector(ansatz.assign_parameters(th))
        fids.append(float(state_fidelity(sv, Statevector.from_label('0'*2))))
    print(f"  {name:28s}  {n_p:9d}  {np.mean(fids):18.6f}")
print("\nLower avg fidelity from |0> => higher expressibility (more uniform coverage).")
