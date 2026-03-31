"""Ch-5 Project 3: Quantum Phase Estimation."""
import numpy as np
from qiskit import QuantumCircuit, transpile
from qiskit.circuit.library import QFT
from qiskit_aer import AerSimulator

sim = AerSimulator()

def qpe_circuit(phase, n_ancilla=4):
    n = n_ancilla + 1  # +1 eigenstate qubit
    qc = QuantumCircuit(n, n_ancilla)
    qc.h(range(n_ancilla))
    qc.x(n_ancilla)  # eigenstate |1> of U=Phase(2pi*phi)
    for j in range(n_ancilla):
        reps = 2**j
        for _ in range(reps):
            qc.cp(2*np.pi*phase, j, n_ancilla)
    qc.compose(QFT(n_ancilla, inverse=True), qubits=range(n_ancilla), inplace=True)
    qc.measure(range(n_ancilla), range(n_ancilla))
    return qc

print(f"{'True phase':>12}  {'Estimated':>12}  {'Error':>10}")
for phi in [0.25, 0.125, 0.375, 0.5]:
    qc = qpe_circuit(phi)
    tc = transpile(qc, sim, optimization_level=0)
    counts = sim.run(tc, shots=2048).result().get_counts()
    top = max(counts, key=counts.get)
    estimated = int(top, 2) / 2**4
    print(f"  {phi:12.4f}  {estimated:12.4f}  {abs(phi-estimated):10.6f}")
