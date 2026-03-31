"""Ch-12 Project 1: Quantum-inspired PCA via SWAP test."""
import numpy as np
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
from qiskit.quantum_info import Statevector

np.random.seed(1)
n_q = 3  # 3-dim data
data = np.random.randn(20, n_q)
cov  = np.cov(data.T)
eigvals, eigvecs = np.linalg.eigh(cov)
explained = eigvals[::-1] / eigvals.sum()
print("Classical PCA explained variance (descending):")
for i, ev in enumerate(explained[::-1]): print(f"  PC{i+1}: {ev:.4f}")

# SWAP test for overlap between two normalised vectors
def swap_test_fidelity(sv_a, sv_b):
    n = len(sv_a.data).bit_length() - 1
    # Use inner product
    return abs(sv_a.inner(sv_b))**2

# Measure overlap of data projected onto top eigenvectors
top2  = eigvecs[:, -2:]
projs = data @ top2
projs_n = projs / np.linalg.norm(projs, axis=1, keepdims=True)
print(f"\nData projected onto top-2 eigenvectors: {projs_n.shape}")
print(f"Avg cosine-similarity in projection: {np.mean(np.abs(projs_n @ projs_n.T)):.4f}")
