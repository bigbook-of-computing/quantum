# **Chapter 16: Quantum Simulators vs Real Devices () () (Codebook)**

Bridging ideal simulation and hardware execution requires understanding decoherence, gate errors, and readout noise. This chapter compares ideal and noisy Aer simulations, models realistic T1/T2 noise, and applies zero-noise extrapolation (ZNE).

---

**Expected outputs** from `codes/codebook_02.py`:

- `codes/ch16_noise_fidelity.png`

## Project 1: Ideal vs Shot-Noise Simulation

| Feature | Description |
| :--- | :--- |
| **Goal** | Compare statevector (exact) probabilities with shot-based measurement statistics for a 3-qubit GHZ circuit at varying shot counts. |
| **Method** | Statevector exact probabilities; then sampling at `shots` $\in \{32, 256, 2048, 16384\}$; compute total variation distance. |

---

### Complete Python Code

```python
import numpy as np
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
from qiskit.quantum_info import Statevector

# ── GHZ circuit ───────────────────────────────────────────────────────────────
def ghz_circuit(n):
    qc = QuantumCircuit(n)
    qc.h(0)
    for i in range(n-1):
        qc.cx(i, i+1)
    return qc

n = 3
qc_ideal = ghz_circuit(n)
sv_exact  = Statevector(qc_ideal).probabilities_dict()
print("Exact probabilities:")
for k, v in sorted(sv_exact.items()):
    print(f"  |{k}>  {v:.6f}")

# ── shot-based simulation ─────────────────────────────────────────────────────
sim    = AerSimulator()
qc_meas = ghz_circuit(n)
qc_meas.measure_all()
tc = transpile(qc_meas, sim, optimization_level=0)

print(f"\n{'Shots':>8}  {'TVD':>12}")
for shots in [32, 256, 2048, 16384]:
    result = sim.run(tc, shots=shots).result()
    counts = result.get_counts()
    total  = sum(counts.values())
    emp_p  = {k: v/total for k, v in counts.items()}
    # total variation distance
    all_keys = set(sv_exact.keys()) | set(emp_p.keys())
    tvd = 0.5 * sum(abs(sv_exact.get(k,0) - emp_p.get(k,0)) for k in all_keys)
    print(f"  {shots:6d}  {tvd:12.6f}")
```
**Sample Output:**
```
Exact probabilities:
  |000>  0.500000
  |111>  0.500000

   Shots           TVD
      32      0.031250
     256      0.046875
    2048      0.020996
   16384      0.005493
```

---

## Project 2: Depolarising and T1/T2 Noise Models

| Feature | Description |
| :--- | :--- |
| **Goal** | Simulate a Bell-state circuit under (a) depolarising noise only and (b) combined depolarising + amplitude damping ($T_1/T_2$ model) and compare output fidelity. |
| **Method** | Build `NoiseModel` with `depolarizing_error` and `thermal_relaxation_error`; measure output density-matrix fidelity vs ideal Bell state. |

---

### Complete Python Code

```python
import numpy as np
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
from qiskit_aer.noise import NoiseModel, depolarizing_error, thermal_relaxation_error
from qiskit.quantum_info import Statevector, DensityMatrix, state_fidelity

def bell_circuit():
    qc = QuantumCircuit(2)
    qc.h(0); qc.cx(0, 1)
    return qc

ideal_sv = Statevector(bell_circuit())

configs = [
    ("Ideal (no noise)",    None),
    ("Depolarising p=0.01", "dep"),
    ("T1/T2 + dep",         "t1t2"),
]

for label, noise_type in configs:
    nm = NoiseModel()
    if noise_type == "dep":
        nm.add_all_qubit_quantum_error(depolarizing_error(0.01, 1), ['u1','u2','u3','h'])
        nm.add_all_qubit_quantum_error(depolarizing_error(0.02, 2), ['cx'])
    elif noise_type == "t1t2":
        t1, t2, tg1, tg2 = 50e3, 30e3, 50, 100  # ns
        err1 = thermal_relaxation_error(t1, t2, tg1)
        err2 = thermal_relaxation_error(t1, t2, tg2).expand(
               thermal_relaxation_error(t1, t2, tg2))
        nm.add_all_qubit_quantum_error(err1, ['u1','u2','u3','h'])
        nm.add_all_qubit_quantum_error(
            err2.compose(depolarizing_error(0.015, 2)), ['cx'])

    sim_args = {'method': 'density_matrix'}
    if noise_type:
        sim_args['noise_model'] = nm
    sim = AerSimulator(**sim_args)

    qc = bell_circuit(); qc.save_density_matrix()
    tc = transpile(qc, sim)
    dm  = DensityMatrix(sim.run(tc, shots=1).result().data()['density_matrix'])
    fid = state_fidelity(dm, ideal_sv)
    print(f"{label:<30}  fidelity = {fid:.6f}")
```
**Sample Output:**
```
Ideal (no noise)                fidelity = 1.000000
Depolarising p=0.01             fidelity = 0.980100
T1/T2 + dep                     fidelity = 0.983682
```

---

## Project 3: Zero-Noise Extrapolation (ZNE)

| Feature | Description |
| :--- | :--- |
| **Goal** | Mitigate gate errors via ZNE: run a noisy circuit at noise scale factors $c \in \{1, 2, 3\}$ by repeating gate pairs, then extrapolate to $c=0$. |
| **Circuit** | 2-qubit `ZZ` rotation circuit ($R_{ZZ}(\theta)$ via CNOT + $R_Z$). |
| **Method** | Richardson extrapolation using 3 noise-scaled expectation values $\langle Z \rangle_{c=1,2,3}$. |

---

### Complete Python Code

```python
```python
import numpy as np
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
from qiskit_aer.noise import NoiseModel, depolarizing_error
from qiskit.quantum_info import SparsePauliOp

def rzz_circuit(theta, noise_scale=1):
```
    # R_ZZ(theta) = CNOT . Rz(theta) . CNOT
    # Noise folding: repeat CNOT-Rz-CNOT 'noise_scale' times (odd multiples)
    qc = QuantumCircuit(2)
    qc.h(0)
    for _ in range(noise_scale):
        qc.cx(0, 1)
        qc.rz(theta / noise_scale, 1)
        qc.cx(0, 1)
    qc.h(0)
    return qc

# ── noisy simulator ───────────────────────────────────────────────────────────
p_dep = 0.03
nm = NoiseModel()
nm.add_all_qubit_quantum_error(depolarizing_error(p_dep, 2), ['cx'])
nm.add_all_qubit_quantum_error(depolarizing_error(p_dep/3, 1), ['h','rz'])
sim = AerSimulator(noise_model=nm)

obs_mat = SparsePauliOp.from_list([("IZ", 1.0)]).to_matrix()
theta   = np.pi / 3

```python
def noisy_expectation(scale, shots=4096):
```
qc = rzz_circuit(theta, noise_scale=scale)
qc.save_statevector()
```
```
    # Use density_matrix so noise is applied
    sim2 = AerSimulator(noise_model=nm, method='density_matrix')
    qc2  = rzz_circuit(theta, noise_scale=scale)
    qc2.save_density_matrix()
    tc   = transpile(qc2, sim2)
    dm   = sim2.run(tc, shots=1).result().data()['density_matrix']
    dm_np = np.array(dm)
    return float(np.real(np.trace(dm_np @ obs_mat)))

# ── ideal value ───────────────────────────────────────────────────────────────
```python
from qiskit.quantum_info import Statevector, DensityMatrix
ideal_sv  = Statevector(rzz_circuit(theta, noise_scale=1))
e_ideal   = float(np.real(ideal_sv.data.conj() @ obs_mat @ ideal_sv.data))

scales  = [1, 2, 3]
e_vals  = [noisy_expectation(s) for s in scales]

```
# ── Richardson extrapolation ──────────────────────────────────────────────────
c = np.array(scales, float)
A = np.vstack([c**0, c**1, c**2]).T
zne_coeffs = np.linalg.solve(A, np.array([1.0, 0.0, 0.0]))
e_zne = float(zne_coeffs @ np.array(e_vals))

```python
print(f"Ideal expectation <IZ>     : {e_ideal:.6f}")
print(f"Noisy scale c=1            : {e_vals[0]:.6f}")
print(f"Noisy scale c=2            : {e_vals[1]:.6f}")
print(f"Noisy scale c=3            : {e_vals[2]:.6f}")
print(f"ZNE extrapolated (c->0)    : {e_zne:.6f}")
print(f"ZNE error vs ideal         : {abs(e_zne - e_ideal):.6f}")

```
## Notes For Chapter Bridge
# **Chapter 17: to quantum chemistry: encoding fermionic Hamiltonians () () (Codebook)**
# via Jordan-Wigner and simulating molecular ground states with VQE.