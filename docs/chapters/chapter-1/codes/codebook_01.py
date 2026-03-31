"""Ch-1 Project 1: Superposition measurement statistics."""
import numpy as np
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator

sim = AerSimulator()
results = {}
for n_qubits in [1, 2, 3]:
    qc = QuantumCircuit(n_qubits)
    qc.h(range(n_qubits))
    qc.measure_all()
    tc = transpile(qc, sim, optimization_level=0)
    counts = sim.run(tc, shots=4096).result().get_counts()
    n_outcomes = len(counts)
    probs = {k: v/4096 for k, v in counts.items()}
    max_p = max(probs.values())
    min_p = min(probs.values())
    results[n_qubits] = (n_outcomes, max_p, min_p)
    print(f"{n_qubits} qubit(s): {n_outcomes} outcomes  max_p={max_p:.4f}  min_p={min_p:.4f}")

print("\nAll outcomes have probability ~1/2^n as expected from uniform superposition.")
