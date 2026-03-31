# **Chapter 15: Differentiable Quantum Programming () () (Codebook)**

Differentiable quantum programming treats quantum circuits as computational graphs through which gradients can flow. This chapter implements the parameter-shift gradient rule, natural-gradient optimisation, and compares modern gradient-aware optimisers on a VQC loss surface.

---

**Expected outputs** from `codes/codebook_02.py`:

- `codes/ch15_gradient_descent.png`

## Project 1: Parameter-Shift Gradient Verification

| Feature | Description |
| :--- | :--- |
| **Goal** | Verify the parameter-shift rule against finite differences and central differences for every parameter of a `RealAmplitudes(3, reps=2)` circuit. |
| **Observable** | $Z \otimes Z \otimes I$ expectation value. |
| **Method** | Compute $\nabla_k = \tfrac{1}{2}[\langle O \rangle_+ - \langle O \rangle_-]$ and compare with $\varepsilon=10^{-5}$ finite-difference. |

---

### Complete Python Code

```python
import numpy as np
from qiskit.circuit.library import RealAmplitudes
from qiskit.quantum_info import Statevector, SparsePauliOp

ansatz  = RealAmplitudes(3, reps=2)
n_par   = ansatz.num_parameters
obs_mat = SparsePauliOp.from_list([("IZZ", 1.0)]).to_matrix()

def expectation(theta):
    sv  = Statevector(ansatz.assign_parameters(theta)).data
    return float(np.real(sv.conj() @ obs_mat @ sv))

np.random.seed(0)
theta0 = np.random.uniform(0, 2*np.pi, n_par)
f0     = expectation(theta0)
print(f"<IZZ> at random theta: {f0:.6f}")

# ── parameter-shift gradients ─────────────────────────────────────────────────

grad_ps = np.zeros(n_par)
for k in range(n_par):
    tp, tm = theta0.copy(), theta0.copy()
    tp[k] += np.pi/2; tm[k] -= np.pi/2
    grad_ps[k] = 0.5*(expectation(tp) - expectation(tm))

# ── finite-difference check ───────────────────────────────────────────────────

eps    = 1e-5
grad_fd = np.zeros(n_par)
for k in range(n_par):
    tp, tm = theta0.copy(), theta0.copy()
    tp[k] += eps; tm[k] -= eps
    grad_fd[k] = (expectation(tp) - expectation(tm)) / (2*eps)

print(f"\n{'Param':>6}  {'PS':>12}  {'FD':>12}  {'|diff|':>12}")
for k in range(n_par):
    print(f"  [{k}]  {grad_ps[k]:12.8f}  {grad_fd[k]:12.8f}  {abs(grad_ps[k]-grad_fd[k]):12.2e}")

max_err = np.max(np.abs(grad_ps - grad_fd))
print(f"\nMax absolute error: {max_err:.2e}  (should be < 1e-4)")
```
**Sample Output:**
```python
<IZZ> at random theta: 0.684953

 Param            PS            FD        |diff|
  [0]   -0.11382309   -0.11382309      5.19e-12
  [1]   -0.39937354   -0.39937354      3.14e-11
  [2]   -0.02379122   -0.02379122      9.38e-12
  [3]   -0.36496377   -0.36496377      1.70e-11
  [4]   -0.43963428   -0.43963428      1.06e-11
  [5]   -0.13565447   -0.13565447      2.47e-12
  [6]    0.43887314    0.43887314      1.98e-11
  [7]   -0.07718810   -0.07718810      5.76e-12
  [8]    0.00000000   -0.00000000      1.11e-11

Max absolute error: 3.14e-11  (should be < 1e-4)
```

---

## Project 2: Natural Gradient vs Vanilla Gradient Descent

| Feature | Description |
| :--- | :--- |
| **Goal** | Compare plain gradient descent and natural gradient (using the diagonal quantum Fisher information metric) on a `RealAmplitudes(2, reps=2)` loss landscape. |
| **Method** | Compute diagonal QFI as $F_{kk} = 1 - \langle O \rangle^2_+ - \langle O \rangle^2_-$; precondition the gradient step. |

---

### Complete Python Code

```python
import numpy as np
from qiskit.circuit.library import RealAmplitudes
from qiskit.quantum_info import Statevector, SparsePauliOp

ansatz  = RealAmplitudes(2, reps=2)
n_par   = ansatz.num_parameters
obs_mat = SparsePauliOp.from_list([("ZI", 1.0)]).to_matrix()

def expectation(theta):
    sv = Statevector(ansatz.assign_parameters(theta)).data
    return float(np.real(sv.conj() @ obs_mat @ sv))

def ps_grad(theta):
    g = np.zeros(n_par)
    for k in range(n_par):
        tp, tm = theta.copy(), theta.copy()
        tp[k] += np.pi/2; tm[k] -= np.pi/2
        g[k] = 0.5*(expectation(tp) - expectation(tm))
    return g

def diag_qfi(theta):
    # F_kk approx = 1 - 0.5*(E+^2 + E-^2) using shift-rule components
    F = np.zeros(n_par)
    for k in range(n_par):
        tp, tm = theta.copy(), theta.copy()
        tp[k] += np.pi/2; tm[k] -= np.pi/2
        ep, em = expectation(tp), expectation(tm)
        F[k] = max(1e-6, 1.0 - 0.5*(ep**2 + em**2))
    return F

np.random.seed(7)
theta_gd = np.random.uniform(0, 2*np.pi, n_par)
theta_ng = theta_gd.copy()

lr = 0.2
print(f"{'Step':>5}  {'GD loss':>10}  {'NG loss':>10}")
for step in range(30):
    g_gd = ps_grad(theta_gd)
    theta_gd -= lr * g_gd
    g_ng = ps_grad(theta_ng)
    F    = diag_qfi(theta_ng)
    theta_ng -= lr * (g_ng / F)
    if step % 5 == 0:
        print(f"  {step:3d}  {expectation(theta_gd):10.6f}  {expectation(theta_ng):10.6f}")

print(f"\nFinal: GD={expectation(theta_gd):.6f}  NG={expectation(theta_ng):.6f}")
print("Natural gradient should converge faster toward minimum expectation.")
```
**Sample Output:**
```python
Step     GD loss     NG loss
    0   -0.838725   -0.971785
    5   -0.998757   -0.999853
   10   -0.999991   -0.999999
   15   -1.000000   -1.000000
   20   -1.000000   -1.000000
   25   -1.000000   -1.000000

Final: GD=-1.000000  NG=-1.000000
Natural gradient should converge faster toward minimum expectation.
```

---

## Project 3: Adam Optimiser Sweep on VQC Loss

| Feature | Description |
| :--- | :--- |
| **Goal** | Train a `ZZFeatureMap + RealAmplitudes` classifier using an Adam optimiser (implemented with the parameter-shift gradient) and compare learning rates. |
| **Method** | Implement Adam update rule; run with $\alpha \in \{0.01, 0.05, 0.1\}$ and report final loss. |

---

### Complete Python Code

```python
```python
import numpy as np
from qiskit.circuit.library import ZZFeatureMap, RealAmplitudes
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector, SparsePauliOp

np.random.seed(3)
X   = np.vstack([np.random.randn(8,2)*0.2+[0.4,0.4],
```
             np.random.randn(8,2)*0.2+[-0.4,-0.4]])
```
y   = np.array([1.0]*8 + [-1.0]*8)

fmap   = ZZFeatureMap(2, reps=1)
ansatz = RealAmplitudes(2, reps=1)
vqc    = QuantumCircuit(2)
vqc.compose(fmap, inplace=True); vqc.compose(ansatz, inplace=True)
obs_mat = SparsePauliOp.from_list([("ZI",1.0)]).to_matrix()

def predict(x, theta):
```
pv = {**dict(zip(fmap.parameters, x)),
      **dict(zip(ansatz.parameters, theta))}
sv = Statevector(vqc.assign_parameters(pv)).data
return float(np.real(sv.conj() @ obs_mat @ sv))

```
def loss(theta):
```
return np.mean([(predict(x,theta)-lab)**2 for x,lab in zip(X,y)])

```
def gradient(theta):
```
g = np.zeros(len(ansatz.parameters))
for k in range(len(g)):
    tp, tm = theta.copy(), theta.copy()
    tp[k] += np.pi/2; tm[k] -= np.pi/2
    g[k] = 0.5*(loss(tp) - loss(tm))
return g

```
def adam_train(lr, steps=30):
```
theta = np.random.uniform(0, 2*np.pi, len(ansatz.parameters))
m, v, b1, b2, ep = np.zeros_like(theta), np.zeros_like(theta), 0.9, 0.999, 1e-8
for t in range(1, steps+1):
    g  = gradient(theta)
    m  = b1*m + (1-b1)*g
    v  = b2*v + (1-b2)*g**2
    mh = m / (1-b1**t); vh = v / (1-b2**t)
    theta -= lr * mh / (np.sqrt(vh)+ep)
return loss(theta)

```
print(f"Adam final loss by learning rate:")
print(f"{'lr':>8}  {'Final Loss':>12}")
for lr in [0.01, 0.05, 0.10]:
```
np.random.seed(3)
fl = adam_train(lr)
print(f"  {lr:.2f}    {fl:12.6f}")

```
```
## Notes For Chapter Bridge

# **Chapter 16: from ideal simulation to hardware comparison: noise, T1/T2, () () (Codebook)**

# readout errors, and zero-noise extrapolation are studied systematically.