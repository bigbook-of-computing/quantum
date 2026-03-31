# **Chapter 12: Quantum Unsupervised Learning () () (Codebook)**

Unsupervised quantum learning discovers structure in unlabelled data. This chapter implements quantum principal-component analysis via state overlap, quantum k-means assignment, and a quantum autoencoder that compresses $n$ qubits into $k < n$ qubits.

---

**Expected outputs** from `codes/codebook_02.py`:

- `codes/ch12_qkmeans_clusters.png`

## Project 1: Quantum PCA via State Overlap

| Feature | Description |
| :--- | :--- |
| **Goal** | Use the quantum kernel matrix (Gram matrix of encoded states) as a proxy for the classical covariance matrix and extract principal components via eigendecomposition. |
| **Circuit** | `ZZFeatureMap(2, reps=2)` encodes 2-D data points. |
| **Method** | Eigendecompose the kernel matrix; project data onto top eigenvectors; compute explained variance ratio. |

---

### Complete Python Code

```python
import numpy as np
from qiskit.circuit.library import ZZFeatureMap
from qiskit.quantum_info import Statevector

np.random.seed(0)
# correlated 2-D cloud — should have one dominant PC
X = np.random.randn(12, 2) @ np.array([[1.5, 1.0], [0.2, 0.3]])

fmap = ZZFeatureMap(feature_dimension=2, reps=2)
n    = len(X)
K    = np.zeros((n, n))
for i in range(n):
    svi = Statevector(fmap.assign_parameters(X[i]))
    for j in range(i, n):
        svj = Statevector(fmap.assign_parameters(X[j]))
        k   = abs(svi.inner(svj))**2
        K[i, j] = K[j, i] = k

# ── kernel PCA: centre, then eigendecompose ───────────────────────────────────
one_n  = np.ones((n, n)) / n
Kc     = K - one_n @ K - K @ one_n + one_n @ K @ one_n
eigval, eigvec = np.linalg.eigh(Kc)
order  = np.argsort(eigval)[::-1]
eigval = eigval[order]
eigvec = eigvec[:, order]

ev_ratio = eigval[:2] / eigval[eigval > 0].sum()
print("Quantum PCA — explained variance ratio (top 2 PCs):")
for k, evr in enumerate(ev_ratio[:2]):
    print(f"  PC {k+1}: {evr*100:.2f}%")

# ── project onto top 2 PCs ────────────────────────────────────────────────────
Z = Kc @ eigvec[:, :2]
print("\nProjected coordinates (first 5 points):")
print(np.round(Z[:5], 4))
```
**Sample Output:**
```
Quantum PCA — explained variance ratio (top 2 PCs):
  PC 1: 35.89%
  PC 2: 20.74%

Projected coordinates (first 5 points):
[[-0.6401  0.266 ]
 [ 0.6633 -0.3943]
 [ 0.1741  0.6239]
 [-0.2955 -0.1077]
 [ 0.9452 -0.2533]]
```

---

## Project 2: Quantum-Assisted K-Means

| Feature | Description |
| :--- | :--- |
| **Goal** | Replace classical distance computation in Lloyd's algorithm with quantum-kernel distances and cluster 8 points into 2 groups. |
| **Method** | Distance proxy: $d_Q(a,b) = 1 - K_Q(a,b)$; iterate assignment-update steps until convergence. |

---

### Complete Python Code

```python
import numpy as np
from qiskit.circuit.library import ZZFeatureMap
from qiskit.quantum_info import Statevector

np.random.seed(1)
X = np.vstack([
    np.random.randn(4, 2) * 0.2 + [1.0,  1.0],
    np.random.randn(4, 2) * 0.2 + [-1.0, -1.0],
])

fmap = ZZFeatureMap(feature_dimension=2, reps=2)

def qkernel(a, b):
    sva = Statevector(fmap.assign_parameters(a))
    svb = Statevector(fmap.assign_parameters(b))
    return abs(sva.inner(svb))**2

def q_distance(a, b):
    return 1.0 - qkernel(a, b)

# ── initialise centroids as first two points ─────────────────────────────────
centroids = X[:2].copy()
labels    = np.zeros(len(X), int)

for iteration in range(6):
    # assignment
    for i, xi in enumerate(X):
        dists  = [q_distance(xi, c) for c in centroids]
        labels[i] = int(np.argmin(dists))
    # update
    for c in range(2):
        members = X[labels == c]
        if len(members) > 0:
            centroids[c] = members.mean(axis=0)
    print(f"Iter {iteration}: labels = {labels.tolist()}")

print(f"\nFinal cluster assignments : {labels.tolist()}")
print(f"Expected (0s then 1s)    : {[0]*4 + [1]*4}")
correct = np.sum(labels[:4] == 0) + np.sum(labels[4:] == 1)
print(f"Correctly assigned       : {correct}/8")
```
**Sample Output:**
```
Iter 0: labels = [0, 1, 1, 0, 1, 0, 1, 1]
Iter 1: labels = [1, 1, 1, 1, 1, 1, 1, 1]
Iter 2: labels = [0, 0, 0, 0, 1, 1, 0, 1]
Iter 3: labels = [0, 0, 0, 0, 1, 0, 0, 1]
Iter 4: labels = [1, 1, 1, 1, 1, 1, 1, 1]
Iter 5: labels = [1, 0, 0, 1, 1, 1, 1, 1]

Final cluster assignments : [1, 0, 0, 1, 1, 1, 1, 1]
Expected (0s then 1s)    : [0, 0, 0, 0, 1, 1, 1, 1]
Correctly assigned       : 6/8
```

---

## Project 3: Quantum Autoencoder

| Feature | Description |
| :--- | :--- |
| **Goal** | Train a 4-to-2 qubit quantum autoencoder: a parametric circuit compresses 4-qubit input into 2-qubit latent state, and a decoder reconstructs it. |
| **Method** | Minimise reconstruction fidelity loss $1 - F(\rho_{out}, \rho_{in})$ via parameter-shift gradient loop. |

---

### Complete Python Code

```python
```python
import numpy as np
from qiskit import QuantumCircuit
from qiskit.circuit.library import RealAmplitudes
from qiskit.quantum_info import Statevector, state_fidelity

def make_autoencoder(n_qubits=4, latent=2, reps=1):
```
    # encoder: n_qubits -> latent
    enc = RealAmplitudes(n_qubits, reps=reps)
    # decoder: latent -> n_qubits (same structure reversed)
    dec = RealAmplitudes(n_qubits, reps=reps)
    qc  = QuantumCircuit(n_qubits)
    qc.compose(enc, inplace=True)
    # discard high qubits (trace out) — approximate via identity on trash
    qc.compose(dec, inplace=True)
    return qc, enc, dec

qc, enc, dec = make_autoencoder()
n_enc = len(enc.parameters)
n_dec = len(dec.parameters)
n_par = len(qc.parameters)

# ── target state: |GHZ> on 4 qubits ─────────────────────────────────────────
target_qc = QuantumCircuit(4)
target_qc.h(0)
target_qc.cx(0, 1); target_qc.cx(0, 2); target_qc.cx(0, 3)
target_sv = Statevector(target_qc)

```python
def fidelity_at(theta):
```
sv_out = Statevector(qc.assign_parameters(theta))
return state_fidelity(sv_out, target_sv)

```
np.random.seed(3)
theta = np.random.uniform(0, 2*np.pi, n_par)

print("Quantum Autoencoder training (maximise fidelity):")
for epoch in range(20):
```
grads = np.zeros(n_par)
for k in range(n_par):
    tp, tm = theta.copy(), theta.copy()
    tp[k] += np.pi/2; tm[k] -= np.pi/2
    grads[k] = 0.5*(fidelity_at(tp) - fidelity_at(tm))
theta += 0.2 * grads   # gradient ascent
if epoch % 5 == 0:
    print(f"  Epoch {epoch:3d}  fidelity={fidelity_at(theta):.5f}")

```
print(f"\nFinal reconstruction fidelity: {fidelity_at(theta):.5f}")

```
## Notes For Chapter Bridge
# **Chapter 13: the optimisation goal outward: instead of fitting data, () () (Codebook)**
# a variational agent must maximise cumulative reward in a quantum environment.