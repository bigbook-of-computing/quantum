"""Ch-9 Project 1: Encoding strategies — angle, amplitude, basis comparison."""
import numpy as np
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector

x = np.array([0.3, 0.7])

# Angle encoding
qc_angle = QuantumCircuit(2)
for i, xi in enumerate(x): qc_angle.ry(xi, i)
sv_angle = Statevector(qc_angle)

# Amplitude encoding
x_norm = x / np.linalg.norm(x)
qc_amp = QuantumCircuit(1)
qc_amp.initialize(x_norm, 0)
sv_amp = Statevector(qc_amp)

# Basis encoding (threshold)
bits = ''.join('1' if xi > 0.5 else '0' for xi in x)
qc_basis = QuantumCircuit(2)
for i, b in enumerate(bits):
    if b == '1': qc_basis.x(i)
sv_basis = Statevector(qc_basis)

print("Encoding comparison for x = [0.3, 0.7]:")
print(f"  Angle encoding   statevector: {np.round(sv_angle.data, 4)}")
print(f"  Amplitude enc.   statevector: {np.round(sv_amp.data, 4)}")
print(f"  Basis encoding   bitstring: |{bits}>  statevector: {np.round(sv_basis.data, 4)}")
