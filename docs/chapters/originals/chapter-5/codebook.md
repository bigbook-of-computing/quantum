# **Chapter 5: Quantum Fourier Transform and Phase Estimation () () (Codebook)**

Three self-contained projects build the QFT from scratch, verify it analytically, and then use it inside Quantum Phase Estimation (QPE). All code uses Qiskit 2.x statevector and shot-based simulation.

---

**Expected outputs** from `codes/codebook_02.py`:

- `codes/ch5_qft_histogram.png`

## Project 1: Manual QFT vs Qiskit Built-in

| Feature | Description |
| :--- | :--- |
| **Goal** | Construct the $n$-qubit QFT manually (controlled-phase rotations + SWAP network) and compare output statevectors against `qiskit.circuit.library.QFT`. |
| **Method** | `state_fidelity` between manual and library circuits for each computational basis input. |

---

### Complete Python Code

```python
import numpy as np
from qiskit import QuantumCircuit
from qiskit.circuit.library import QFT
from qiskit.quantum_info import Statevector, state_fidelity

def qft_manual(n):
    # Build n-qubit QFT: controlled-phase rotations + bit-reversal swaps
    qc = QuantumCircuit(n)
    for j in range(n):
        qc.h(j)
        for k in range(j + 1, n):
            angle = 2 * np.pi / (2 ** (k - j + 1))
            qc.cp(angle, k, j)
    for i in range(n // 2):
        qc.swap(i, n - 1 - i)
    return qc

n = 3
qft_lib = QFT(n, do_swaps=True, inverse=False)

print(f"{'Input':>10}  {'Fidelity (manual vs library)':>30}")
print("-" * 44)
for j in range(2**n):
    # Prepare basis state |j>
    init = QuantumCircuit(n)
    for bit in range(n):
        if (j >> bit) & 1:
            init.x(bit)
    qc_m = init.compose(qft_manual(n))
    qc_l = init.compose(qft_lib)
    sv_m = Statevector.from_instruction(qc_m)
    sv_l = Statevector.from_instruction(qc_l)
    fid  = state_fidelity(sv_m, sv_l)
    print(f"|{j}> = |{format(j, f'0{n}b')}> fidelity = {fid:.10f}")

# QFT amplitudes for |1> on 4 qubits
print("\nQFT|1> amplitudes (n=4):")
n4   = 4
init = QuantumCircuit(n4)
init.x(0)                          # |0001> = |1>
qc4  = init.compose(qft_manual(n4))
sv4  = Statevector.from_instruction(qc4)
for k, amp in enumerate(sv4.data):
    print(f"  |{k:2d}>  amp={amp:.4f}  phase={np.angle(amp):.4f} rad")
```
**Sample Output:**
```
Input    Fidelity (manual vs library)

---

|0> = |000> fidelity = 1.0000000000
|1> = |001> fidelity = 0.4267766953
|2> = |010> fidelity = 0.2500000000
|3> = |011> fidelity = 0.0366116524
|4> = |100> fidelity = 0.4267766953
|5> = |101> fidelity = 0.7285533906
|6> = |110> fidelity = 0.0366116524
|7> = |111> fidelity = 0.0214466094

QFT|1> amplitudes (n=4):
  | 0>  amp=0.2500+0.0000j  phase=0.0000 rad
  | 1>  amp=0.2500+0.0000j  phase=0.0000 rad
  | 2>  amp=0.2500+0.0000j  phase=0.0000 rad
  | 3>  amp=0.2500+0.0000j  phase=0.0000 rad
  | 4>  amp=0.2500+0.0000j  phase=0.0000 rad
  | 5>  amp=0.2500+0.0000j  phase=0.0000 rad
  | 6>  amp=0.2500+0.0000j  phase=0.0000 rad
  | 7>  amp=0.2500+0.0000j  phase=0.0000 rad
  | 8>  amp=-0.2500+0.0000j  phase=3.1416 rad
  | 9>  amp=-0.2500+0.0000j  phase=3.1416 rad
  |10>  amp=-0.2500+0.0000j  phase=3.1416 rad
  |11>  amp=-0.2500+0.0000j  phase=3.1416 rad
  |12>  amp=-0.2500+0.0000j  phase=3.1416 rad
  |13>  amp=-0.2500+0.0000j  phase=3.1416 rad
  |14>  amp=-0.2500+0.0000j  phase=3.1416 rad
  |15>  amp=-0.2500+0.0000j  phase=3.1416 rad
```

---

## Project 2: Inverse QFT for Period Finding (Conceptual Core of Shor)

| Feature | Description |
| :--- | :--- |
| **Goal** | Encode a quantum state with period $r$ in its phase structure and recover the frequency $N/r$ via the inverse QFT, demonstrating the conceptual core of Shor's algorithm. |
| **Method** | Manual phase injection + `QFT(inverse=True)`; shot-based histogram. |

---

### Complete Python Code

```python
import numpy as np
from qiskit import QuantumCircuit
from qiskit.circuit.library import QFT
from qiskit_aer import AerSimulator
import matplotlib.pyplot as plt

def periodic_state(n_qubits, period):
    # Uniform superposition over multiples of period
    N    = 2 ** n_qubits
    amps = np.zeros(N, dtype=complex)
    cnt  = 0
    for k in range(N):
        if k % period == 0:
            amps[k] = 1.0
            cnt += 1
    amps /= np.sqrt(cnt)
    return amps

backend = AerSimulator()

for n, period in [(4, 4), (4, 2), (5, 8)]:
    N    = 2 ** n
    amps = periodic_state(n, period)
    qc   = QuantumCircuit(n, n)
    qc.initialize(amps, range(n))
    qc.compose(QFT(n, inverse=True), inplace=True)
    qc.measure(range(n), range(n))

    counts       = backend.run(qc, shots=8192).result().get_counts()
    exp_peak     = N // period
    print(f"\nn={n}  N={N}  period={period}  expected frequency peak = {exp_peak}")
    top = sorted(counts.items(), key=lambda x: -x[1])[:4]
    for bits, cnt in top:
        freq = int(bits[::-1], 2)    # Qiskit LSB ordering
        tag  = "<-- expected peak" if freq % exp_peak == 0 else ""
        print(f"  |{bits}> freq={freq:3d}  count={cnt:5d}  {tag}")
```

---

## Project 3: Quantum Phase Estimation

| Feature | Description |
| :--- | :--- |
| **Goal** | Estimate the phase $\varphi$ of eigenvalue $e^{2\pi i \varphi}$ of a unitary $U$ with $t$ precision bits. Test $U = T$ (phase $1/8$), $U = S$ (phase $1/4$), $U = Z$ (phase $1/2$). |
| **Method** | Standard QPE circuit: $t$ ancilla qubits, controlled-$U^{2^k}$, inverse QFT. |

---

### Complete Python Code

```python
import numpy as np
from qiskit import QuantumCircuit
from qiskit.circuit.library import QFT
from qiskit_aer import AerSimulator

def qpe_circuit(gate_name, t):
    # Eigenvector |1> works for T, S, Z gates
    qc = QuantumCircuit(t + 1, t)
    qc.x(t)                        # target register in |1>
    qc.h(range(t))
    for k in range(t):
        reps = 2 ** k
        for _ in range(reps):
            if gate_name == "t":
                qc.cp(2 * np.pi / 8, k, t)
            elif gate_name == "s":
                qc.cp(2 * np.pi / 4, k, t)
            elif gate_name == "z":
                qc.cp(2 * np.pi / 2, k, t)
    qc.compose(QFT(t, inverse=True), qubits=range(t), inplace=True)
    qc.measure(range(t), range(t))
    return qc

backend = AerSimulator()
t = 5           # 5 bits -> resolution 1/32

tests = [
    ("t", 1/8,  "T gate  (phi=1/8)"),
    ("s", 1/4,  "S gate  (phi=1/4)"),
    ("z", 1/2,  "Z gate  (phi=1/2)"),
]

print(f"{'Gate':<22}  {'True phi':>8}  {'Estimated phi':>14}  {'Error':>8}")
print("-" * 58)
for gate, true_phi, label in tests:
    qc      = qpe_circuit(gate, t)
    counts  = backend.run(qc, shots=4096).result().get_counts()
    best    = max(counts, key=counts.get)
    measured = int(best[::-1], 2)        # Qiskit LSB
    est_phi  = measured / (2 ** t)
    error    = abs(est_phi - true_phi)
    print(f"{label:<22}  {true_phi:>8.5f}  {est_phi:>14.5f}  {error:>8.1e}")

print(f"\nResolution with t={t}: 1/{2**t} = {1/(2**t):.5f}")
```
**Sample Output:**
```
Gate                    True phi   Estimated phi     Error

---

```

---

## Notes For Chapter Bridge

QPE is the exact phase-reading subroutine. Chapter 6 introduces variational algorithms (VQE, QAOA) that bypass QPE entirely by replacing exact phase calculation with classical optimisation, trading precision for hardware efficiency on near-term devices.