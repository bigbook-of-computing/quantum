"""Ch-7 Project 1: Multi-level transpilation comparison."""
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator

sim = AerSimulator()
qc = QuantumCircuit(4)
qc.h(range(4))
for i in range(3): qc.cx(i, i+1)
qc.rx(0.5, 0); qc.ry(0.7, 1)
for i in range(2, -1, -1): qc.cx(i, i+1)
qc.measure_all()

print(f"Original: depth={qc.depth()}  gates={dict(qc.count_ops())}")
print()
print(f"{'opt  ':>5}  {'depth':>7}  {'cx':>5}  {'1q':>5}")
for opt in range(4):
    tc = transpile(qc, sim, basis_gates=['cx','u3'], optimization_level=opt)
    ops = dict(tc.count_ops())
    print(f"  {opt:3d}  {tc.depth():7d}  {ops.get('cx',0):5d}  {ops.get('u3',0):5d}")
