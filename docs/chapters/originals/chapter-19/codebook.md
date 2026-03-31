# **Chapter 19: Superconducting Qubits and Hardware () () (Codebook)**

Superconducting qubits are the dominant hardware platform for near-term quantum computers. This chapter explores FakeBackend device properties, transpilation for real connectivity, and custom noise models that replicate T1/T2 decoherence observed in real devices.

---

**Expected outputs** from `codes/codebook_02.py`:

- `codes/ch19_decoherence.png`

## Project 1: FakeBackend Device Properties

| Feature | Description |
| :--- | :--- |
| **Goal** | Load a FakeBackend (simulated 5-qubit device), inspect coupling map, qubit frequencies, T1/T2 times, and gate error rates. |
| **Method** | Use `qiskit_aer.primitives` FakeBackend; print properties table. |

---

### Complete Python Code

```python
import numpy as np
from qiskit_aer import AerSimulator
from qiskit_aer.noise import NoiseModel

# ── build a representative 5-qubit noise model (IBM Ourense-like params) ──────
# T1/T2 times (ns), gate times (ns), error rates
t1_times  = [54_000, 63_000, 45_000, 50_000, 72_000]   # T1 per qubit
t2_times  = [28_000, 35_000, 22_000, 30_000, 40_000]   # T2 per qubit
t1_gate   = 50      # single-qubit gate time (ns)
t2_gate   = 300     # two-qubit gate time (ns)
readout_p = [0.02, 0.03, 0.04, 0.025, 0.015]           # readout error per qubit

from qiskit_aer.noise import (thermal_relaxation_error, ReadoutError,
                               depolarizing_error)

nm = NoiseModel()
coupling = [(0,1),(1,2),(2,3),(3,4)]

for q in range(5):
    # single-qubit thermal relaxation
    err1 = thermal_relaxation_error(t1_times[q], t2_times[q], t1_gate)
    nm.add_quantum_error(err1, ['h','u1','u2','u3','rx','ry','rz'], [q])
    # readout
    p0g1 = readout_p[q]; p1g0 = readout_p[q] / 2
    re   = ReadoutError([[1-p0g1, p0g1], [p1g0, 1-p1g0]])
    nm.add_readout_error(re, [q])

for q1, q2 in coupling:
    err2 = (thermal_relaxation_error(t1_times[q1], t2_times[q1], t2_gate)
            .expand(thermal_relaxation_error(t1_times[q2], t2_times[q2], t2_gate)))
    err2 = err2.compose(depolarizing_error(0.01, 2))
    nm.add_quantum_error(err2, ['cx'], [q1, q2])

print("Custom 5-qubit device noise model (IBM-like parameters):")
print(f"  Qubits     : 5")
print(f"  Coupling   : {coupling}")
print(f"\n  {'Qubit':>6}  {'T1 (us)':>10}  {'T2 (us)':>10}  {'Readout err':>12}")
for q in range(5):
    print(f"  {q:6d}  {t1_times[q]/1000:10.1f}  {t2_times[q]/1000:10.1f}  {readout_p[q]:12.4f}")

sim = AerSimulator(noise_model=nm)
print(f"\nAerSimulator with custom noise model ready: {sim.name}")
```
**Sample Output:**
```
Custom 5-qubit device noise model (IBM-like parameters):
  Qubits     : 5
  Coupling   : [(0, 1), (1, 2), (2, 3), (3, 4)]

   Qubit     T1 (us)     T2 (us)   Readout err
       0        54.0        28.0        0.0200
       1        63.0        35.0        0.0300
       2        45.0        22.0        0.0400
       3        50.0        30.0        0.0250
       4        72.0        40.0        0.0150

AerSimulator with custom noise model ready: aer_simulator
```

---

## Project 2: Transpilation for Heavy-Hex Connectivity

| Feature | Description |
| :--- | :--- |
| **Goal** | Transpile a 4-qubit circuit with all-to-all gates onto a linear 4-qubit coupling map (mimicking sparse hardware topology) and measure SWAP overhead. |
| **Method** | Create a circuit requiring non-adjacent 2-qubit gates; transpile at level 3; count SWAP gates inserted. |

---

### Complete Python Code

```python
import numpy as np
from qiskit import QuantumCircuit, transpile
from qiskit.transpiler import CouplingMap

# ── circuit requiring non-adjacent gates ─────────────────────────────────────
qc = QuantumCircuit(4)
qc.h(range(4))
qc.cx(0, 3)  # long-range: skip 2 nodes on linear chain
qc.cx(1, 3)  # also non-adjacent
qc.rz(0.5, 2)
qc.cx(0, 2)
qc.cx(1, 3)
qc.measure_all()

print("Original circuit gate counts:", dict(qc.count_ops()))

# ── linear coupling: 0-1-2-3 ─────────────────────────────────────────────────
linear_coupling = CouplingMap([[0,1],[1,0],[1,2],[2,1],[2,3],[3,2]])

for opt_level in [0, 1, 2, 3]:
    tc = transpile(qc, coupling_map=linear_coupling,
                   basis_gates=['cx','u3','measure','barrier'],
                   optimization_level=opt_level)
    ops   = dict(tc.count_ops())
    n_cx  = ops.get('cx', 0)
    depth = tc.depth()
    swaps = max(0, (n_cx - 5) // 3)  # each SWAP = 3 CX; estimate
    print(f"  opt={opt_level}: depth={depth:3d}  CX={n_cx:3d}  est. SWAPs={swaps}")

print("\nHigher optimisation levels reduce SWAP overhead.")
print("Real hardware routing adds SWAP gates for non-adjacent qubits.")
```
**Sample Output:**
```
Original circuit gate counts: {'h': 4, 'cx': 4, 'measure': 4, 'rz': 1, 'barrier': 1}
```

---

## Project 3: T1/T2 Decoherence Characterisation

| Feature | Description |
| :--- | :--- |
| **Goal** | Simulate T1 (energy relaxation) and T2 (dephasing) decay curves for a single qubit using Aer density-matrix simulation with thermal relaxation. |
| **Method** | Prepare $\vert 1 \rangle$ (T1) and $\vert + \rangle$ (T2); apply identity delay; measure $\langle Z \rangle$ vs delay time. |

---

### Complete Python Code

```python
```python
import numpy as np
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
from qiskit_aer.noise import NoiseModel, thermal_relaxation_error
from qiskit.quantum_info import DensityMatrix

T1 = 50_000   # ns
T2 = 25_000   # ns
delay_times = np.linspace(0, 100_000, 15)   # ns

print(f"T1 decay (|1> -> |0>):  T1={T1/1000:.0f} us")
print(f"{'Delay (us)':>12}  {'<Z>_T1':>10}  {'Analytic':>10}")
for t in delay_times:
```
nm = NoiseModel()
err = thermal_relaxation_error(T1, T2, t)
nm.add_all_qubit_quantum_error(err, ['id'])

qc = QuantumCircuit(1)
qc.x(0)        # prepare |1>
qc.id(0)       # delay gate (noise applied here)
qc.save_density_matrix()

sim = AerSimulator(noise_model=nm, method='density_matrix')
tc  = transpile(qc, sim)
dm  = np.array(sim.run(tc, shots=1).result().data()['density_matrix'])
z   = float(np.real(dm[0,0] - dm[1,1]))   # <Z> = rho_00 - rho_11
analytic = -np.exp(-t/T1)
if t == 0 or t > 85_000 or t % 15000 < 8000:
    print(f"  {t/1000:10.1f}  {z:10.6f}  {analytic:10.6f}")

```
print("\nT2 Ramsey decay (|+> dephasing): T2 =", T2/1000, "us")
print(f"{'Delay (us)':>12}  {'<X>_T2':>10}  {'Analytic':>10}")
for t in delay_times:
```
nm = NoiseModel()
nm.add_all_qubit_quantum_error(thermal_relaxation_error(T1, T2, t), ['id'])
qc = QuantumCircuit(1)
qc.h(0)        # prepare |+>
qc.id(0)       # delay
qc.h(0)        # rotate back
qc.save_density_matrix()
sim = AerSimulator(noise_model=nm, method='density_matrix')
tc  = transpile(qc, sim)
dm  = np.array(sim.run(tc, shots=1).result().data()['density_matrix'])
x   = float(np.real(dm[0,0] - dm[1,1]))
analytic = np.exp(-t/T2)
if t == 0 or t > 85_000 or t % 15000 < 8000:
    print(f"  {t/1000:10.1f}  {x:10.6f}  {analytic:10.6f}")

```
```
## Notes For Chapter Bridge
# **Chapter 20: on the hardware model to study quantum error correction: () () (Codebook)**
# syndrome detection, logical qubit encoding, and fault-tolerant operations.