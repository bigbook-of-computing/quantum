# **Chapter 9: Quantum Data Encoding Techniques () () (Codebook)**

Choosing an encoding is the first design decision in any QML pipeline. This chapter surveys the main strategies — basis encoding, amplitude encoding, and angle/IQP encoding — and evaluates their scaling, expressibility, and fidelity properties.

---

**Expected outputs** from `codes/codebook_02.py`:

- `codes/ch9_gram_matrix.png`

## Project 1: Encoding Strategy Comparison

| Feature | Description |
| :--- | :--- |
| **Goal** | Implement basis, angle, and amplitude encoding for a 4-element classical vector and compare the resulting statevectors. |
| **Circuits** | Basis: computational basis preparation; Angle: single-qubit $R_Y$ rotations; Amplitude: `initialize` instruction normalising the vector. |
| **Method** | Print statevector amplitudes and verify inner products / Bloch coordinates. |

---

### Complete Python Code

```python
import numpy as np
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector

data = np.array([0.2, 0.5, 0.1, 0.8])

# ── 1. Basis encoding: integer index → computational basis ───────────────────

idx = int(np.argmax(data))   # encode the index of the max value
qc_basis = QuantumCircuit(2)
if idx & 1: qc_basis.x(0)
if idx & 2: qc_basis.x(1)
sv_basis = Statevector(qc_basis)
print(f"Basis encoding  (idx={idx}): {np.round(np.abs(sv_basis.data)**2, 3)}")

# ── 2. Angle encoding: R_Y(pi * x_i) on qubit i ─────────────────────────────

qc_angle = QuantumCircuit(4)
for i, xi in enumerate(data):
    qc_angle.ry(np.pi * xi, i)
sv_angle = Statevector(qc_angle)
print(f"Angle encoding  probs : {np.round(sv_angle.probabilities(), 3)}")

# ── 3. Amplitude encoding: normalise vector → state amplitudes ───────────────

norm   = np.linalg.norm(data)
amps   = data / norm
qc_amp = QuantumCircuit(2)
qc_amp.initialize(amps, [0, 1])
sv_amp = Statevector(qc_amp)
print(f"Amplitude encoding state: {np.round(sv_amp.data, 4)}")
print(f"Reconstruction fidelity : {abs(np.dot(sv_amp.data.conj(), amps))**2:.6f}")
```
**Sample Output:**
```python
Basis encoding  (idx=3): [0. 0. 0. 1.]
Angle encoding  probs : [0.042 0.004 0.042 0.004 0.001 0.    0.001 0.    0.399 0.042 0.399 0.042
 0.01  0.001 0.01  0.001]
Amplitude encoding state: [0.2063+0.j 0.5157+0.j 0.1031+0.j 0.8251+0.j]
Reconstruction fidelity : 1.000000
```

---

## Project 2: ZZFeatureMap Geometry

| Feature | Description |
| :--- | :--- |
| **Goal** | Visualise how `ZZFeatureMap` maps 1-D grid of inputs into 2-qubit Hilbert space by plotting the Gram matrix entries. |
| **Circuit** | `ZZFeatureMap` with 2 qubits, 2 reps, applied to a 20-point grid in $[-\pi, \pi]$. |
| **Method** | Compute statevector inner products and plot the resulting kernel heatmap values. |

---

### Complete Python Code

```python
import numpy as np
from qiskit.circuit.library import ZZFeatureMap
from qiskit.quantum_info import Statevector

fmap  = ZZFeatureMap(feature_dimension=2, reps=2)
grid  = np.linspace(-np.pi, np.pi, 12)
pairs = np.array([[g, g/2] for g in grid])

n    = len(pairs)
gram = np.zeros((n, n))
svs  = [Statevector(fmap.assign_parameters(p)) for p in pairs]

for i in range(n):
    for j in range(i, n):
        k = abs(svs[i].inner(svs[j])) ** 2
        gram[i, j] = k
        gram[j, i] = k

print("ZZFeatureMap Gram-matrix (diagonal = 1.0):")
print(np.round(gram, 3))

# ── kernel width: average off-diagonal entry ─────────────────────────────────

mask     = np.ones((n, n), bool); np.fill_diagonal(mask, False)
avg_off  = gram[mask].mean()
print(f"\nAvg off-diagonal kernel value: {avg_off:.4f}")
print("Low value => high-dimensional feature space (distinguishable states).")
```
**Sample Output:**
```python
ZZFeatureMap Gram-matrix (diagonal = 1.0):
[[1.    0.137 0.273 0.051 0.022 0.014 0.036 0.503 0.221 0.132 0.556 0.055]
 [0.137 1.    0.093 0.528 0.653 0.263 0.175 0.358 0.443 0.027 0.209 0.637]
 [0.273 0.093 1.    0.289 0.085 0.263 0.011 0.046 0.014 0.582 0.247 0.172]
 [0.051 0.528 0.289 1.    0.677 0.224 0.025 0.166 0.285 0.013 0.03  0.498]
 [0.022 0.653 0.085 0.677 1.    0.627 0.066 0.314 0.231 0.077 0.038 0.465]
 [0.014 0.263 0.263 0.224 0.627 1.    0.335 0.176 0.258 0.301 0.1   0.074]
 [0.036 0.175 0.011 0.025 0.066 0.335 1.    0.041 0.039 0.007 0.422 0.053]
 [0.503 0.358 0.046 0.166 0.314 0.176 0.041 1.    0.397 0.029 0.477 0.077]
 [0.221 0.443 0.014 0.285 0.231 0.258 0.039 0.397 1.    0.249 0.064 0.408]
 [0.132 0.027 0.582 0.013 0.077 0.301 0.007 0.029 0.249 1.    0.103 0.171]
 [0.556 0.209 0.247 0.03  0.038 0.1   0.422 0.477 0.064 0.103 1.    0.173]
 [0.055 0.637 0.172 0.498 0.465 0.074 0.053 0.077 0.408 0.171 0.173 1.   ]]

Avg off-diagonal kernel value: 0.2240
Low value => high-dimensional feature space (distinguishable states).
```

---

## Project 3: Encoding Fidelity Under Noise

| Feature | Description |
| :--- | :--- |
| **Goal** | Measure how depolarising noise degrades amplitude encoding fidelity as noise strength increases. |
| **Circuit** | 2-qubit amplitude encoding circuit with `initialize`, simulated on noisy `AerSimulator`. |
| **Method** | Compare ideal statevector fidelity with noisy density-matrix fidelity across noise rates $[0, 0.05, 0.1, 0.2]$. |

---

### Complete Python Code

```python
```python
import numpy as np
from qiskit import QuantumCircuit, transpile
from qiskit.quantum_info import Statevector, state_fidelity, DensityMatrix
from qiskit_aer import AerSimulator
from qiskit_aer.noise import NoiseModel, depolarizing_error

data    = np.array([0.5, 0.5, 0.5, 0.5])
target  = Statevector(data)

def build_encoding_circuit():
```
qc = QuantumCircuit(2)
qc.initialize(data, [0, 1])
return qc

```
noise_rates = [0.0, 0.02, 0.05, 0.10]
print(f"{'Noise p':>10}  {'Fidelity':>12}")
print("-" * 26)

for p in noise_rates:
```
nm = NoiseModel()
if p > 0:
    nm.add_all_qubit_quantum_error(depolarizing_error(p, 1), ['u1','u2','u3'])
    nm.add_all_qubit_quantum_error(depolarizing_error(p*2, 2), ['cx'])

sim = AerSimulator(noise_model=nm if p > 0 else None, method='density_matrix')
qc  = build_encoding_circuit()
qc.save_density_matrix()
qc_t = transpile(qc, sim)
result = sim.run(qc_t, shots=1).result()
dm   = DensityMatrix(result.data()['density_matrix'])
fid  = state_fidelity(dm, target)
print(f"{p:10.3f}  {fid:12.6f}")

```
```
## Notes For Chapter Bridge

# **Chapter 10: from encoding to the expressibility and trainability of () () (Codebook)**

# variational ansatze — the parametric circuits that sit after the feature map.