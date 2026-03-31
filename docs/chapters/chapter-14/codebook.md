# **Chapter 14: Quantum Optimization — QUBO and QAOA (Codebook)**

Quantum optimisation targets NP-hard combinatorial problems by encoding them as Ising Hamiltonians. This chapter covers QUBO problem formulation, the Quantum Approximate Optimization Algorithm (QAOA), and Grover adaptive search for binary optimisation.

---

**Expected outputs** from `codes/codebook_02.py`:

- `codes/ch14_qaoa_histogram.png`

## Project 1: QUBO MaxCut Formulation and Cost Evaluation

| Feature | Description |
| :--- | :--- |
| **Goal** | Formulate MaxCut for a 4-node graph as a QUBO cost function and evaluate the cost for all $2^4 = 16$ binary assignments using Qiskit. |
| **Graph** | 4 nodes, edges: $(0,1),(1,2),(2,3),(0,3),(0,2)$. |
| **Method** | Build `SparsePauliOp` cost Hamiltonian $H_C$; evaluate $\langle z \vert H_C \vert z \rangle$ for each basis state. |

---

### Complete Python Code

```python
import numpy as np
from qiskit.quantum_info import SparsePauliOp, Statevector
from qiskit import QuantumCircuit

n_qubits = 4
edges    = [(0,1),(1,2),(2,3),(0,3),(0,2)]

# ── MaxCut cost: H_C = 0.5 * sum_{(i,j)} (I - Z_i Z_j) ─────────────────────

terms = []
for i, j in edges:
    pauli_str  = ['I'] * n_qubits
    pauli_str[i] = 'Z'; pauli_str[j] = 'Z'
    terms.append((''.join(reversed(pauli_str)), -0.5))  # Z_i Z_j
    terms.append(('I'*n_qubits,                  0.5))  # +0.5 offset

H_C = SparsePauliOp.from_list(terms)
H_mat = H_C.to_matrix().real

print(f"MaxCut cost Hamiltonian (diagonal entries = cut cost per basis state)")
print(f"{'State':>8}  {'Bitstring':>10}  {'Cut value':>12}")
best_cut, best_state = 0, 0
for s in range(2**n_qubits):
    bits = format(s, f'0{n_qubits}b')
    # evaluation: diagonal of Hamiltonian
    cost = H_mat[s, s]
    if cost > best_cut:
        best_cut, best_state = cost, bits
    marker = " <-- best" if bits == best_state and cost == best_cut else ""
    print(f"  {s:6d}  {bits:>10}  {cost:12.2f}{marker}")

print(f"\nOptimal cut = {best_cut} at bitstring {best_state}")
print(f"Number of edges = {len(edges)}  (max possible cut = {len(edges)})")
```
**Sample Output:**
```python
MaxCut cost Hamiltonian (diagonal entries = cut cost per basis state)
   State   Bitstring     Cut value
       0        0000          0.00
       1        0001          3.00 <-- best
       2        0010          2.00
       3        0011          3.00
       4        0100          3.00
       5        0101          4.00 <-- best
       6        0110          3.00
       7        0111          2.00
       8        1000          2.00
       9        1001          3.00
      10        1010          4.00
      11        1011          3.00
      12        1100          3.00
      13        1101          2.00
      14        1110          3.00
      15        1111          0.00

Optimal cut = 4.0 at bitstring 0101
Number of edges = 5  (max possible cut = 5)
```

---

## Project 2: QAOA on a 4-Node Graph

| Feature | Description |
| :--- | :--- |
| **Goal** | Run QAOA with $p=2$ layers on the same MaxCut graph and recover a near-optimal partition. |
| **Circuit** | Phase-separation unitary $U(H_C, \gamma)$ and mixing unitary $U(H_B, \beta)$ with $X$ mixers. |
| **Method** | Parameter sweep over $(\gamma, \beta) \in [0, \pi] \times [0, \pi]$; extract best measurement outcome. |

---

### Complete Python Code

```python
import numpy as np
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator

n_qubits = 4
edges    = [(0,1),(1,2),(2,3),(0,3),(0,2)]

def build_qaoa(gamma_list, beta_list):
    qc = QuantumCircuit(n_qubits)
    qc.h(range(n_qubits))
    for gamma, beta in zip(gamma_list, beta_list):
        # phase separator
        for i, j in edges:
            qc.cx(i, j)
            qc.rz(2*gamma, j)
            qc.cx(i, j)
        # mixer
        for q in range(n_qubits):
            qc.rx(2*beta, q)
    qc.measure_all()
    return qc

sim     = AerSimulator()
n_shots = 2048

# ── 2-layer QAOA: sweep gamma1 and beta1 (fix gamma2=0.4, beta2=0.3) ─────────

best_energy = -np.inf
best_params = (0, 0)
best_counts = {}

for g1 in np.linspace(0.1, np.pi, 8):
    for b1 in np.linspace(0.1, np.pi, 8):
        qc = build_qaoa([g1, 0.4], [b1, 0.3])
        tc = transpile(qc, sim, optimization_level=1)
        result  = sim.run(tc, shots=n_shots).result()
        counts  = result.get_counts()
        # estimate energy as weighted average of cut values
        energy = 0.0
        def cut_value(bits):
            return sum(bits[i] != bits[j] for i,j in edges)
        for bits, cnt in counts.items():
            energy += cut_value(bits) * cnt / n_shots
        if energy > best_energy:
            best_energy = energy
            best_params = (g1, b1)
            best_counts = counts

print(f"Best QAOA energy (p=2): {best_energy:.4f}  params: gamma={best_params[0]:.3f} beta={best_params[1]:.3f}")
top5 = sorted(best_counts.items(), key=lambda x: -x[1])[:5]
print("\nTop-5 output bitstrings:")
for bits, cnt in top5:
    cv = sum(bits[i] != bits[j] for i,j in edges)
    print(f"  |{bits}>  count={cnt:5d}  cut={cv}")
```
**Sample Output:**
```python
Best QAOA energy (p=2): 3.2134  params: gamma=2.273 beta=1.404

Top-5 output bitstrings:
  |0101>  count=  504  cut=4
  |1010>  count=  470  cut=4
  |1001>  count=  179  cut=3
  |1100>  count=  168  cut=3
  |0110>  count=  165  cut=3
```

---

## Project 3: Grover Adaptive Search for Binary QUBO

| Feature | Description |
| :--- | :--- |
| **Goal** | Use Grover amplification to search for the bit-string minimising a 4-variable QUBO objective $f(x) = x^T Q x$ where $Q$ is a random symmetric matrix. |
| **Oracle** | A phase-kickback oracle that tags all bitstrings with $f(x) < $ threshold using a classical comparison encoded in the circuit. |
| **Method** | Enumerate exhaustively (exact for 4 bits), then confirm Grover angles amplify the optimal states. |

---

### Complete Python Code

```python
```python
import numpy as np
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator

np.random.seed(42)
n = 4
```
# random symmetric QUBO matrix

Q_raw = np.random.randn(n, n)
Q     = (Q_raw + Q_raw.T) / 2

```python
def qubo_val(x_bits):
```
x = np.array([int(b) for b in x_bits], float)
return float(x @ Q @ x)

```
```
# ── enumerate all 2^n states ─────────────────────────────────────────────────

vals = {}
for s in range(2**n):
    bits = format(s, f'0{n}b')
    vals[bits] = qubo_val(bits)

optimal_bits = min(vals, key=vals.get)
optimal_val  = vals[optimal_bits]

```python
print(f"Optimal QUBO solution: |{optimal_bits}>  value={optimal_val:.4f}")
sorted_vals  = sorted(vals.items(), key=lambda x: x[1])
print("Top-5 best bitstrings:")
for b, v in sorted_vals[:5]:
```
print(f"  |{b}>  f={v:.4f}")

```
```
# ── Grover: build oracle that marks |optimal_bits> ────────────────────────────

target_int = int(optimal_bits, 2)

```python
def grover_circuit(target, n_qubits, n_iter):
```
qc = QuantumCircuit(n_qubits)
qc.h(range(n_qubits))
for _ in range(n_iter):
```
```
        # phase oracle for target
        bits = format(target, f'0{n_qubits}b')
        for i, b in enumerate(reversed(bits)):
            if b == '0': qc.x(i)
        qc.h(n_qubits-1)
        qc.mcx(list(range(n_qubits-1)), n_qubits-1)
        qc.h(n_qubits-1)
        for i, b in enumerate(reversed(bits)):
            if b == '0': qc.x(i)
        # diffusion
        qc.h(range(n_qubits)); qc.x(range(n_qubits))
        qc.h(n_qubits-1)
        qc.mcx(list(range(n_qubits-1)), n_qubits-1)
        qc.h(n_qubits-1)
        qc.x(range(n_qubits)); qc.h(range(n_qubits))
    qc.measure_all()
    return qc

sim    = AerSimulator()
n_iter = max(1, int(np.floor(np.pi/4 * np.sqrt(2**n))))
qc     = grover_circuit(target_int, n, n_iter)
tc     = transpile(qc, sim, optimization_level=1)
result = sim.run(tc, shots=2048).result()
counts = result.get_counts()

top3 = sorted(counts.items(), key=lambda x: -x[1])[:3]
```python
print(f"\nGrover ({n_iter} iteration(s)) top-3 measurement outcomes:")
for bits, cnt in top3:
```
print(f"  |{bits}>  count={cnt}  f={qubo_val(bits):.4f}")
```
print(f"Optimal target: |{optimal_bits}>")

```
## Notes For Chapter Bridge

# **Chapter 15: differentiable quantum programming: how to compute exact () () (Codebook)**

# gradients through circuits and combine them with classical autodiff optimisers.