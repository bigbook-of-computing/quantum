"""Ch-11 Project 3: Quantum kernel SVM (simulation)."""
import numpy as np
from qiskit.circuit.library import ZZFeatureMap
from qiskit.quantum_info import Statevector

np.random.seed(0)
n_q = 2; n_pts = 8
X = np.random.uniform(-np.pi, np.pi, (n_pts, n_q))
y = np.sign(X[:,0] * X[:,1])  # XOR-like labels

fmap = ZZFeatureMap(n_q, reps=1)

def k(x, z):
    sx = Statevector(fmap.assign_parameters(x))
    sz = Statevector(fmap.assign_parameters(z))
    return abs(sx.inner(sz))**2

K = np.array([[k(X[i],X[j]) for j in range(n_pts)] for i in range(n_pts)])
K_eps = K + 0.01*np.eye(n_pts)  # regularise

# Kernel Perceptron (simplified)
alpha = np.zeros(n_pts); b = 0.0
print("Kernel Perceptron training (quantum kernel SVM):")
for epoch in range(10):
    mistakes = 0
    for i in range(n_pts):
        score = sum(alpha[j]*y[j]*K[i,j] for j in range(n_pts)) + b
        if y[i]*score <= 0:
            alpha[i] += 1; b += y[i]; mistakes += 1
    acc = sum((sum(alpha[j]*y[j]*K[i,j] for j in range(n_pts))+b)*y[i]>0
              for i in range(n_pts)) / n_pts
    if epoch % 2 == 0:
        print(f"  epoch={epoch}  mistakes={mistakes}  train_acc={acc:.2f}")
