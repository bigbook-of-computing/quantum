"""Ch-2 Project 3: Density matrix purity analysis."""
import numpy as np
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector, DensityMatrix

# Pure states
pure_states = {
    '|0>': [],  '|1>': ['x'], '|+>': ['h'],
    'GHZ': None  # special
}

def make_pure_dm(ops):
    qc = QuantumCircuit(1)
    for op in ops: getattr(qc, op)(0)
    return DensityMatrix(qc)

# GHZ 3-qubit
def ghz_dm():
    qc = QuantumCircuit(3); qc.h(0); qc.cx(0,1); qc.cx(0,2)
    return DensityMatrix(qc)

print(f"{'State':>8}  {'Purity Tr(rho^2)':>18}  {'Type':>8}")
for label, ops in pure_states.items():
    dm = make_pure_dm(ops) if ops is not None else ghz_dm()
    purity = float(np.real(np.trace(dm.data @ dm.data)))
    qubits = 1 if ops is not None else 3
    kind   = 'pure' if abs(purity - 1.0) < 0.01 else 'mixed'
    print(f"  {label:8s}  {purity:18.8f}  {kind:>8}")

# Mixed state: maximally mixed single qubit
rho_mix = np.eye(2) / 2
purity_mix = float(np.real(np.trace(rho_mix @ rho_mix)))
print(f"  {'I/2':8s}  {purity_mix:18.8f}  {'mixed':>8}")
print("\nPurity = 1 <=> pure state; Purity = 1/d <=> maximally mixed (d=dim).")
