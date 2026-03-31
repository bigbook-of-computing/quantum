# **Chapter 20: Quantum Error Correction () () (Codebook)**

Quantum error correction (QEC) encodes logical qubits in multiple physical qubits so that errors can be detected and corrected without collapsing the quantum state. This chapter implements the 3-qubit bit-flip code, the 3-qubit phase-flip code, and the 7-qubit Steane code.

---

**Expected outputs** from `codes/codebook_02.py`:

- `codes/ch20_syndrome_results.png`

## Project 1: 3-Qubit Bit-Flip Code

| Feature | Description |
| :--- | :--- |
| **Goal** | Encode a logical qubit $\vert \psi_L \rangle = \alpha\vert 000 \rangle + \beta \vert 111 \rangle$, inject a random single-qubit $X$ error, detect the syndrome via ancilla measurements, and correct the error. |
| **Circuit** | 3 data qubits + 2 syndrome ancilla qubits; CNOT fan-out encoding; parity-check syndrome extraction. |
| **Method** | Simulate without error, with error on qubit 0/1/2; verify syndrome correctly identifies each case. |

---

### Complete Python Code

```python
import numpy as np
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator

def bit_flip_code(error_qubit=None):
    qc = QuantumCircuit(5, 2)  # q0,q1,q2=data; q3,q4=ancilla

    # ── encode: |psi>|0>|0> -> alpha|000> + beta|111> ───────────────────────
    qc.ry(np.pi/3, 0)   # arbitrary logical |psi>
    qc.cx(0, 1); qc.cx(0, 2)

    # ── inject error ──────────────────────────────────────────────────────────
    if error_qubit is not None:
        qc.x(error_qubit)

    # ── syndrome measurement: s0 = q0 XOR q1, s1 = q1 XOR q2 ────────────────
    qc.cx(0, 3); qc.cx(1, 3)   # s0 ancilla
    qc.cx(1, 4); qc.cx(2, 4)   # s1 ancilla
    qc.measure(3, 0); qc.measure(4, 1)

    return qc

sim   = AerSimulator(method='statevector')
cases = {None: "no error", 0: "X on q0", 1: "X on q1", 2: "X on q2"}

print("Bit-flip code syndrome results:")
print(f"{'Case':>12}  {'s0,s1 (most common)':>22}  {'Correct correction?':>22}")
for eq, label in cases.items():
    qc = bit_flip_code(eq)
    tc = transpile(qc, sim, optimization_level=0)
    res = sim.run(tc, shots=1024).result()
    counts = res.get_counts()
    top = max(counts, key=counts.get)
    s0, s1 = int(top[1]), int(top[0])  # little-endian

    # correction rule: s1s0 -> error qubit (00=none,01=q0,10=q2,11=q1)
    syndrome_table = {"00": None, "01": 0, "11": 1, "10": 2}
    detected = syndrome_table.get(f"{s1}{s0}", "?")
    correct  = (detected == eq)
    print(f"  {label:>12}  s0={s0} s1={s1} -> q{detected}  {'YES' if correct else 'NO':>22}")
```
**Sample Output:**
```python
Bit-flip code syndrome results:
        Case     s0,s1 (most common)     Correct correction?
      no error  s0=0 s1=0 -> qNone                     YES
       X on q0  s0=1 s1=0 -> q0                     YES
       X on q1  s0=1 s1=1 -> q1                     YES
       X on q2  s0=0 s1=1 -> q2                     YES
```

---

## Project 2: 3-Qubit Phase-Flip Code

| Feature | Description |
| :--- | :--- |
| **Goal** | Encode a logical qubit against $Z$ (phase-flip) errors using the dual block code: Hadamard-basis encoding and syndrome extraction. |
| **Circuit** | H-then-CNOT encoding transforms $X$ errors in the $\vert\pm\rangle$ basis; H-back maps phase to bit-flip syndrome. |
| **Method** | Inject $Z$ error on each qubit; confirm syndrome recovery. |

---

### Complete Python Code

```python
import numpy as np
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator

def phase_flip_code(error_qubit=None):
    qc = QuantumCircuit(5, 2)  # 3 data + 2 ancilla

    # ── encode ───────────────────────────────────────────────────────────────
    qc.ry(np.pi/4, 0)         # arbitrary logical state
    qc.cx(0, 1); qc.cx(0, 2)
    qc.h(0); qc.h(1); qc.h(2)  # rotate to +/- basis

    # ── inject Z error ────────────────────────────────────────────────────────
    if error_qubit is not None:
        qc.z(error_qubit)

    # ── decode back to computational basis ───────────────────────────────────
    qc.h(0); qc.h(1); qc.h(2)

    # ── syndrome: same parity checks as bit-flip ─────────────────────────────
    qc.cx(0, 3); qc.cx(1, 3)
    qc.cx(1, 4); qc.cx(2, 4)
    qc.measure(3, 0); qc.measure(4, 1)
    return qc

sim = AerSimulator()
cases = {None: "no error", 0: "Z on q0", 1: "Z on q1", 2: "Z on q2"}
syndrome_table = {"00": None, "01": 0, "11": 1, "10": 2}

print("Phase-flip code syndrome results:")
print(f"{'Case':>12}  {'Syndrome':>10}  {'Detected':>10}  {'Correct?':>10}")
for eq, label in cases.items():
    qc = phase_flip_code(eq)
    tc = transpile(qc, sim, optimization_level=0)
    res = sim.run(tc, shots=1024).result()
    top = max(res.get_counts(), key=res.get_counts().get)
    s0, s1 = int(top[1]), int(top[0])
    detected = syndrome_table.get(f"{s1}{s0}", "?")
    print(f"  {label:>12}  s={s1}{s0}        q{detected}  {'YES' if detected==eq else 'NO':>10}")
```
**Sample Output:**
```python
Phase-flip code syndrome results:
        Case    Syndrome    Detected    Correct?
      no error  s=00        qNone         YES
       Z on q0  s=01        q0         YES
       Z on q1  s=11        q1         YES
       Z on q2  s=10        q2         YES
```

---

## Project 3: Steane 7-Qubit Code (Encoding Circuit)

| Feature | Description |
| :--- | :--- |
| **Goal** | Construct the encoding circuit for the Steane [[7,1,3]] code and verify the encoded logical $\vert 0_L \rangle$ state satisfies all six stabiliser constraints. |
| **Method** | Build the 7-qubit encoding unitary from known CNOT pattern; project onto stabiliser subspace; check all six parity checks evaluate to $+1$. |

---

### Complete Python Code

```python
```python
import numpy as np
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector, SparsePauliOp

def steane_encode_zero():
```
    # Steane code encoding for |0_L> using standard generator matrix
    # Generator rows (G columns define CNOT targets):
    qc = QuantumCircuit(7)
    # Place H on qubits 4, 5, 6 (ancilla-like for encoding |0_L>)
    qc.h([4, 5, 6])
    # CNOT pattern derived from Steane generator matrix (H matrix of [7,4,3] Hamming code)
    # Row 4 (qubit 4): controls 0,2,4 (cols with 1s: 0,2,4,6 in H^T)
    qc.cx(4, 0); qc.cx(4, 2); qc.cx(4, 6)
    # Row 5 (qubit 5): controls 1,2,5
    qc.cx(5, 1); qc.cx(5, 2); qc.cx(5, 6)
    # Row 6 (qubit 6): controls 3,4,5,6
    qc.cx(6, 3); qc.cx(6, 4); qc.cx(6, 5); qc.cx(6, 6)
    return qc

qc = steane_encode_zero()
sv = Statevector(qc)
```python
print(f"Steane [[7,1,3]] encoded |0_L>:")
print(f"  Statevector norm: {np.linalg.norm(sv.data):.8f}")
```
# non-zero amplitudes

amps = sv.data
nonzero = [(format(i,'07b'), abs(a)) for i,a in enumerate(amps) if abs(a) > 1e-6]
```python
print(f"  Non-zero amplitude states ({len(nonzero)}):")
for bits, amp in sorted(nonzero, key=lambda x: -x[1]):
```
print(f"    |{bits}> : {amp:.6f}")

```
```
# ── verify X-type stabilisers (generators of Steane code) ────────────────────

# Steane X-stabilisers: X1X2X3X4, X1X2X5X6, X1X3X5X7 (1-indexed)

x_stabs = [
    "XXXX" + "I" * 3,   # positions 0-3
    "XX" + "I" * 2 + "XX" + "I",
    "X" + "I" + "X" + "I" + "X" + "I" + "X",
]
```python
print("\nX-stabiliser expectation values (should all be +1.0):")
for stab in x_stabs:
```
op  = SparsePauliOp.from_list([(stab, 1.0)]).to_matrix()
exp = float(np.real(sv.data.conj() @ op @ sv.data))
print(f"  {stab}: {exp:+.4f}")

```
```
## Notes For Chapter Bridge

# This chapter completes the quantum computing volume. Error correction closes

# the loop from physical noise (Chapter 19) to fault-tolerant logical operations,

# setting the stage for large-scale quantum advantage in future volumes.