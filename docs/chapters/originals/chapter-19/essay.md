# **Chapter 19: Quantum Hardware**

---

# **Introduction**

All quantum algorithms ultimately run on physical quantum hardware — systems where quantum information is encoded in the quantum states of real physical objects: superconducting circuits, trapped atomic ions, photons, or electron spins. Understanding the **physical implementation** of quantum computing is essential for any serious quantum programmer: the choice of hardware determines gate fidelity, qubit connectivity, coherence time, and the type of noise that must be managed. Without this physical grounding, quantum software development becomes an exercise in writing programs for imaginary computers.

This chapter focuses on the dominant quantum hardware platform of the current era: **superconducting qubits**, specifically the **transmon** architecture that underlies IBM Quantum, Google Sycamore, and most other leading processors. We develop the physics of the transmon qubit from its LC circuit origins, examine the **Josephson junction** that makes it anharmonic and therefore usable as a qubit, and connect this physical picture to the noise sources (T1, T2, gate errors) that define hardware performance. We then explore **hardware calibration workflows** using Qiskit's `FakeBackend` infrastructure and Qiskit Experiments for T1/T2 characterisation. The chapter closes by examining how **hardware topology** (qubit connectivity graphs) constrains circuit transpilation and why understanding the heavy-hex lattice is critical for writing efficient IBM Quantum programs [1, 2].

---

# **Chapter 19: Outline**

| **Sec.** | **Title** | **Core Ideas & Examples** |
| :--- | :--- | :--- |
| **19.1** | Superconducting Qubits and the Transmon | LC oscillator, Josephson junction, Cooper pairs, transmon anharmonicity |
| **19.2** | Decoherence and Noise: T1, T2, Gate Errors | Energy relaxation, dephasing, gate infidelity, noise model hierarchy |
| **19.3** | Hardware Calibration and Transpilation | FakeBackend properties, T1/T2 characterisation, heavy-hex topology, SABRE routing |

---

## **19.1 Superconducting Qubits and the Transmon**

---

Superconducting qubits exploit the quantum mechanical behaviour of **superconducting circuits** at millikelvin temperatures (~15 mK). The key insight is that a superconducting LC circuit — an inductor $L$ and capacitor $C$ — behaves as a quantum harmonic oscillator with discrete energy levels:

$$
E_n = \hbar\omega_0 \left(n + \frac{1}{2}\right), \quad \omega_0 = \frac{1}{\sqrt{LC}}
$$

However, a harmonic oscillator has **equally spaced energy levels**: since $E_{n+1} - E_n = \hbar\omega_0$ is constant, a microwave drive resonant with the $0 \to 1$ transition also drives the $1 \to 2$ transition. To define a two-level qubit, we need an **anharmonic** oscillator where only the $|0\rangle \leftrightarrow |1\rangle$ transition is addressable.

### **The Josephson Junction and Anharmonicity**

---

The anharmonicity is provided by the **Josephson junction** — a nanoscale break in the superconductor. The Josephson junction behaves as a nonlinear inductor with energy:

$$
E_J(\phi) = -E_J\cos\phi
$$

where $\phi$ is the superconducting phase difference across the junction and $E_J$ is the Josephson energy. The full transmon Hamiltonian is:

$$
H_{\text{transmon}} = 4E_C(n - n_g)^2 - E_J\cos\phi
$$

where $E_C = e^2/2C_\Sigma$ is the charging energy, $n$ is the Cooper pair number, and $n_g$ is the gate-induced offset charge.

The **anharmonicity** $\alpha = E_{12} - E_{01}$ (the difference in transition frequencies) for the transmon is:

$$
\alpha \approx -E_C \approx -200 \text{ to } -350 \text{ MHz}
$$

!!! tip "Why Transmon vs Cooper Pair Box?"
```
Early superconducting qubits (Cooper pair box) operated at $E_J/E_C \approx 1$, making them sensitive to charge noise. The transmon increases $E_J/E_C \gg 1$ (typically 50–100), dramatically reducing charge noise sensitivity at the cost of smaller anharmonicity. This is the dominant trade-off in transmon design.

```
### **Qubit Addressing and Control**

---

Each transmon connects to a **readout resonator** (for state measurement via dispersive coupling) and **control lines** (for microwave drive pulses). State readout is performed by measuring the dispersive shift of the resonator frequency:

$$
\omega_r^{\text{dressed}} = \omega_r \pm \frac{g^2}{\Delta} \quad (\text{sign depends on qubit state})
$$

where $g$ is the coupling strength and $\Delta = \omega_q - \omega_r$ is the qubit-resonator detuning. Single-qubit gates are implemented by microwave pulses at the qubit frequency; two-qubit gates (typically `CX` or `ECR` on IBM hardware) are implemented via cross-resonance driving.

!!! example "Cross-Resonance Gate"
```
IBM's native two-qubit gate is the **cross-resonance (CR) gate**: drive the control qubit at the *target* qubit's frequency. Due to the capacitive coupling between them, this creates an $IX$ interaction on the target qubit conditioned on the control state, forming the basis for constructing CNOT gates. CR gate durations are typically 300–500 ns on current IBM hardware.

```
??? question "Why must quantum hardware operate near absolute zero?"
```
At room temperature, thermal fluctuations have energy $k_BT \approx 25$ meV — far larger than the transmon qubit energy splitting $\hbar\omega_q \approx 15$ GHz $\approx 0.06$ meV. Thermal excitation would drive the qubit to a mixed state ($T = 15$ mK gives $k_BT \approx 0.001$ meV $\ll \hbar\omega_q$, yielding ground-state occupation $> 99\%$). The full cryostat (dilution refrigerator) maintains the chip temperature below 20 mK.

```
---

## **19.2 Decoherence and Noise: T1, T2, Gate Errors**

---

No quantum system is perfectly isolated. Interactions with the environment cause **decoherence** — the degradation of quantum coherence (superpositions and entanglement) into classical mixed states. The two fundamental decoherence timescales are $T_1$ (energy relaxation) and $T_2$ (phase decoherence).

### **Energy Relaxation: T₁**

---

**T₁** (longitudinal relaxation time, also called qubit lifetime) characterises the timescale for a qubit to spontaneously decay from $|1\rangle$ to $|0\rangle$ by emitting a photon to the environment:

$$
\langle Z(t) \rangle = 1 - 2e^{-t/T_1}
$$

A standard **T₁ experiment** prepares $|1\rangle$ with an X gate, waits for delay time $\tau$, and measures. The exponential decay gives $T_1$.

Typical T₁ values on current IBM Quantum hardware: **50–200 μs** (Eagle/Heron processors), with the record for a single qubit exceeding 1 ms.

### **Dephasing: T₂ and T₂\***

---

**T₂** (transverse relaxation, Hahn echo time) characterises the timescale for superposition phases to randomise, measured via a **Ramsey experiment** (with echo pulse) or **Hahn echo experiment**. The Ramsey decay is:

$$
\langle X(t) \rangle = e^{-t/T_2^*}\cos(\Delta\omega \cdot t)
$$

where $T_2^*$ is the free-induction decay time (without echo). The full T₂ (with echo) is always $T_2 \leq 2T_1$.

**Dephasing sources** on superconducting hardware:
1. **Flux noise** — fluctuations in residual magnetic field threading the qubit loop
2. **Charge noise** — two-level systems (TLS) in tunnel junction oxide
3. **Photon shot noise** — residual microwave photons in the readout resonator

!!! tip "T₁ vs T₂ for Circuit Depth Planning"
```
The maximum coherent circuit time is $\min(T_1, T_2)$. A single CNOT gate takes ~350 ns on IBM hardware; with $T_2 \approx 100$ μs, you can execute ~285 CNOT gates before 50% coherence loss. This sets a hard practical limit on NISQ algorithm depth.

```
### **Gate Errors and Error Hierarchy**

---

Hardware errors form a hierarchy by magnitude:

| Error Source | Typical Rate (IBM Eagle) | Origin |
| :--- | :--- | :--- |
| **Single-qubit gate** | 0.05%–0.1% | Pulse miscalibration, decoherence |
| **Two-qubit gate (CX)** | 0.5%–2% | Residual ZZ coupling, decoherence |
| **Readout** | 1%–3% | SNAIL asymmetry, measurement backaction |
| **Idle decoherence** | T-dependent | T1/T2 decay during wait time |

!!! example "Fidelity Budget for a VQE Circuit"
```
A 6-qubit VQE ansatz with 12 CNOT gates has a fidelity estimate:
$$F \approx (1 - p_{\text{sq}})^{N_{\text{sq}}} \times (1 - p_{\text{2q}})^{N_{2q}}$$
$$\approx (0.999)^{30} \times (0.99)^{12} \approx 0.97 \times 0.89 \approx 0.86$$
About 14% of circuit executions produce incorrect results — requiring many shots (typically 1000–10000) for reliable expectation value estimation.

```
??? question "What is ZZ coupling and why is it a major noise source?"
```
Adjacent transmon qubits, coupled via a capacitor or resonator bus, develop an **always-on ZZ (static ZZ) interaction** $H_{ZZ} = \xi Z_1 Z_2/4$ with strength $\xi \sim 1$–100 kHz. This causes a qubit's resonance frequency to shift depending on its neighbour's state, accumulating phase errors during idle times. Reducing ZZ coupling is a primary design focus of modern processors like IBM's Heron (using tunable couplers to turn off ZZ when not gating).

```
---

## **19.3 Hardware Calibration and Transpilation**

---

### **FakeBackend Properties and Noise Calibration**

---

Qiskit's `FakeBackend` provides a complete snapshot of a real device's calibration data, enabling hardware-realistic simulation without cloud access:

```python
from qiskit.providers.fake_provider import FakeNairobi

backend = FakeNairobi()
props = backend.properties()

# Print T1, T2, gate errors for each qubit
for i, qubit in enumerate(props.qubits):
    t1 = props.qubit_property(i, 'T1')[0] * 1e6  # convert to μs
    t2 = props.qubit_property(i, 'T2')[0] * 1e6
    err = props.gate_error('x', i)
    print(f"Q{i}: T1={t1:.0f}μs, T2={t2:.0f}μs, X-err={err:.4f}")
```

T1 characterisation circuit (Qiskit Experiments):
```python
from qiskit_experiments.library import T1

t1_exp = T1(physical_qubits=(0,), delays=[100e-9, 500e-9, 1e-6, 5e-6, 10e-6])
t1_data = t1_exp.run(backend).block_for_results()
print(t1_data.analysis_results("T1"))
```

### **IBM Heavy-Hex Topology**

---

IBM's heavy-hex coupling map is a degree-3 sparse graph where most qubits connect to at most 3 neighbours, minimising ZZ cross-talk:

```
Q0 — Q1 — Q2 — Q3 — Q4
|              |
Q5   Q6   Q7   Q8   Q9
     |              |
Q10 — Q11 — Q12 — Q13 ...
```

Circuits with non-adjacent qubit interactions require **SWAP routing** — inserting SWAP gates to move qubit states to adjacent physical locations. The routing problem is NP-hard in general; Qiskit uses the **SABRE heuristic** for near-optimal routing.

!!! tip "Map Algorithms to Heavy-Hex Early"
```
For CNOT-heavy algorithms, identify the logical CNOT pairs that dominate the circuit and map the most frequently interacting qubit pairs to physically adjacent qubits in the heavy-hex layout. This pre-layout step reduces SWAP overhead by 30–50% compared to default DenseLayout.

```
!!! example "Transpilation for Heavy-Hex: GHZ Circuit"
```
A 5-qubit GHZ circuit requires 4 logically ordered CNOTs. After SabreLayout on a 7-qubit FakeNairobi backend, the layout assigns qubits to maximise edge overlap with the heavy-hex graph, reducing required SWAP insertions from 2 (random layout) to 0 (optimal layout).

```
??? question "Why does IBM use a heavy-hex lattice rather than a full square grid?"
```
The heavy-hex lattice has a maximum qubit degree of 3 (vs 4 for a square grid and up to 25 for fully connected). Lower connectivity means fewer capacitive couplings per qubit, which reduces parasitic ZZ-type interactions between qubits that are not being operated on (crosstalk). The 50% reduction in crosstalk on heavy-hex vs square-grid layouts directly translates to lower error rates, compensating for the slightly higher SWAP overhead.

```
---

## **References**

[1] Koch, J., et al. (2007). *Charge-insensitive qubit design derived from the Cooper pair box*. Physical Review A, 76(4), 042319.

[2] Krantz, P., et al. (2019). *A quantum engineer's guide to superconducting qubits*. Applied Physics Reviews, 6(2), 021318.

[3] Li, G., et al. (2019). *Tackling the qubit mapping problem for NISQ-era quantum devices*. ASPLOS 2019.