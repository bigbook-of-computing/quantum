"""Ch-2 Project 1: Pauli expectation values on canonical states."""
import numpy as np
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector, SparsePauliOp

paulis = {'X': SparsePauliOp('X').to_matrix(),
          'Y': SparsePauliOp('Y').to_matrix(),
          'Z': SparsePauliOp('Z').to_matrix()}

states = {
    '|0>':  QuantumCircuit(1),
    '|1>':  (lambda: (QuantumCircuit(1).__setattr__('_', None) or QuantumCircuit(1).x(0), QuantumCircuit(1))[1])(),
    '|+>':  (lambda qc: (qc.h(0), qc)[1])(QuantumCircuit(1)),
    '|->':  (lambda qc: (qc.h(0), qc.z(0), qc)[2])(QuantumCircuit(1)),
}

# Cleaner approach
def make_state(ops):
    qc = QuantumCircuit(1)
    for op in ops: getattr(qc, op)(0)
    return Statevector(qc).data

state_vecs = {
    '|0>': make_state([]),
    '|1>': make_state(['x']),
    '|+>': make_state(['h']),
    '|->': make_state(['h', 'z']),
    '|i>': make_state(['h', 's']),
}

print(f"{'State':>5}", end='')
for p in paulis: print(f"  <{p}>       ", end='')
print()
for label, sv in state_vecs.items():
    print(f"  {label}", end='')
    for pmat in paulis.values():
        exp = float(np.real(sv.conj() @ pmat @ sv))
        print(f"  {exp:10.6f}", end='')
    print()
