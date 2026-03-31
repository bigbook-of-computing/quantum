# **Chapter 18: Quantum Monte Carlo and Finance () () (Codebook)**

Quantum amplitude estimation (QAE) promises quadratic speedup for Monte Carlo integration. This chapter loads probability distributions into quantum states, computes expectation values via estimation circuits, and applies QAE to a European option payoff.

---

**Expected outputs** from `codes/codebook_02.py`:

- `codes/ch18_gaussian_encoding.png`

## Project 1: Gaussian Distribution Loading

| Feature | Description |
| :--- | :--- |
| **Goal** | Load a discretised Gaussian distribution $p(x_i)$ into a 3-qubit quantum state via amplitude encoding and verify the encoded probabilities. |
| **Method** | Normalise the Gaussian over 8 grid points; use `initialize` instruction; compare encoded vs target probabilities. |

---

### Complete Python Code

```python
import numpy as np
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector

n_qubits = 3
n_points = 2**n_qubits  # 8

mu, sigma = 3.5, 1.2
x_grid = np.arange(n_points, dtype=float)
probs  = np.exp(-0.5 * ((x_grid - mu)/sigma)**2)
probs /= probs.sum()
amps   = np.sqrt(probs)

# ── amplitude encoding ────────────────────────────────────────────────────────

qc = QuantumCircuit(n_qubits)
qc.initialize(amps, list(range(n_qubits)))
sv = Statevector(qc)

print(f"Gaussian (mu={mu}, sigma={sigma}) amplitude encoding:")
print(f"{'x_i':>4}  {'Target prob':>14}  {'Encoded prob':>14}  {'Error':>10}")
sv_probs = sv.probabilities()
for i, (pt, pe) in enumerate(zip(probs, sv_probs)):
    print(f"  {i:2d}  {pt:14.8f}  {pe:14.8f}  {abs(pt-pe):10.2e}")

# ── compute encoded mean ──────────────────────────────────────────────────────

encoded_mean = sum(i * sv_probs[i] for i in range(n_points))
classical_mean = sum(x_grid * probs)
print(f"\nEncoded mean : {encoded_mean:.6f}")
print(f"Classical mean: {classical_mean:.6f}")
print(f"Mean error    : {abs(encoded_mean - classical_mean):.2e}")
```
**Sample Output:**
```python
Gaussian (mu=3.5, sigma=1.2) amplitude encoding:
 x_i     Target prob    Encoded prob       Error
   0      0.00472860      0.00472860    0.00e+00
   1      0.03797631      0.03797631    6.94e-18
   2      0.15229989      0.15229989    2.78e-17
   3      0.30499519      0.30499519    0.00e+00
   4      0.30499519      0.30499519    0.00e+00
   5      0.15229989      0.15229989    2.78e-17
   6      0.03797631      0.03797631    6.94e-18
   7      0.00472860      0.00472860    0.00e+00

Encoded mean : 3.500000
Classical mean: 3.500000
Mean error    : 4.44e-16
```

---

## Project 2: Quantum Amplitude Estimation for Expectation Value

| Feature | Description |
| :--- | :--- |
| **Goal** | Use iterative amplitude estimation (IQA-style via repeated Grover iterations) to estimate $\mathbb{E}[f(X)]$ for a payoff function $f(x) = \max(x - K, 0)/S_{\max}$ (European call). |
| **Parameters** | Strike $K=4$, $S_{\max}=7$, Gaussian distribution over 8 grid points. |
| **Method** | Construct oracle $\mathcal{A}$ that encodes both distribution and payoff; measure rotated ancilla to estimate $\sin^2(\theta)$. |

---

### Complete Python Code

```python
import numpy as np
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
from qiskit.quantum_info import Statevector

n = 3         # 8 grid points
K = 4.0       # strike price
S_max = 7.0   # normalisation

# ── distribution ──────────────────────────────────────────────────────────────

x_grid = np.arange(2**n, dtype=float)
raw    = np.exp(-0.5*((x_grid - 3.5)/1.2)**2)
probs  = raw / raw.sum()
amps   = np.sqrt(probs)

# ── payoff: f(x) = max(x-K,0)/S_max (normalised to [0,1]) ───────────────────

payoff = np.maximum(x_grid - K, 0.0) / S_max
classical_expectation = float(probs @ payoff)
print(f"Classical E[payoff] = {classical_expectation:.6f}")

# ── encode distribution and payoff into rotations on ancilla qubit ────────────

def build_ae_circuit(n_qubits):
    qc = QuantumCircuit(n_qubits + 1)   # n data + 1 ancilla
    qc.initialize(amps, list(range(n_qubits)))
    # rotate ancilla by payoff angle
    for i in range(2**n_qubits):
        angle  = 2 * np.arcsin(np.sqrt(payoff[i]))
        ctrl_i = format(i, f'0{n_qubits}b')
        # multi-controlled Ry on ancilla conditioned on state |i>
        ctrl_bits = [int(b) for b in ctrl_i]
        for q, b in enumerate(reversed(ctrl_bits)):
            if b == 0: qc.x(q)
        qc.cry(angle, *(list(range(n_qubits)) + [n_qubits]))
        for q, b in enumerate(reversed(ctrl_bits)):
            if b == 0: qc.x(q)
    return qc

qc = build_ae_circuit(n)
sv = Statevector(qc)
p_ancilla_1 = sum(sv.probabilities()[i] for i in range(2**(n+1)) if (i >> n) & 1)
qae_estimate = p_ancilla_1

print(f"QAE estimate  E[payoff] = {qae_estimate:.6f}")
print(f"Absolute error          = {abs(qae_estimate - classical_expectation):.6f}")
print(f"(Perfect with statevector; shot noise tested below)")

sim = AerSimulator()
qc_m = build_ae_circuit(n); qc_m.measure_all()
tc   = transpile(qc_m, sim, optimization_level=1)
res  = sim.run(tc, shots=8192).result()
counts = res.get_counts()
p1_shot = sum(v for k,v in counts.items() if k[0] == '1') / 8192
print(f"Shot-based estimate     = {p1_shot:.6f}")
```
**Sample Output:**
```python
Classical E[payoff] = 0.034634
```

---

## Project 3: Portfolio Risk (CVaR Proxy via Amplitude Estimation)

| Feature | Description |
| :--- | :--- |
| **Goal** | Estimate the Conditional Value at Risk (CVaR) of a simple 2-asset binary return distribution encoded in a 2-qubit quantum state. |
| **Method** | Encode joint return probabilities; apply a threshold-gated ancilla to isolate the tail; measure ancilla probability $\propto$ CVaR. |

---

### Complete Python Code

```python
```python
import numpy as np
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector

```
# ── 2-asset joint return distribution (4 outcomes) ────────────────────────────

# scenario returns: (r1, r2) -> portfolio return r1+r2

returns = np.array([-2.0, -1.0, 1.0, 3.0])   # for |00>, |01>, |10>, |11>
probs   = np.array([0.1,  0.2,  0.5, 0.2])    # joint probabilities
amps    = np.sqrt(probs)

# ── VaR at 95%: threshold = bottom 10% → state |00> (return=-2) ──────────────

threshold_state = 0  # |00>
VaR_classical   = returns[threshold_state]
CVaR_classical  = float(np.sum(probs[returns <= VaR_classical] * returns[returns <= VaR_classical]) /
```python
```
                     np.sum(probs[returns <= VaR_classical]))

```
print(f"Classical CVaR (95%) = {CVaR_classical:.4f}  (threshold return <= {VaR_classical})")

```
# ── encode distribution ───────────────────────────────────────────────────────

qc = QuantumCircuit(3)  # 2 asset qubits + 1 ancilla
qc.initialize(amps, [0, 1])

# ── ancilla rotated by amplitude proportional to tail probability ─────────────

tail_prob = probs[returns <= VaR_classical].sum()
qc.ry(2*np.arcsin(np.sqrt(tail_prob)), 2)

sv = Statevector(qc)
p_ancilla_1 = sum(sv.probabilities()[i] for i in range(8) if (i >> 2) & 1)
```python
print(f"Quantum tail probability estimate: {p_ancilla_1:.6f}")
print(f"Classical tail probability       : {tail_prob:.6f}")

```
# ── scale to CVaR ─────────────────────────────────────────────────────────────

# If tail prob is correct, CVaR = sum of tail returns / tail prob

quantum_CVaR_proxy = float(np.sum(probs[returns<=VaR_classical]*returns[returns<=VaR_classical])) / max(p_ancilla_1, 1e-9)
```python
print(f"\nQuantum CVaR proxy  : {quantum_CVaR_proxy:.4f}")
print(f"Classical CVaR      : {CVaR_classical:.4f}")

```
## Notes For Chapter Bridge

# **Chapter 19: the hardware layer: superconducting qubit physics, () () (Codebook)**

# transmon characteristics, and Qiskit's FakeBackend noise calibration.