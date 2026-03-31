"""Ch-4 Project 3: Grover search algorithm."""
import numpy as np
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator

sim = AerSimulator()

def grover(n, target, n_iter=1):
    qc = QuantumCircuit(n)
    qc.h(range(n))
    for _ in range(n_iter):
        bits = format(target, f'0{n}b')
        for i, b in enumerate(reversed(bits)):
            if b == '0': qc.x(i)
        qc.h(n-1); qc.mcx(list(range(n-1)), n-1); qc.h(n-1)
        for i, b in enumerate(reversed(bits)):
            if b == '0': qc.x(i)
        qc.h(range(n)); qc.x(range(n))
        qc.h(n-1); qc.mcx(list(range(n-1)), n-1); qc.h(n-1)
        qc.x(range(n)); qc.h(range(n))
    qc.measure_all(); return qc

print(f"{'n':>4}  {'target':>8}  {'top_outcome':>12}  {'prob':>8}  {'correct?':>10}")
for n, target in [(3, 5), (3, 2), (4, 11)]:
    n_iter = max(1, int(np.floor(np.pi/4*np.sqrt(2**n))))
    qc = grover(n, target, n_iter)
    tc = transpile(qc, sim, optimization_level=1)
    counts = sim.run(tc, shots=2048).result().get_counts()
    top = max(counts, key=counts.get)
    prob = counts[top]/2048
    correct = int(top, 2) == target
    print(f"  {n:2d}  {target:8d}  {top:>12s}  {prob:8.4f}  {'YES' if correct else 'NO':>10}")
