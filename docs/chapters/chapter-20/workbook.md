# **Chapter 5: 1: Bit-flip and Phase-flip Codes () () () (Workbook)**

The goal of this chapter is to introduce the foundational principles of **Quantum Error Correction (QEC)** by analyzing the simplest repetition codes—the **3-qubit bit-flip code** and the **3-qubit phase-flip code**—and explaining the concept of **syndrome extraction** using ancilla qubits.

---

### 5.1.1 Types of Quantum Errors and Classical Analogy

> **Summary:** Quantum errors are not just bit flips ($X$ errors) but also **phase flips** ($Z$ errors). A general error is a combination of Pauli errors ($I, X, Y, Z$). The QEC philosophy is based on the **classical repetition code** (e.g., encoding $0$ as $000$) but must avoid collapsing the protected quantum superposition.

#### Quiz Questions

**1. An error that introduces a minus sign on the $|1\rangle$ component of a superposition state ($\alpha|0\rangle + \beta|1\rangle \to \alpha|0\rangle - \beta|1\rangle$) is known as a:**
* **A.** Bit-flip ($X$ error).
* **B.** **Phase-flip ($Z$ error)**. (Correct)
* **C.** $Y$ error.
* **D.** Ancilla error.

**2. Which theorem dictates that a QEC process cannot simply copy the quantum state multiple times to achieve redundancy?**
* **A.** The Threshold Theorem.
* **B.** The Stabilizer Formalism.
* **C.** **The No-cloning theorem**. (Correct)
* **D.** The Adiabatic Theorem.

#### Interview-Style Question

**Question:** Explain why protecting a logical qubit against a general single-qubit error requires protection against both $X$ and $Z$ errors, and not just $X$ errors.

**Answer Strategy:**
* **Pauli Error Basis:** A general, arbitrary error on a single qubit is mathematically represented as a linear combination of the four Pauli operators ($I, X, Y, Z$).
* **$Y$ Error:** The $Y$ error is the product of an $X$ error and a $Z$ error ($Y = iXZ$).
* **Necessity:** Therefore, any code that claims to correct a **general single-qubit error** must be able to independently detect and correct the two fundamental, non-commuting error components: the **bit-flip ($X$)** and the **phase-flip ($Z$)**. If a code only corrects $X$, it will fail on $Z$ or $Y$ errors.

---

### 5.1.3–5.1.4 Bit-flip and Phase-flip Codes

> **Summary:** The **3-qubit bit-flip code** protects against single $X$ errors by encoding $|{\psi}\rangle = \alpha |0\rangle + \beta |1\rangle$ as $|{\psi}_L\rangle = \alpha |000\rangle + \beta |111\rangle$. The **3-qubit phase-flip code** protects against single $Z$ errors by applying the bit-flip code logic in the Hadamard basis, resulting in the logical state $|{\psi}_L\rangle = \alpha |+++\rangle + \beta |---\rangle$. Both use **stabilizer measurements** to determine the error **syndrome**.

#### Quiz Questions

**1. What is the logical state $|1_L\rangle$ for the 3-qubit bit-flip code?**
* **A.** $|+++\rangle$.
* **B.** $\frac{1}{\sqrt{2}}(|000\rangle + |111\rangle)$.
* **C.** **$|111\rangle$**. (Correct)
* **D.** $|100\rangle$.

**2. The error detection for the 3-qubit bit-flip code relies on measuring the parity of which pairs of qubits?**
* **A.** $X_1 X_2$ and $X_2 X_3$.
* **B.** $X_1 Z_2$ and $Z_2 X_3$.
* **C.** **$Z_1 Z_2$ and $Z_2 Z_3$**. (Correct)
* **D.** $H_1 H_2$ and $H_2 H_3$.

#### Interview-Style Question

**Question:** Explain the intuitive reason why the **Phase-flip code** uses the **Hadamard basis** (states $|+\rangle, |-\rangle$) for its logical states.

**Answer Strategy:**
* **Interchangeability:** The Hadamard gate has the property that it maps the Pauli $X$ operator to the Pauli $Z$ operator, and vice-versa.
* **Rotation:** A **phase-flip ($Z$ error)** in the computational basis is equivalent to a **bit-flip ($X$ error)** in the Hadamard basis.
* **Intuition:** By rotating the code into the Hadamard basis using $H$ gates, the physical $Z$ error effectively becomes a physical $X$ error. The code can then simply reuse the established **Bit-flip code mechanism** (which is easy to analyze using majority voting) to correct the error, and then rotate back.

---

### 5.1.5–5.1.6 Syndrome Measurement and Stabilizers

> **Summary:** The core challenge of QEC is **syndrome extraction**, which detects the error location without collapsing the superposition of the data qubits. This is achieved using **ancilla qubits** entangled with the data qubit parities via CNOT gates. The code states must satisfy the **stabilizer formalism**, meaning all states $|{\psi}\rangle$ are eigenvectors with eigenvalue $+1$ for all stabilizer operators $S_i$.

#### Quiz Questions

**1. The primary purpose of using **ancilla qubits** in the error correction process is to:**
* **A.** Store the logical state redundantly.
* **B.** **Measure the error syndrome without collapsing the data qubit's superposition**. (Correct)
* **C.** Perform the correction by applying an inverse gate.
* **D.** Separate bit-flip and phase-flip errors.

**2. According to the stabilizer formalism, what must be true for all valid code states $|{\psi}\rangle$ and all stabilizer operators $S_i$?**
* **A.** $S_i |{\psi}\rangle = -|{\psi}\rangle$.
* **B.** $S_i |{\psi}\rangle = 0$.
* **C.** **$S_i |{\psi}\rangle = +|{\psi}\rangle$**. (Correct)
* **D.** $S_i |{\psi}\rangle = \delta_{ij} |{\psi}\rangle$.

## Hands-On Workbook Projects

These projects focus on demonstrating the encoding, stabilizer properties, and error detection logic of the 3-qubit codes.

### Project 1: Bit-flip Code Error Correction Logic

* **Goal:** Practice the error identification logic of the 3-qubit bit-flip code.
* **Setup:** The code measures the two stabilizers $S_A = Z_1 Z_2$ and $S_B = Z_2 Z_3$. The measured syndrome is a binary pair $(S_A, S_B)$.
* **Steps:**
    1.  An error $E=X_3$ (bit-flip on qubit 3) occurs. Calculate the resulting syndrome $(S_A, S_B)$. (Hint: $X_3$ commutes with $Z_1 Z_2$, but anti-commutes with $Z_2 Z_3$)
    2.  An error $E=X_2$ (bit-flip on qubit 2) occurs. Calculate the resulting syndrome $(S_A, S_B)$.
    3.  Explain how a decoding algorithm uses the syndrome $(1, 0)$ to determine the correction.

### Project 2: Phase-flip Code Encoding

* **Goal:** Verify the encoding steps for the phase-flip code.
* **Setup:** Start with the logical state $|{\psi}\rangle = \alpha |0\rangle + \beta |1\rangle$. The goal is to reach $|{\psi}_L\rangle = \alpha |+++\rangle + \beta |---\rangle$.
* **Steps:**
    1.  Write the basis states $|+\rangle$ and $|-\rangle$ in the computational basis $\{|0\rangle, |1\rangle\}$.
    2.  Write the explicit computational basis expansion for the target state $|+++\rangle$.
    3.  Explain, without using gates, why the encoding $|0\rangle \to |+++\rangle$ and $|1\rangle \to |---\rangle$ protects against $Z$ errors. (Hint: What does the $Z$ error do to $|+\rangle$ and $|-\rangle$?)

### Project 3: Logical Operator Identity

* **Goal:** Understand the properties of logical operators.
* **Setup:** For the 3-qubit bit-flip code, the logical $X$ operator is defined as $X_L = X_1 X_2 X_3$.
* **Steps:**
    1.  Apply $X_L$ to the logical state $|0_L\rangle = |000\rangle$. Show the result is the logical $|1_L\rangle$.
    2.  Show that $X_L$ commutes with the stabilizer $S_A = Z_1 Z_2$. (Hint: $X$ and $Z$ anti-commute, $[X, Z] = 2iY$).
    3.  Explain why commuting with the stabilizer is a necessary condition for a logical operator.

### Project 4: Error Detection vs. Correction

* **Goal:** Distinguish between error detection and correction.
* **Setup:** Consider a simpler 2-qubit code: $|{\psi}_L\rangle = \alpha |00\rangle + \beta |11\rangle$. Stabilizer is $S = Z_1 Z_2$.
* **Steps:**
    1.  Verify that this code can **detect** an $X_1$ error. (Hint: Check if the syndrome measurement $Z_1 Z_2$ changes from $+1$ to $-1$)
    2.  Explain why this code **cannot correct** the $X_1$ error. (Hint: What would the syndrome be for an $X_2$ error?)

---

## Python Implementations

### Project 1: Bit-flip Code Syndrome Calculation

```python
import numpy as np
from functools import reduce

I = np.eye(2, dtype=complex)
X = np.array([[0,1],[1,0]], dtype=complex)
Z = np.diag([1.,-1.]).astype(complex)
def tensor(*ops): return reduce(np.kron, ops)

S_A = tensor(Z, Z, I)   # Z0 Z1 I2
S_B = tensor(I, Z, Z)   # I0 Z1 Z2

syndrome_table = {
    (0, 0): None, # no error
    (1, 0): 0,    # X_0 error (anticommutes with S_A only)
    (1, 1): 1,    # X_1 error (anticommutes with both)
    (0, 1): 2,    # X_2 error (anticommutes with S_B only)
}

ket_0L = np.zeros(8); ket_0L[0] = 1.

print("Syndrome table verification:")
for error_q in range(3):
    ops = [I, I, I]; ops[error_q] = X
    E = tensor(*ops)
    state = E @ ket_0L
    # syndrome: 0 if eigenvalue +1, 1 if eigenvalue -1
    sA = int(round((1 - np.real(state @ S_A @ state)) / 2))
    sB = int(round((1 - np.real(state @ S_B @ state)) / 2))
    detected = syndrome_table.get((sA, sB))
    correct = (detected == error_q)
    print(f"  X_{error_q}: syndrome=({sA},{sB}) -> detected qubit {detected} [{'OK' if correct else 'FAIL'}]")
```
**Sample Output:**
```python
Syndrome table verification:
  X_0: syndrome=(1,0) -> detected qubit 0 [OK]
  X_1: syndrome=(1,1) -> detected qubit 1 [OK]
  X_2: syndrome=(0,1) -> detected qubit 2 [OK]
```


### Project 2: Phase-flip Code Encoding

```python
import numpy as np
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector

ket_plus  = np.array([1, 1], dtype=complex) / np.sqrt(2)
ket_minus = np.array([1,-1], dtype=complex) / np.sqrt(2)
Z = np.diag([1.,-1.]).astype(complex)

print("Hadamard basis states:")
print(f"  |+> = {ket_plus}")
print(f"  |-> = {ket_minus}")

# Z error transforms |+> -> |->

print(f"\nZ|+> = {Z @ ket_plus}  (= |-> = {ket_minus}? {np.allclose(Z@ket_plus, ket_minus)})")

# |+++> in computational basis: 8 components, each = 1/(2*sqrt(2))

ket_ppp = np.kron(np.kron(ket_plus, ket_plus), ket_plus)
print(f"\n|+++> has {len(ket_ppp)} components, each = {np.real(ket_ppp[0]):.4f}")

# Phase-flip encoding circuit

def encode_phase_flip(alpha, beta):
    norm = np.sqrt(abs(alpha)**2 + abs(beta)**2)
    qc = QuantumCircuit(3)
    qc.initialize([alpha/norm, beta/norm], 0)
    qc.cx(0, 1); qc.cx(0, 2)
    qc.h([0, 1, 2])
    return qc

qc = encode_phase_flip(1/np.sqrt(2), 1/np.sqrt(2))
sv = Statevector(qc)
print("\nEncoded |+_L> amplitudes (expect all equal magnitude):")
for i, amp in enumerate(sv.data):
    if abs(amp) > 1e-6: print(f"  |{i:03b}> : {amp:+.4f}")
```
**Sample Output:**
```python
Hadamard basis states:
  |+> = [0.70710678+0.j 0.70710678+0.j]
  |-> = [ 0.70710678+0.j -0.70710678+0.j]

Z|+> = [ 0.70710678+0.j -0.70710678+0.j]  (= |-> = [ 0.70710678+0.j -0.70710678+0.j]? True)

|+++> has 8 components, each = 0.3536

Encoded |+_L> amplitudes (expect all equal magnitude):
  |000> : +0.5000+0.0000j
  |011> : +0.5000+0.0000j
  |101> : +0.5000+0.0000j
  |110> : +0.5000+0.0000j
```


### Project 3: Logical Operator Identity

```python
import numpy as np
from functools import reduce

I = np.eye(2, dtype=complex)
X = np.array([[0,1],[1,0]], dtype=complex)
Z = np.diag([1.,-1.]).astype(complex)
def tensor(*ops): return reduce(np.kron, ops)

X_L = tensor(X, X, X)       # logical X_L = X0 X1 X2
S_A  = tensor(Z, Z, I)       # stabilizer Z0 Z1 I2
S_B  = tensor(I, Z, Z)       # stabilizer I0 Z1 Z2

ket_0L = np.zeros(8); ket_0L[0] = 1.0   # |000>
ket_1L = np.zeros(8); ket_1L[7] = 1.0   # |111>

# X_L flips the logical qubit

print("X_L |0_L> = |", np.argmax(np.abs(X_L @ ket_0L)), ">  (index 7 = |111>)")
print("X_L |1_L> = |", np.argmax(np.abs(X_L @ ket_1L)), ">  (index 0 = |000>)")

# X_L must commute with all stabilizers (preserves code space)

print("\nCommutation relations:")
print("  X_L S_A = S_A X_L?", np.allclose(X_L @ S_A, S_A @ X_L))
print("  X_L S_B = S_B X_L?", np.allclose(X_L @ S_B, S_B @ X_L))

# Code states are +1 eigenstates of stabilizers

print("\nStabilizer eigenvalues on code states:")
print("  S_A|0_L> = +|0_L>?", np.allclose(S_A @ ket_0L,  ket_0L))
print("  S_B|1_L> = +|1_L>?", np.allclose(S_B @ ket_1L,  ket_1L))
```
**Sample Output:**
```python
X_L |0_L> = | 7 >  (index 7 = |111>)
X_L |1_L> = | 0 >  (index 0 = |000>)

Commutation relations:
  X_L S_A = S_A X_L? True
  X_L S_B = S_B X_L? True

Stabilizer eigenvalues on code states:
  S_A|0_L> = +|0_L>? True
  S_B|1_L> = +|1_L>? True
```


### Project 4: Error Detection vs Correction

```python
import numpy as np
from functools import reduce

I = np.eye(2, dtype=complex)
X = np.array([[0,1],[1,0]], dtype=complex)
Z = np.diag([1.,-1.]).astype(complex)
def tensor(*ops): return reduce(np.kron, ops)

# 2-qubit code: |psi_L> = alpha|00> + beta|11>, stabilizer S = Z x Z

S  = tensor(Z, Z)
X1 = tensor(X, I)
X2 = tensor(I, X)

ket_0L = np.array([1,0,0,0], dtype=complex)  # |00>
ket_1L = np.array([0,0,0,1], dtype=complex)  # |11>

def syndrome_eigenvalue(state, operator):
    return np.real(state.conj() @ operator @ state)

# Code states should be +1 eigenstates of S

print("Stabilizer eigenvalue on code states:")
print(f"  S|00>: {syndrome_eigenvalue(ket_0L, S):+.0f}  (+1 means in code space)")
print(f"  S|11>: {syndrome_eigenvalue(ket_1L, S):+.0f}  (+1 means in code space)")

# Errors flip syndrome to -1

print("\nSyndrome after single-qubit errors:")
for E, name in [(X1, "X_1"), (X2, "X_2")]:
    err = E @ ket_0L
    s = syndrome_eigenvalue(err, S)
    print(f"  After {name}: syndrome eigenvalue = {s:+.0f}  (detectable: {s < 0})")

print("\nConclusion: Both X_1 and X_2 give syndrome=-1.")
print("Cannot distinguish them -> detection only, correction impossible.")
```
**Sample Output:**
```python
Stabilizer eigenvalue on code states:
  S|00>: +1  (+1 means in code space)
  S|11>: +1  (+1 means in code space)

Syndrome after single-qubit errors:
  After X_1: syndrome eigenvalue = -1  (detectable: True)
  After X_2: syndrome eigenvalue = -1  (detectable: True)

Conclusion: Both X_1 and X_2 give syndrome=-1.
Cannot distinguish them -> detection only, correction impossible.
```