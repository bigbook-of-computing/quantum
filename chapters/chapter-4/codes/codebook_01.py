"""Ch-4 Project 1: Deutsch-Jozsa algorithm."""
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator

sim = AerSimulator()

def deutsch_jozsa(f_type, n=3):
    """f_type: 'constant_0','constant_1','balanced'"""
    qc = QuantumCircuit(n+1, n)
    qc.x(n); qc.h(range(n+1))
    if f_type == 'constant_1':
        qc.x(n)
    elif f_type == 'balanced':
        for i in range(n): qc.cx(i, n)
    qc.h(range(n))
    qc.measure(range(n), range(n))
    return qc

for f in ['constant_0', 'constant_1', 'balanced']:
    qc = deutsch_jozsa(f)
    tc = transpile(qc, sim, optimization_level=0)
    counts = sim.run(tc, shots=512).result().get_counts()
    top = max(counts, key=counts.get)
    kind = 'constant' if top == '0'*3 else 'balanced'
    print(f"  f={f:12s}  output={top}  detected={kind}")
