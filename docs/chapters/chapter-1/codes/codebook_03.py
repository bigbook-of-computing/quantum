"""Ch-1 Project 3: Multi-state statevector survey."""
import numpy as np
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector

configs = [
    ('|0>',  lambda qc: None),
    ('|1>',  lambda qc: qc.x(0)),
    ('|+>',  lambda qc: qc.h(0)),
    ('|->',  lambda qc: (qc.h(0), qc.z(0))),
    ('|i>',  lambda qc: (qc.h(0), qc.s(0))),
    ('|R>',  lambda qc: qc.ry(np.pi/3, 0)),
]

print(f"{'State':>5}  {'|alpha|^2':>12}  {'|beta|^2':>12}  {'Re(alpha)':>12}  {'Im(alpha)':>12}")
for label, prep in configs:
    qc = QuantumCircuit(1)
    prep(qc)
    sv = Statevector(qc).data
    print(f"  {label:5s}  {abs(sv[0])**2:12.6f}  {abs(sv[1])**2:12.6f}"
          f"  {sv[0].real:12.6f}  {sv[0].imag:12.6f}")

print("\nAll states satisfy |alpha|^2 + |beta|^2 = 1 (Born normalisation).")
