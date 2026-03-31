"""Ch-20 Project 3: Steane [[7,1,3]] code stabiliser syndrome table."""
import numpy as np
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator

# Steane code parity-check matrix (6x7)
# H = [H_x | H_z] where H_x = H_z = Steane H
H_s = np.array([
    [1,0,1,0,1,0,1],
    [0,1,1,0,0,1,1],
    [0,0,0,1,1,1,1],
], dtype=int)

# All single-qubit X errors and their syndromes
print("Steane [[7,1,3]] code — X-error syndrome table:")
print(f"{'Error':>12}  {'Syndrome (H_s @ e mod 2)':>28}")
print('-'*45)
# No error
e0 = np.zeros(7, dtype=int)
synd = (H_s @ e0) % 2
print(f"  {'no error':>10}  {synd.tolist()}")
for q in range(7):
    e = np.zeros(7, dtype=int); e[q] = 1
    synd = (H_s @ e) % 2
    dec  = int(''.join(map(str,synd)), 2)
    print(f"  {'X on q'+str(q):>10}  {synd.tolist()}  -> decimal {dec} -> corrects q{dec-1}")

print("\nEach single-qubit X error maps to a unique 3-bit syndrome -> perfect correction.")
