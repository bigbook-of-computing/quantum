"""Ch-3 Project 1: Bell state generation and fidelity."""
import numpy as np
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
from qiskit.quantum_info import Statevector, state_fidelity

bell_names  = ['Phi+', 'Phi-', 'Psi+', 'Psi-']
bell_states = []
for name in bell_names:
    qc = QuantumCircuit(2); qc.h(0); qc.cx(0,1)
    if '-' in name: qc.z(0)
    if 'Psi' in name: qc.x(1)
    bell_states.append(Statevector(qc))

sim = AerSimulator()
print(f"{'Bell state':>8}  {'|00> prob':>10}  {'|11> prob':>10}  {'|01>+|10>':>12}")
for name, sv in zip(bell_names, bell_states):
    probs = sv.probabilities_dict()
    p00 = probs.get('00', 0); p11 = probs.get('11', 0)
    p_cross = probs.get('01', 0) + probs.get('10', 0)
    print(f"  {name:8s}  {p00:10.4f}  {p11:10.4f}  {p_cross:12.4f}")
