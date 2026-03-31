"""Ch-17 Project 1: H2 molecule Jordan-Wigner Hamiltonian eigenvalues."""
import numpy as np
from qiskit.quantum_info import SparsePauliOp

# Minimal 2-qubit H2 STO-3G Hamiltonian (Jordan-Wigner, R=0.74 Å)
H_terms = [
    ('II', -1.0523732),
    ('ZI', +0.3979374),
    ('IZ', -0.3979374),
    ('ZZ', -0.0112801),
    ('XX', +0.1809270),
    ('YY', +0.1809270),
]
H = SparsePauliOp.from_list(H_terms)
H_mat = H.to_matrix().real
eigvals = np.linalg.eigvalsh(H_mat)
print("H2 Jordan-Wigner 2-qubit Hamiltonian eigenvalues (Ha):")
for i, e in enumerate(eigvals): print(f"  E{i} = {e:.8f} Ha")
print(f"\nGround state energy E0 = {eigvals[0]:.8f} Ha")
print(f"HOMO-LUMO gap          = {eigvals[1]-eigvals[0]:.8f} Ha")
