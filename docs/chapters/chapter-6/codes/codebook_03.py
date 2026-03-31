"""Ch-6 Project 3: QAOA MaxCut on 4-node graph."""
import numpy as np
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator

edges = [(0,1),(1,2),(2,3),(0,3)]
n_qubits = 4
sim = AerSimulator()

def build_qaoa(gamma, beta):
    qc = QuantumCircuit(n_qubits); qc.h(range(n_qubits))
    for i,j in edges: qc.cx(i,j); qc.rz(2*gamma,j); qc.cx(i,j)
    for q in range(n_qubits): qc.rx(2*beta, q)
    qc.measure_all(); return qc

best_cut, best_params = 0, (0,0)
for g in np.linspace(0.1, np.pi, 6):
    for b in np.linspace(0.1, np.pi, 6):
        qc = build_qaoa(g, b)
        tc = transpile(qc, sim, optimization_level=1)
        counts = sim.run(tc, shots=2048).result().get_counts()
        cut = sum(sum(bits[i]!=bits[j] for i,j in edges)*c for bits,c in counts.items()) / 2048
        if cut > best_cut: best_cut = cut; best_params = (g,b)

print(f"MaxCut 4-node graph: best avg cut={best_cut:.3f}  params gamma={best_params[0]:.3f} beta={best_params[1]:.3f}")
qc = build_qaoa(*best_params)
tc = transpile(qc, sim, optimization_level=1)
counts = sim.run(tc, shots=4096).result().get_counts()
print("Top-5 bitstrings:")
for bits,cnt in sorted(counts.items(),key=lambda x:-x[1])[:5]:
    cut = sum(bits[i]!=bits[j] for i,j in edges)
    print(f"  |{bits}>  count={cnt}  cut={cut}")
