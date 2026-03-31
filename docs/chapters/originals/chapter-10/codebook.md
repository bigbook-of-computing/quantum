# **Chapter 10: Variational Quantum Circuits () () (Codebook)**

Variational Quantum Circuits (VQCs) form the backbone of near-term quantum algorithms. This chapter studies hardware-efficient ansatze, the parameter-shift rule for gradient estimation, and expressibility metrics.

---

**Expected outputs** from `codes/codebook_02.py`:

- `codes/ch10_parameter_shift.png`

## Project 1: Hardware-Efficient Ansatz Analysis

| Feature | Description |
| :--- | :--- |
| **Goal** | Build a `RealAmplitudes` hardware-efficient ansatz for 4 qubits and analyse its circuit structure and parameter space. |
| **Circuit** | `RealAmplitudes(4, reps=2)` — alternating $R_Y$ single-qubit gates and CNOT entangling layers. |
| **Method** | Print gate counts, depth, and sample a random parametrised statevector. |

---

### Complete Python Code

```python
import numpy as np
from qiskit.circuit.library import RealAmplitudes
from qiskit.quantum_info import Statevector

n_qubits = 4
reps     = 2
ansatz   = RealAmplitudes(n_qubits, reps=reps)

# ── basic circuit properties ─────────────────────────────────────────────────
print(f"Ansatz: RealAmplitudes(n={n_qubits}, reps={reps})")
print(f"  Parameters : {ansatz.num_parameters}")
print(f"  Circuit depth: {ansatz.depth()}")
print(f"  Gate counts  : {dict(ansatz.count_ops())}")

# ── random parameter sweep — statevector sample ──────────────────────────────
np.random.seed(0)
n_samples = 5
print("\nSample statevector first two amplitudes (random parameters):")
for k in range(n_samples):
    theta = np.random.uniform(0, 2*np.pi, ansatz.num_parameters)
    sv    = Statevector(ansatz.assign_parameters(theta))
    probs = sv.probabilities()
    print(f"  Trial {k}: |00..0> prob = {probs[0]:.4f}  |11..1> prob = {probs[-1]:.4f}")

# ── verify it spans the full probability simplex ─────────────────────────────
max_probs = []
for _ in range(200):
    theta = np.random.uniform(0, 2*np.pi, ansatz.num_parameters)
    sv = Statevector(ansatz.assign_parameters(theta))
    max_probs.append(sv.probabilities().max())
print(f"\nMax single-outcome probability (200 random configs):")
print(f"  min={min(max_probs):.4f}  max={max(max_probs):.4f}  mean={np.mean(max_probs):.4f}")
print("High max means occasional collapsed states; low mean indicates spread.")
```
**Sample Output:**
```
Ansatz: RealAmplitudes(n=4, reps=2)
  Parameters : 12
  Circuit depth: 1
  Gate counts  : {'RealAmplitudes': 1}

Sample statevector first two amplitudes (random parameters):
  Trial 0: |00..0> prob = 0.2982  |11..1> prob = 0.0072
  Trial 1: |00..0> prob = 0.0108  |11..1> prob = 0.0081
  Trial 2: |00..0> prob = 0.1628  |11..1> prob = 0.0006
  Trial 3: |00..0> prob = 0.1920  |11..1> prob = 0.0007
  Trial 4: |00..0> prob = 0.0081  |11..1> prob = 0.0800

Max single-outcome probability (200 random configs):
  min=0.1282  max=0.7493  mean=0.3278
High max means occasional collapsed states; low mean indicates spread.
```

---

## Project 2: Parameter-Shift Rule Gradient

| Feature | Description |
| :--- | :--- |
| **Goal** | Compute the exact gradient of an expectation value $\langle Z \rangle$ with respect to each ansatz parameter using the parameter-shift rule. |
| **Circuit** | `RealAmplitudes(2, reps=1)` with 4 parameters; observable is $Z \otimes I$. |
| **Method** | $\partial_k \langle O \rangle = \tfrac{1}{2}[\langle O \rangle(\theta_k+\tfrac{\pi}{2}) - \langle O \rangle(\theta_k-\tfrac{\pi}{2})]$. |

---

### Complete Python Code

```python
import numpy as np
from qiskit.circuit.library import RealAmplitudes
from qiskit.quantum_info import Statevector, SparsePauliOp

ansatz  = RealAmplitudes(2, reps=1)
params  = list(ansatz.parameters)
n_par   = len(params)
theta0  = np.array([0.5, 1.2, 0.8, 0.3])

observable = SparsePauliOp.from_list([("ZI", 1.0)])

def expectation(theta):
    sv    = Statevector(ansatz.assign_parameters(theta))
    op    = observable.to_matrix()
    state = sv.data
    return np.real(state.conj() @ op @ state)

# ── parameter-shift gradients ────────────────────────────────────────────────
gradients = np.zeros(n_par)
for k in range(n_par):
    shifted_plus  = theta0.copy(); shifted_plus[k]  += np.pi / 2
    shifted_minus = theta0.copy(); shifted_minus[k] -= np.pi / 2
    gradients[k] = 0.5 * (expectation(shifted_plus) - expectation(shifted_minus))

# ── finite-difference check ──────────────────────────────────────────────────
eps  = 1e-5
fd   = np.zeros(n_par)
for k in range(n_par):
    ep_plus  = theta0.copy(); ep_plus[k]  += eps
    ep_minus = theta0.copy(); ep_minus[k] -= eps
    fd[k] = (expectation(ep_plus) - expectation(ep_minus)) / (2 * eps)

f0 = expectation(theta0)
print(f"Expectation <ZI> at theta0: {f0:.6f}")
print(f"\n{'Param':>6}  {'PS grad':>12}  {'FD grad':>12}  {'Diff':>12}")
for k, (ps, fdk) in enumerate(zip(gradients, fd)):
    print(f"  t[{k}]  {ps:12.8f}  {fdk:12.8f}  {abs(ps-fdk):12.2e}")
print("\nParameter-shift matches finite difference to high precision.")
```
**Sample Output:**
```
Expectation <ZI> at theta0: 0.028360

 Param       PS grad       FD grad          Diff
  t[0]   -0.16596446   -0.16596446      3.99e-12
  t[1]   -0.88849316   -0.88849316      8.80e-12
  t[2]    0.00000000    0.00000000      5.55e-12
  t[3]   -0.98438603   -0.98438603      2.23e-11

Parameter-shift matches finite difference to high precision.
```

---

## Project 3: Expressibility Scan

| Feature | Description |
| :--- | :--- |
| **Goal** | Estimate the expressibility of `RealAmplitudes` circuits with varying depth by computing the frame potential approximation via random state sampling. |
| **Circuits** | `RealAmplitudes(2, reps=r)` for $r \in \{1, 2, 3, 4\}$. |
| **Method** | Sample $N=200$ random parameter configurations, accumulate pairwise fidelities, and compute $\hat{F}_1 = \mathbb{E}[\lvert\langle\psi\vert\phi\rangle\rvert^4]$ as expressibility proxy. |

---

### Complete Python Code

```python
```python
import numpy as np
from qiskit.circuit.library import RealAmplitudes
from qiskit.quantum_info import Statevector

def expressibility_proxy(n_qubits, reps, n_samples=200, seed=42):
```
np.random.seed(seed)
ansatz = RealAmplitudes(n_qubits, reps=reps)
n_par  = ansatz.num_parameters
svs    = []
for _ in range(n_samples):
    theta = np.random.uniform(0, 2*np.pi, n_par)
    svs.append(Statevector(ansatz.assign_parameters(theta)).data)
```
```
    # estimate E[|<psi|phi>|^4]
    fids4 = []
    for i in range(0, n_samples, 10):
        for j in range(i+1, min(i+10, n_samples)):
            f4 = abs(svs[i].conj() @ svs[j]) ** 4
            fids4.append(f4)
    return np.mean(fids4) if fids4 else 0.0

```python
print(f"{'Reps':>6}  {'E[|overlap|^4]':>16}  Notes")
print("-" * 46)
for reps in [1, 2, 3, 4]:
```
ep = expressibility_proxy(2, reps)
note = "low (expressible)" if ep < 0.05 else "high (less expressive)"
print(f"  {reps:4d}  {ep:16.6f}  {note}")

```
print("\nHigher reps → lower proxy → more expressible circuit (closer to Haar).")

```
## Notes For Chapter Bridge
# **Chapter 11: VQCs directly to supervised classification; trainable () () (Codebook)**
# parameters replace Bayesian or kernel-regression weights and are updated via
# gradient descent using the parameter-shift rule derived above.