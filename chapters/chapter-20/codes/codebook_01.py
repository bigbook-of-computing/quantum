"""Ch-20 Project 1: 3-qubit bit-flip code — syndrome detection."""
import numpy as np
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
from qiskit_aer.noise import depolarizing_error, NoiseModel

sim = AerSimulator()

def bitflip_encode_detect(error_qubit=None, p_flip=0.0):
    qc = QuantumCircuit(5, 2)  # 3 data + 2 syndrome
    # Encode |0> -> |000>
    qc.cx(0,1); qc.cx(0,2)
    # Inject error
    if error_qubit is not None: qc.x(error_qubit)
    # Syndrome measurement
    qc.cx(0,3); qc.cx(1,3)  # s0 = q0 XOR q1
    qc.cx(1,4); qc.cx(2,4)  # s1 = q1 XOR q2
    qc.measure([3,4],[0,1])
    return qc

syndrome_table = {'00': 'no error', '10': 'q1 flip', '11': 'q1 flip (ambiguous)', '01': 'q2 flip'}

print("Bit-flip syndrome detection:")
print(f"{'error qubit':>12}  {'syndrome':>10}  {'detection':>20}")
for erq in [None, 0, 1, 2]:
    qc = bitflip_encode_detect(error_qubit=erq)
    tc = transpile(qc, sim, optimization_level=0)
    counts = sim.run(tc, shots=1024).result().get_counts()
    top = max(counts, key=counts.get)
    print(f"  {str(erq):10s}  {top:>10s}  {syndrome_table.get(top, 'unknown'):>20s}")
