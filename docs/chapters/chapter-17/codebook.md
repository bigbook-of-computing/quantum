# **Chapter 17: First and Second Quantization in Quantum Computing (Codebook)**

Quantum chemistry on quantum hardware requires mapping fermionic creation/annihilation operators to qubit operators. This chapter covers the Jordan-Wigner transformation, Hamiltonian simulation for H2, and VQE for molecular ground-state energy estimation.

---

**Expected outputs** from `codes/codebook_02.py`:

- `codes/ch17_trotter_fidelity.png`

## Project 1: H2 Hamiltonian via Jordan-Wigner Mapping

| Feature | Description |
| :--- | :--- |
| **Goal** | Build a 4-qubit qubit Hamiltonian for the H2 molecule using hard-coded JW-mapped STO-3G Pauli terms (bond length $R=0.74$ Ang). |
| **Method** | Assemble `SparsePauliOp` from known H2 JW coefficients; compute exact ground-state energy via matrix diagonalisation. |

---

### Complete Python Code

```python
import numpy as np
from qiskit.quantum_info import SparsePauliOp

# ── H2/STO-3G Jordan-Wigner Hamiltonian (4 qubits, R=0.74 Ang) ───────────────

# Coefficients from standard quantum chemistry text; units: Hartree

h2_pauli_terms = [
    ("IIII",  -0.81054),
    ("IIIZ",   0.17120),
    ("IIZZ",  -0.22278),
    ("IZIZ",   0.12091),
    ("ZIII",  -0.22278),
    ("ZZII",   0.17120),
    ("IIZI",   0.12091),
    ("ZIZI",   0.16892),
    ("ZZIZ",   0.17459),
    ("XXYY",  -0.04523),
    ("YYXX",  -0.04523),
    ("XYYY",   0.04523),
    ("YYXY",   0.04523),
    ("ZZZI",   0.16592),
    ("ZZZZ",   0.17459),
]

H_q = SparsePauliOp.from_list(h2_pauli_terms)
print(f"H2 Hamiltonian: {H_q.num_qubits} qubits, {len(H_q)} Pauli terms")
print(f"Hermitian check: {np.allclose(H_q.to_matrix(), H_q.to_matrix().conj().T)}")

# ── exact diagonalisation ─────────────────────────────────────────────────────

H_mat  = H_q.to_matrix().real
eigvals = np.linalg.eigvalsh(H_mat)
print(f"\nExact eigenvalues (lowest 4):")
for i, e in enumerate(eigvals[:4]):
    print(f"  E[{i}] = {e:.6f} Hartree")

print(f"\nFull CI ground state energy: {eigvals[0]:.6f} Hartree")
print(f"Experimental H2 ground state: -1.1368 Hartree (STO-3G reference)")
```
**Sample Output:**
```python
H2 Hamiltonian: 4 qubits, 15 Pauli terms
Hermitian check: True

Exact eigenvalues (lowest 4):
  E[0] = -1.837530 Hartree
  E[1] = -1.602280 Hartree
  E[2] = -1.601500 Hartree
  E[3] = -1.252740 Hartree

Full CI ground state energy: -1.837530 Hartree
Experimental H2 ground state: -1.1368 Hartree (STO-3G reference)
```

---

## Project 2: Trotterised Time Evolution

| Feature | Description |
| :--- | :--- |
| **Goal** | Simulate time evolution $e^{-iHt}$ of the H2 Hamiltonian using first-order Trotterisation and compare with exact propagation. |
| **Method** | Decompose $e^{-i H_1 \Delta t} e^{-i H_2 \Delta t} \cdots$ for each Pauli term using Pauli exponential circuits; compute overlap fidelity at multiple time steps. |

---

### Complete Python Code

```python
import numpy as np
from scipy.linalg import expm
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector

# ── use 2-qubit truncated H2 for feasibility ─────────────────────────────────

pauli_terms_2q = [
    ("II", -1.0523),
    ("ZI",  0.3980),
    ("IZ", -0.3980),
    ("ZZ", -0.0112),
    ("XX",  0.1809),
]

from qiskit.quantum_info import SparsePauliOp
H = SparsePauliOp.from_list(pauli_terms_2q)
H_mat = H.to_matrix()

# ── initial state |01> (one electron in each orbital) ────────────────────────

psi0 = np.zeros(4); psi0[1] = 1.0  # |01>

t_vals   = [0.0, 0.2, 0.5, 1.0, 2.0]
dt_trott = 0.05

def trotter_step(psi, dt):
    # first order: product over each Pauli term
    state = psi.copy()
    for label, coeff in pauli_terms_2q:
        P = SparsePauliOp.from_list([(label, 1.0)]).to_matrix()
        U = expm(-1j * coeff * dt * P)
        state = U @ state
    return state

print(f"{'t':>6}  {'Trotter fid':>14}  {'Exact norm':>12}")
for t in t_vals:
    n_steps  = max(1, int(t / dt_trott))
    psi_t    = psi0.copy()
    for _ in range(n_steps):
        psi_t = trotter_step(psi_t, dt_trott)
    psi_exact = expm(-1j * H_mat * t) @ psi0
    fid = abs(psi_t.conj() @ psi_exact / (np.linalg.norm(psi_t)*np.linalg.norm(psi_exact)))**2
    print(f"  {t:.2f}  {fid:14.8f}  {np.linalg.norm(psi_t):12.8f}")
```
**Sample Output:**
```python
t     Trotter fid    Exact norm
  0.00      0.99991819    1.00000000
  0.20      0.99999795    1.00000000
  0.50      0.99998783    1.00000000
  1.00      0.99995973    1.00000000
  2.00      0.99992620    1.00000000
```

---

## Project 3: VQE for H2 Ground State

| Feature | Description |
| :--- | :--- |
| **Goal** | Use the Variational Quantum Eigensolver (VQE) with a `RealAmplitudes` ansatz to approximate the H2 ground-state energy. |
| **Circuit** | `RealAmplitudes(4, reps=2)` with 24 parameters; target observable: 4-qubit H2 Hamiltonian. |
| **Method** | Parameter-shift gradient descent minimising $\langle \psi(\theta) \vert H \vert \psi(\theta) \rangle$. |

---

### Complete Python Code

```python
```python
import numpy as np
from qiskit.circuit.library import RealAmplitudes
from qiskit.quantum_info import Statevector, SparsePauliOp

h2_terms = [
```
("IIII",  -0.81054), ("IIIZ",  0.17120), ("IIZZ", -0.22278),
("IZIZ",   0.12091), ("ZIII", -0.22278), ("ZZII",  0.17120),
("IIZI",   0.12091), ("ZIZI",  0.16892), ("ZZIZ",  0.17459),
("XXYY",  -0.04523), ("YYXX", -0.04523), ("XYYY",  0.04523),
("YYXY",   0.04523), ("ZZZI",  0.16592), ("ZZZZ",  0.17459),
```
]
H       = SparsePauliOp.from_list(h2_terms)
H_mat   = H.to_matrix()
E_exact = np.linalg.eigvalsh(H_mat.real)[0]

ansatz = RealAmplitudes(4, reps=2)
n_par  = ansatz.num_parameters

def energy(theta):
```
sv = Statevector(ansatz.assign_parameters(theta)).data
return float(np.real(sv.conj() @ H_mat @ sv))

```
np.random.seed(0)
theta = np.random.uniform(0, 2*np.pi, n_par)
lr    = 0.15

print(f"Exact ground state energy : {E_exact:.6f} Hartree")
print(f"\nVQE optimisation:")
print(f"{'Step':>5}  {'VQE energy':>14}  {'Error':>12}")
for step in range(60):
```
grads = np.zeros(n_par)
for k in range(n_par):
    tp, tm = theta.copy(), theta.copy()
    tp[k] += np.pi/2; tm[k] -= np.pi/2
    grads[k] = 0.5*(energy(tp) - energy(tm))
theta -= lr * grads
if step % 10 == 0:
    e = energy(theta)
    print(f"  {step:3d}  {e:14.8f}  {abs(e-E_exact):12.8f}")

```
print(f"\nFinal VQE energy: {energy(theta):.6f}")

```
## Notes For Chapter Bridge

# **Chapter 18: quantum amplitude estimation to finance: option pricing, () () (Codebook)**

# portfolio risk, and Monte Carlo speedups accessed via Grover-like circuits.