# **Chapter 2: State and Operators () () (Codebook)**

This codebook makes the abstract formalism of Chapter 2 concrete: quantum states as vectors, operators as matrices, and expectation values as measurable quantities. All examples use NumPy and Qiskit `quantum_info`.

---

**Expected outputs** from `codes/codebook_02.py`:

- `codes/ch2_pauli_expectations.png`

## Project 1: Pauli Operator Expectation Values

| Feature | Description |
| :--- | :--- |
| **Goal** | Compute $\langle X \rangle$, $\langle Y \rangle$, $\langle Z \rangle$ for a general Bloch state $|\psi(\theta,\phi)\rangle$ and verify against the analytic Bloch vector formulae $(\sin\theta\cos\phi,\, \sin\theta\sin\phi,\, \cos\theta)$. |
| **Method** | `SparsePauliOp` expectation values via `Statevector.expectation_value`. |

---

### Complete Python Code

```python
import numpy as np
from qiskit.quantum_info import Statevector, SparsePauliOp

X = SparsePauliOp("X")
Y = SparsePauliOp("Y")
Z = SparsePauliOp("Z")

def bloch_state(theta, phi):
    return Statevector([np.cos(theta / 2),
                        np.exp(1j * phi) * np.sin(theta / 2)])

test_cases = [
    (np.pi / 2, 0,           "|+>"),
    (np.pi / 2, np.pi / 2,   "|i>"),
    (0,         0,            "|0>"),
    (np.pi,     0,            "|1>"),
    (np.pi / 2, np.pi / 4,   "equator phi=pi/4"),
]

header = f"{'State':<20} {'<X>':>8} {'<Y>':>8} {'<Z>':>8}   theory"
print(header)
print("-" * len(header))

for theta, phi, label in test_cases:
    sv = bloch_state(theta, phi)
    ex = float(sv.expectation_value(X).real)
    ey = float(sv.expectation_value(Y).real)
    ez = float(sv.expectation_value(Z).real)
    tx = np.sin(theta) * np.cos(phi)
    ty = np.sin(theta) * np.sin(phi)
    tz = np.cos(theta)
    print(f"{label:<20} {ex:>8.4f} {ey:>8.4f} {ez:>8.4f}   "
          f"({tx:.4f}, {ty:.4f}, {tz:.4f})")

print()
print("Max deviation between simulation and analytic Bloch vector:")
errs = []
for theta, phi, _ in test_cases:
    sv = bloch_state(theta, phi)
    errs.append(max(
        abs(float(sv.expectation_value(X).real) - np.sin(theta)*np.cos(phi)),
        abs(float(sv.expectation_value(Y).real) - np.sin(theta)*np.sin(phi)),
        abs(float(sv.expectation_value(Z).real) - np.cos(theta)),
    ))
print(f"  {max(errs):.2e}")
```
**Sample Output:**
```python
State                     <X>      <Y>      <Z>   theory

---

|+>                    1.0000   0.0000   0.0000   (1.0000, 0.0000, 0.0000)
|i>                    0.0000   1.0000   0.0000   (0.0000, 1.0000, 0.0000)
|0>                    0.0000   0.0000   1.0000   (0.0000, 0.0000, 1.0000)
|1>                    0.0000   0.0000  -1.0000   (0.0000, 0.0000, -1.0000)
equator phi=pi/4       0.7071   0.7071   0.0000   (0.7071, 0.7071, 0.0000)

Max deviation between simulation and analytic Bloch vector:
  1.61e-16
```

---

## Project 2: Operator Unitarity and Hermiticity Checks

| Feature | Description |
| :--- | :--- |
| **Goal** | Build standard single-qubit gate matrices numerically and verify: Pauli gates are Hermitian and unitary; $R_y(\theta)$ is unitary but not generally Hermitian; Hadamard is both. |
| **Method** | NumPy: $U U^\dagger = I$ (unitarity), $M = M^\dagger$ (Hermiticity). |

---

### Complete Python Code

```python
import numpy as np

I2 = np.eye(2, dtype=complex)

def is_unitary(M, tol=1e-12):
    return np.allclose(M @ M.conj().T, I2, atol=tol)

def is_hermitian(M, tol=1e-12):
    return np.allclose(M, M.conj().T, atol=tol)

H_gate = np.array([[1, 1], [1, -1]], dtype=complex) / np.sqrt(2)
X_gate = np.array([[0, 1], [1,  0]], dtype=complex)
Y_gate = np.array([[0, -1j], [1j, 0]], dtype=complex)
Z_gate = np.array([[1, 0], [0, -1]], dtype=complex)
S_gate = np.array([[1, 0], [0, 1j]], dtype=complex)
T_gate = np.array([[1, 0], [0, np.exp(1j*np.pi/4)]], dtype=complex)

def Ry(theta):
    c, s = np.cos(theta/2), np.sin(theta/2)
    return np.array([[c, -s], [s, c]], dtype=complex)

gates = {
    "H":       H_gate,
    "X":       X_gate,
    "Y":       Y_gate,
    "Z":       Z_gate,
    "S":       S_gate,
    "T":       T_gate,
    "Ry(pi/3)": Ry(np.pi/3),
    "Ry(pi)":   Ry(np.pi),
}

print(f"{'Gate':<12}  {'Unitary?':<10}  {'Hermitian?':<12}  {'||UU†-I||_inf':>15}")
print("-" * 55)
for name, M in gates.items():
    err = np.max(np.abs(M @ M.conj().T - I2))
    print(f"{name:<12}  {str(is_unitary(M)):<10}  {str(is_hermitian(M)):<12}  {err:.2e}")

print()
print("Pauli eigenvalues (should be +/-1):")
for name, M in [("X", X_gate), ("Y", Y_gate), ("Z", Z_gate)]:
    evals = np.linalg.eigvalsh(M)
    print(f"  {name}: {evals}")
```
**Sample Output:**
```python
Gate          Unitary?    Hermitian?      ||UU†-I||_inf

---

H             True        True          2.22e-16
X             True        True          0.00e+00
Y             True        True          0.00e+00
Z             True        True          0.00e+00
S             True        False         0.00e+00
T             True        False         0.00e+00
Ry(pi/3)      True        False         7.44e-18
Ry(pi)        True        False         0.00e+00

Pauli eigenvalues (should be +/-1):
  X: [-1.  1.]
  Y: [-1.  1.]
  Z: [-1.  1.]
```

---

## Project 3: Density Matrix and Mixed-State Purity

| Feature | Description |
| :--- | :--- |
| **Goal** | Construct density matrices for pure and mixed states, compute purity $\text{Tr}(\rho^2)$ and von Neumann entropy $S = -\text{Tr}(\rho \log_2 \rho)$. |
| **Method** | `qiskit.quantum_info.DensityMatrix` plus NumPy trace arithmetic. |

---

### Complete Python Code

```python
import numpy as np
from qiskit.quantum_info import DensityMatrix, Statevector

# Pure states

psi_plus  = Statevector([1/np.sqrt(2),  1/np.sqrt(2)])
psi_minus = Statevector([1/np.sqrt(2), -1/np.sqrt(2)])
psi_0     = Statevector([1, 0])
psi_1     = Statevector([0, 1])
psi_i     = Statevector([1/np.sqrt(2), 1j/np.sqrt(2)])

pure_states = [("|+>", psi_plus), ("|->", psi_minus),
               ("|0>", psi_0),   ("|1>", psi_1)]

# Mixed states

rho_max = DensityMatrix(0.5 * np.eye(2, dtype=complex))
rho_partial = DensityMatrix(
    0.7 * np.outer(psi_plus.data, psi_plus.data.conj()) +
    0.3 * np.outer(psi_i.data,    psi_i.data.conj())
)

print(f"{'State':<30}  {'Tr(rho)':>8}  {'Tr(rho^2)':>10}  Pure?")
print("-" * 62)

for name, sv in pure_states:
    dm     = DensityMatrix(sv)
    tr     = np.trace(dm.data).real
    purity = np.trace(dm.data @ dm.data).real
    print(f"{name:<30}  {tr:>8.6f}  {purity:>10.6f}  {purity > 0.9999}")

for name, dm in [("Maximally mixed (rho=I/2)", rho_max),
                 ("70%|+> + 30%|i>",            rho_partial)]:
    tr     = np.trace(dm.data).real
    purity = np.trace(dm.data @ dm.data).real
    print(f"{name:<30}  {tr:>8.6f}  {purity:>10.6f}  {purity > 0.9999}")

print()
print("Von Neumann entropy S = -Tr(rho * log2(rho)):")
for name, dm in [("Maximally mixed", rho_max),
                 ("70%|+> + 30%|i>", rho_partial)]:
    evals   = np.linalg.eigvalsh(dm.data)
    evals   = evals[evals > 1e-12]
    entropy = -np.sum(evals * np.log2(evals))
    print(f"  {name}: S = {entropy:.6f} bits")
```
**Sample Output:**
```python
State                            Tr(rho)   Tr(rho^2)  Pure?

---

|+>                             1.000000    1.000000  True
|->                             1.000000    1.000000  True
|0>                             1.000000    1.000000  True
|1>                             1.000000    1.000000  True
Maximally mixed (rho=I/2)       1.000000    0.500000  False
70%|+> + 30%|i>                 1.000000    0.790000  False

Von Neumann entropy S = -Tr(rho * log2(rho)):
  Maximally mixed: S = 1.000000 bits
  70%|+> + 30%|i>: S = 0.527090 bits
```

---

## Notes For Chapter Bridge

The density matrix formalism and operator algebra established here underpin Chapter 3, where unitary gates are composed into circuits and their combined action is analysed as matrix products.