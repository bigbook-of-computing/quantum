# **Chapter 11: Quantum Supervised Learning () () (Codebook)**

Supervised quantum learning trains a parametric circuit to minimise a classification or regression loss. This chapter implements a variational binary classifier, a quantum kernel SVM, and a loss-landscape diagnostic.

---

**Expected outputs** from `codes/codebook_02.py`:

- `codes/ch11_loss_landscape.png`

## Project 1: Variational Binary Classifier on Iris (2-class)

| Feature | Description |
| :--- | :--- |
| **Goal** | Train a 2-qubit `ZZFeatureMap + RealAmplitudes` circuit to distinguish setosa from versicolor in the Iris dataset (2 features). |
| **Method** | Manual gradient-free optimisation loop using the parameter-shift rule and binary cross-entropy loss. |
| **Data** | First 2 principal Iris features, 20 training / 10 test points, labels $\{+1, -1\}$. |

---

### Complete Python Code

```python
import numpy as np
from qiskit.circuit.library import ZZFeatureMap, RealAmplitudes
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector, SparsePauliOp

# ── tiny Iris subset (sepal length / width, 2 classes) ──────────────────────
np.random.seed(7)
# class 0 (setosa-like): centred at (0.3, 0.3), class 1: at (-0.3, -0.3)
X = np.vstack([np.random.randn(15, 2)*0.2 + [0.3,  0.3],
               np.random.randn(15, 2)*0.2 + [-0.3, -0.3]])
y = np.array([1]*15 + [-1]*15, dtype=float)

X_tr, y_tr = X[:20], y[:20]
X_te, y_te = X[20:], y[20:]

fmap   = ZZFeatureMap(feature_dimension=2, reps=1)
ansatz = RealAmplitudes(num_qubits=2, reps=1)
vqc    = QuantumCircuit(2)
vqc.compose(fmap, inplace=True)
vqc.compose(ansatz, inplace=True)

obs_mat = SparsePauliOp.from_list([("ZI", 1.0)]).to_matrix()

def predict_raw(x, theta):
    pvals = {**dict(zip(fmap.parameters, x)),
             **dict(zip(ansatz.parameters, theta))}
    sv = Statevector(vqc.assign_parameters(pvals)).data
    return float(np.real(sv.conj() @ obs_mat @ sv))

def loss_fn(theta):
    raw = np.array([predict_raw(x, theta) for x in X_tr])
    return np.mean((raw - y_tr)**2)  # MSE

def ps_gradient(theta):
    g = np.zeros(len(theta))
    for k in range(len(theta)):
        tp, tm = theta.copy(), theta.copy()
        tp[k] += np.pi/2;  tm[k] -= np.pi/2
        g[k] = 0.5*(loss_fn(tp) - loss_fn(tm))
    return g

theta = np.random.uniform(0, 2*np.pi, len(ansatz.parameters))
lr    = 0.15
for epoch in range(25):
    g     = ps_gradient(theta)
    theta -= lr * g
    if epoch % 5 == 0:
        print(f"Epoch {epoch:3d}  loss={loss_fn(theta):.5f}")

preds_te = [np.sign(predict_raw(x, theta)) for x in X_te]
acc = np.mean(np.array(preds_te) == y_te)
print(f"\nTest accuracy: {acc*100:.1f}%")
```
**Sample Output:**
```
Epoch   0  loss=0.86184
Epoch   5  loss=0.77771
Epoch  10  loss=0.71505
Epoch  15  loss=0.67598
Epoch  20  loss=0.65388

Test accuracy: 0.0%
```

---

## Project 2: Quantum Kernel SVM

| Feature | Description |
| :--- | :--- |
| **Goal** | Use the quantum kernel matrix from `ZZFeatureMap` as input to a classical SVM (hard-coded kernel matrix) and evaluate test accuracy. |
| **Data** | Same 2-class 2-feature dataset as Project 1. |
| **Method** | Build full kernel matrix analytically via statevector inner products; feed to a simple soft-margin linear separator. |

---

### Complete Python Code

```python
import numpy as np
from qiskit.circuit.library import ZZFeatureMap
from qiskit.quantum_info import Statevector

np.random.seed(7)
X = np.vstack([np.random.randn(15, 2)*0.2 + [0.3,  0.3],
               np.random.randn(15, 2)*0.2 + [-0.3, -0.3]])
y = np.array([1.0]*15 + [-1.0]*15)

X_tr, y_tr = X[:24], y[:24]
X_te, y_te = X[24:], y[24:]

fmap = ZZFeatureMap(feature_dimension=2, reps=2)

def q_kernel(a, b):
    sv_a = Statevector(fmap.assign_parameters(a))
    sv_b = Statevector(fmap.assign_parameters(b))
    return abs(sv_a.inner(sv_b))**2

# ── build train/test kernel matrices ─────────────────────────────────────────
n_tr = len(X_tr)
K_tr = np.zeros((n_tr, n_tr))
for i in range(n_tr):
    for j in range(i, n_tr):
        k = q_kernel(X_tr[i], X_tr[j])
        K_tr[i, j] = K_tr[j, i] = k

K_te = np.array([[q_kernel(X_te[i], X_tr[j]) for j in range(n_tr)]
                 for i in range(len(X_te))])

# ── naive 1-NN classifier using kernel distance: d^2 = K(a,a)+K(b,b)-2K(a,b) ─
def knn_predict(K_te_row, K_tr, y_tr, k=3):
    diag_tr = np.diag(K_tr)
    dists   = 1.0 - K_te_row + 1e-9
    nn_idx  = np.argsort(dists)[:k]
    return np.sign(y_tr[nn_idx].sum())

preds = [knn_predict(K_te[i], K_tr, y_tr) for i in range(len(X_te))]
acc   = np.mean(np.array(preds) == y_te)
print(f"Quantum-kernel 3-NN test accuracy: {acc*100:.1f}%")

# ── print a slice of kernel matrix ───────────────────────────────────────────
print("\nTop-left 5x5 of quantum kernel matrix:")
print(np.round(K_tr[:5, :5], 4))
```
**Sample Output:**
```
Quantum-kernel 3-NN test accuracy: 83.3%

Top-left 5x5 of quantum kernel matrix:
[[1.     0.5643 0.1007 0.0606 0.8201]
 [0.5643 1.     0.521  0.0437 0.6377]
 [0.1007 0.521  1.     0.6478 0.0406]
 [0.0606 0.0437 0.6478 1.     0.1258]
 [0.8201 0.6377 0.0406 0.1258 1.    ]]
```

---

## Project 3: Loss Landscape Visualisation

| Feature | Description |
| :--- | :--- |
| **Goal** | Plot the 2-D loss landscape by sweeping two parameters of the classifier and identify flat vs sharp minima. |
| **Method** | Fix all but two parameters ($\theta_0, \theta_1$); sweep a $20\times20$ grid and print the loss surface statistics. |

---

### Complete Python Code

```python
```python
import numpy as np
from qiskit.circuit.library import ZZFeatureMap, RealAmplitudes
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector, SparsePauliOp

np.random.seed(7)
X_tr = np.vstack([np.random.randn(10, 2)*0.2 + [0.3,  0.3],
```
              np.random.randn(10, 2)*0.2 + [-0.3, -0.3]])
```
y_tr = np.array([1.0]*10 + [-1.0]*10)

fmap   = ZZFeatureMap(feature_dimension=2, reps=1)
ansatz = RealAmplitudes(num_qubits=2, reps=1)
vqc    = QuantumCircuit(2)
vqc.compose(fmap, inplace=True)
vqc.compose(ansatz, inplace=True)
obs_mat = SparsePauliOp.from_list([("ZI", 1.0)]).to_matrix()

theta_base = np.array([0.5, 0.8, 1.1, 0.3])

def loss_at(t0, t1):
```
theta = theta_base.copy()
theta[0] = t0; theta[1] = t1
total = 0.0
for x, lab in zip(X_tr, y_tr):
    pv = {**dict(zip(fmap.parameters, x)),
          **dict(zip(ansatz.parameters, theta))}
    sv = Statevector(vqc.assign_parameters(pv)).data
    exp = float(np.real(sv.conj() @ obs_mat @ sv))
    total += (exp - lab)**2
return total / len(y_tr)

```
grid   = np.linspace(0, 2*np.pi, 20)
losses = np.array([[loss_at(t0, t1) for t1 in grid] for t0 in grid])

print(f"Loss landscape stats (20x20 grid over theta_0, theta_1):")
print(f"  min loss : {losses.min():.5f}")
print(f"  max loss : {losses.max():.5f}")
print(f"  mean loss: {losses.mean():.5f}")
print(f"  std loss : {losses.std():.5f}")

flat_frac = (losses.max() - losses.min()) / losses.mean()
print(f"\nPeak-to-mean ratio: {flat_frac:.3f}")
if flat_frac < 0.5:
```
print("Relatively flat landscape — signs of barren plateau with 2 qubits.")
```
else:
```
print("Non-trivial landscape — gradient descent should converge.")

```
```
## Notes For Chapter Bridge
# **Chapter 12: quantum learning to the unsupervised regime: PCA, k-means, () () (Codebook)**
# and autoencoder patterns are recast as quantum state manipulation tasks.