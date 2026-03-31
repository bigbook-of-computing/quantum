"""Ch-14 Project 3: Grover Adaptive Search (GAS) for MaxCut."""
import numpy as np
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator

edges = [(0,1),(1,2),(2,3),(0,3)]
n_q   = 4
sim   = AerSimulator()

def cut(bits): return sum(bits[i]!=bits[j] for i,j in edges)

# Grover oracle: marks all bitstrings with cut value >= threshold
def grover_oracle(threshold):
    qc = QuantumCircuit(n_q)
    # Multi-controlled Z on bitstrings meeting cut requirement (mark by phase flip)
    from itertools import product
    marked = [b for b in product([0,1],repeat=n_q) if cut(b)>=threshold]
    for bits in marked:
        for i,b in enumerate(bits):
            if b==0: qc.x(i)
        qc.h(n_q-1)
        qc.mcx(list(range(n_q-1)), n_q-1)
        qc.h(n_q-1)
        for i,b in enumerate(bits):
            if b==0: qc.x(i)
    return qc

# One iteration of Grover with threshold=3
qc = QuantumCircuit(n_q)
qc.h(range(n_q))
qc.compose(grover_oracle(3), inplace=True)
# Diffuser
qc.h(range(n_q)); qc.x(range(n_q))
qc.h(n_q-1); qc.mcx(list(range(n_q-1)), n_q-1); qc.h(n_q-1)
qc.x(range(n_q)); qc.h(range(n_q))
qc.measure_all()

tc = transpile(qc, sim, optimization_level=1)
counts = sim.run(tc, shots=2048).result().get_counts()
total_high_cut = sum(c for b,c in counts.items() if cut(b)>=3) / 2048
print(f"Grover Adaptive Search (threshold=3):")
print(f"  P(cut>=3): {total_high_cut:.4f}")
print("\nTop outcomes:")
for b,c in sorted(counts.items(),key=lambda x:-x[1])[:5]:
    print(f"  |{b}>  cut={cut(b)}  prob={c/2048:.4f}")
