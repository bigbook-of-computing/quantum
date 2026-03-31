"""Ch-3 Project 3: Circuit depth vs qubit count analysis."""
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator

sim = AerSimulator()
print(f"{'n_qubits':>10}  {'Depth (ideal)':>14}  {'Depth (transpile)':>18}  {'CX count':>10}")
for n in range(2, 9):
    qc = QuantumCircuit(n)
    qc.h(range(n))
    for i in range(n-1): qc.cx(i, i+1)
    for i in range(n-1, 0, -1): qc.cx(i-1, i)
    qc.measure_all()
    tc = transpile(qc, sim, optimization_level=3)
    ops = dict(tc.count_ops())
    print(f"  {n:8d}  {qc.depth():14d}  {tc.depth():18d}  {ops.get('cx',0):10d}")
