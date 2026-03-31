"""Ch-8 Project 1: Quantum kernel matrix estimation."""
import numpy as np
from qiskit.circuit.library import ZZFeatureMap
from qiskit.quantum_info import Statevector

np.random.seed(42)
n_features, n_samples = 2, 6
X = np.random.uniform(-np.pi, np.pi, (n_samples, n_features))

fmap = ZZFeatureMap(n_features, reps=1)

def kernel_entry(x, y):
    fx = fmap.assign_parameters(x)
    fy = fmap.assign_parameters(y)
    sv_x = Statevector(fx); sv_y = Statevector(fy)
    return abs(sv_x.inner(sv_y))**2

K = np.array([[kernel_entry(X[i], X[j]) for j in range(n_samples)]
              for i in range(n_samples)])

print("ZZFeatureMap quantum kernel matrix (6x6):")
np.set_printoptions(precision=4, suppress=True)
print(K)
eigvals = np.linalg.eigvalsh(K)
print(f"\nKernel eigenvalues: {eigvals}")
print(f"Positive semi-definite: {all(eigvals >= -1e-8)}")
