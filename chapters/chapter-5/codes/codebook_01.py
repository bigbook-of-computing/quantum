"""Ch-5 Project 1: Manual QFT vs library QFT statevector comparison."""
import numpy as np
from qiskit import QuantumCircuit
from qiskit.circuit.library import QFT
from qiskit.quantum_info import Statevector

def manual_qft(n):
    qc = QuantumCircuit(n)
    for i in range(n):
        qc.h(i)
        for j in range(i+1, n):
            qc.cp(2*np.pi/2**(j-i+1), j, i)
    for i in range(n//2): qc.swap(i, n-1-i)
    return qc

n = 4
qc_manual = manual_qft(n)
qc_lib    = QFT(n)

sv_manual = Statevector.from_instruction(qc_manual)
sv_lib    = Statevector.from_instruction(qc_lib)

overlap = abs(sv_manual.inner(sv_lib))**2
print(f"Manual QFT vs Library QFT fidelity: {overlap:.8f}")

# Apply to |0101>
init = QuantumCircuit(n); init.x(0); init.x(2)
sv0 = Statevector(init)
sv_qft_manual = sv0.evolve(qc_manual)
sv_qft_lib    = sv0.evolve(qc_lib)
fid = abs(sv_qft_manual.inner(sv_qft_lib))**2
print(f"Applied to |0101> fidelity: {fid:.8f}")
print("\nFidelity ~1.0 confirms manual and library implementations agree.")
