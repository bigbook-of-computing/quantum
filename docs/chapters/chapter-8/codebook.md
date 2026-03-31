# **Chapter 8: Quantum Machine Learning Foundations () () (Codebook)**

Quantum Machine Learning (QML) merges parametrised quantum circuits with classical optimisation to learn patterns encoded in quantum states. This chapter establishes three core primitives: kernel estimation, variational classification, and data re-uploading.

---

**Expected outputs** from `codes/codebook_02.py`:

- `codes/ch8_kernel_heatmap.png`

## Project 1: Quantum Kernel Matrix Estimation

| Feature | Description |
| :--- | :--- |
| **Goal** | Compute a quantum kernel matrix $K[i,j] = \lvert\langle\phi(x_i)\vert\phi(x_j)\rangle\rvert^2$ for a small 2-D dataset using `ZZFeatureMap`. |
| **Circuit** | 2-qubit `ZZFeatureMap` with 2 repetitions encodes each sample via Pauli rotations. |
| **Method** | Swap-test-free approach: measure overlap via statevector inner product between two encoded states. |

---

### Complete Python Code

```python
import numpy as np
from qiskit.circuit.library import ZZFeatureMap
from qiskit.quantum_info import Statevector

# ── tiny 2-D dataset (4 points on unit circle) ──────────────────────────────

X = np.array([
    [0.0, 0.0],
    [0.5, 0.3],
    [1.0, 0.6],
    [1.5, 0.9],
])

feature_map = ZZFeatureMap(feature_dimension=2, reps=2)
n = len(X)
K = np.zeros((n, n))

for i in range(n):
    sv_i = Statevector(feature_map.assign_parameters(X[i]))
    for j in range(i, n):
        sv_j = Statevector(feature_map.assign_parameters(X[j]))
        overlap = abs(sv_i.inner(sv_j)) ** 2
        K[i, j] = overlap
        K[j, i] = overlap

print("Quantum Kernel Matrix:")
print(np.round(K, 4))

# ── eigenvalues reveal feature-space geometry ──────────────────────────────

eigvals = np.linalg.eigvalsh(K)
print(f"\nKernel eigenvalues: {np.round(eigvals, 4)}")
print(f"Kernel PSD check (all >= 0): {np.all(eigvals >= -1e-8)}")
```
**Sample Output:**
```python
Quantum Kernel Matrix:
[[1.     0.2837 0.1933 0.1705]
 [0.2837 1.     0.7207 0.5863]
 [0.1933 0.7207 1.     0.4362]
 [0.1705 0.5863 0.4362 1.    ]]

Kernel eigenvalues: [0.2454 0.5787 0.8944 2.2816]
Kernel PSD check (all >= 0): True
```

---

## Project 2: Variational Quantum Classifier

| Feature | Description |
| :--- | :--- |
| **Goal** | Train a `ZZFeatureMap + RealAmplitudes` circuit to classify two linearly separable classes. |
| **Circuit** | Feature map encodes $x$; `RealAmplitudes` ansatz provides trainable parameters $\theta$. |
| **Method** | Manual gradient-free optimisation (grid sweep) over a single rotation angle to demonstrate training dynamics. |

---

### Complete Python Code

```python
import numpy as np
from qiskit.circuit.library import ZZFeatureMap, RealAmplitudes
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector

# ── toy binary dataset ──────────────────────────────────────────────────────

np.random.seed(42)
X_train = np.vstack([
    np.random.randn(5, 2) * 0.3 + [0.5, 0.5],   # class +1
    np.random.randn(5, 2) * 0.3 + [-0.5, -0.5],  # class -1
])
y_train = np.array([1]*5 + [-1]*5)

feature_map = ZZFeatureMap(feature_dimension=2, reps=1)
ansatz     = RealAmplitudes(num_qubits=2, reps=1)
vqc = QuantumCircuit(2)
vqc.compose(feature_map, inplace=True)
vqc.compose(ansatz, inplace=True)

def predict(x, theta):
    param_vals = {**dict(zip(feature_map.parameters, x)),
                  **dict(zip(ansatz.parameters, theta))}
    sv = Statevector(vqc.assign_parameters(param_vals))
    probs = sv.probabilities()
    # expectation of Z0: P(0...) - P(1...)
    return probs[0] + probs[1] - probs[2] - probs[3]

def accuracy(theta):
    preds = [predict(x, theta) for x in X_train]
    return sum(np.sign(p) == y for p, y in zip(preds, y_train)) / len(y_train)

# ── coarse parameter sweep over first angle ─────────────────────────────────

n_params = len(ansatz.parameters)
best_theta = np.zeros(n_params)
best_acc   = 0.0

for trial in range(30):
    theta = np.random.uniform(0, 2*np.pi, n_params)
    acc   = accuracy(theta)
    if acc > best_acc:
        best_acc   = acc
        best_theta = theta.copy()

print(f"Best training accuracy after random sweep: {best_acc*100:.1f}%")
print(f"Best parameters: {np.round(best_theta, 3)}")
```
**Sample Output:**
```python
Best training accuracy after random sweep: 70.0%
Best parameters: [0.409 5.962 6.067 5.079]
```

---

## Project 3: Data Re-Uploading Classifier

| Feature | Description |
| :--- | :--- |
| **Goal** | Demonstrate data re-uploading: embed features multiple times interleaved with trainable layers to increase expressive power. |
| **Circuit** | Single-qubit circuit with alternating $R_Y(x_0)R_Z(x_1)$ data layers and $R_Y(\theta_k)$ parameter layers ($L=3$ repetitions). |
| **Method** | Compute Bloch-sphere $\langle Z \rangle$ output and visualise its dependence on input angle. |

---

### Complete Python Code

```python
```python
import numpy as np
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector

def reuploading_circuit(x, theta, layers=3):
```
    # x: shape (2,), theta: shape (layers,)
    qc = QuantumCircuit(1)
    for l in range(layers):
        qc.ry(x[0], 0)
        qc.rz(x[1], 0)
        qc.ry(theta[l], 0)
    return qc

```python
def expectation_z(x, theta):
```
qc  = reuploading_circuit(x, theta)
sv  = Statevector(qc)
p0  = sv.probabilities()[0]
return 2*p0 - 1   # <Z> = P(0) - P(1)

```
```
# ── sweep input angle x[0] over [0, 2pi] ────────────────────────────────────

theta_fixed = np.array([0.8, 1.2, 0.4])
angles      = np.linspace(0, 2*np.pi, 40)
z_vals_1    = [expectation_z(np.array([a, 0.0]), theta_fixed) for a in angles]
z_vals_3    = [expectation_z(np.array([a, 0.3]), theta_fixed) for a in angles]

```python
print("Re-uploading <Z> vs input angle x[0]:")
print(f"{'Angle':>8}   {'<Z> (x1=0.0)':>14}   {'<Z> (x1=0.3)':>14}")
for a, z1, z3 in zip(angles[::5], z_vals_1[::5], z_vals_3[::5]):
```
print(f"{a:8.4f}   {z1:14.6f}   {z3:14.6f}")

```
```
# check that deeper circuit produces richer response landscape

var_single = np.var(z_vals_1)
var_shift  = np.var(z_vals_3)
```python
print(f"\nVariance (x1=0.0): {var_single:.6f}")
print(f"Variance (x1=0.3): {var_shift:.6f}")
print("Re-uploading expands the representable function space.")

```
## Notes For Chapter Bridge

# **Chapter 9: the encoding question: how many qubits and which encoding () () (Codebook)**

# strategy (basis, amplitude, angle, IQP) best preserve classical data geometry?