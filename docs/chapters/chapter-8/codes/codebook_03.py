"""Ch-8 Project 3: Data re-uploading variational classifier."""
import numpy as np
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector

def data_reupload_circuit(x, theta, n_layers=3):
    qc = QuantumCircuit(1)
    for l in range(n_layers):
        offset = l * 3
        qc.ry(x * theta[offset],     0)
        qc.rz(x * theta[offset+1],   0)
        qc.ry(theta[offset+2],        0)
    return qc

def predict(x, theta):
    qc = data_reupload_circuit(x, theta)
    sv = Statevector(qc).data
    return abs(sv[0])**2 - abs(sv[1])**2  # <Z>

# XOR-like dataset
X_train = np.array([-1.5, -0.5, 0.5, 1.5])
y_train = np.array([-1,    1,  -1,   1], dtype=float)

np.random.seed(7)
theta = np.random.uniform(0, 1, 9)
lr = 0.05

for step in range(100):
    loss = sum((predict(x, theta) - y)**2 for x, y in zip(X_train, y_train)) / len(X_train)
    grads = np.zeros_like(theta)
    for k in range(len(theta)):
        tp,tm = theta.copy(), theta.copy()
        tp[k] += np.pi/2; tm[k] -= np.pi/2
        grads[k] = sum((predict(x,tp)-y)**2-(predict(x,tm)-y)**2
                       for x,y in zip(X_train,y_train)) / len(X_train) * 0.5
    theta -= lr * grads
    if step % 20 == 0:
        acc = sum((predict(x,theta)*y > 0) for x,y in zip(X_train,y_train)) / len(X_train)
        print(f"  step={step:3d}  loss={loss:.4f}  acc={acc:.2f}")
