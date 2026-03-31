# **Chapter 5: Quantum Fourier Transform and Phase Estimation (Workbook)**

---

The goal of this chapter is to establish concepts in the Quantum Fourier Transform (QFT) and Quantum Phase Estimation (QPE). The QFT is a key component in many quantum algorithms, and QPE uses it to determine the eigenvalues of unitary operators.

---

## **5.1 Quantum Fourier Transform (QFT)** {.heading-with-pill}

> **Difficulty:** ★★☆☆☆
> 
> **Concept:** Basis change to the frequency domain via phase gradients
> 
> **Summary:** The QFT maps computational-basis amplitudes to a Fourier basis. For $N=2^n$ it acts as $|j\rangle\mapsto\tfrac{1}{\sqrt{N}}\sum_{k=0}^{N-1}\omega_N^{jk}|k\rangle$ with $\omega_N=e^{2\pi i/N}$ and admits a circuit of $\mathcal{O}(n^2)$ one- and two-qubit gates.

### **Theoretical Background**

The Quantum Fourier Transform (QFT) is the quantum analog of the discrete Fourier transform (DFT), mapping computational basis states to a superposition with phase relationships encoding frequency information.

**Mathematical Definition:**  
For an $n$-qubit system with dimension $N = 2^n$, define the primitive $N$-th root of unity:

$$
\omega_N = e^{2\pi i/N}
$$

The QFT acts on computational basis states as:

$$
\text{QFT}_N|j\rangle = \frac{1}{\sqrt{N}}\sum_{k=0}^{N-1} \omega_N^{jk}|k\rangle = \frac{1}{\sqrt{N}}\sum_{k=0}^{N-1} e^{2\pi ijk/N}|k\rangle
$$

By linearity, for an arbitrary state $|\psi\rangle = \sum_{j=0}^{N-1} \alpha_j|j\rangle$:

$$
\text{QFT}_N|\psi\rangle = \sum_{j=0}^{N-1} \alpha_j \cdot \text{QFT}_N|j\rangle = \frac{1}{\sqrt{N}}\sum_{j=0}^{N-1}\sum_{k=0}^{N-1} \alpha_j e^{2\pi ijk/N}|k\rangle = \sum_{k=0}^{N-1} \tilde{\alpha}_k|k\rangle
$$

where $\tilde{\alpha}_k = \frac{1}{\sqrt{N}}\sum_{j=0}^{N-1} \alpha_j e^{2\pi ijk/N}$ are the Fourier coefficients.

**Product Representation:**  
Expressing basis states in binary $j = j_{n-1}2^{n-1} + \cdots + j_1 2 + j_0$ with $j_\ell \in \{0,1\}$, the QFT has the elegant product form:

$$
\text{QFT}_N|j_{n-1}\cdots j_1 j_0\rangle = \frac{1}{2^{n/2}}\bigotimes_{\ell=0}^{n-1} \left(|0\rangle + e^{2\pi i \cdot 0.j_\ell j_{\ell-1}\cdots j_0}|1\rangle\right)
$$

where $0.j_\ell j_{\ell-1}\cdots j_0$ denotes the binary fraction $\sum_{m=0}^\ell j_m 2^{-(\ell-m+1)}$.

**Circuit Decomposition:**  
This product structure enables an efficient quantum circuit using:

1. **Hadamard gates** on each qubit to create superposition  
2. **Controlled phase rotations** $R_m = \text{diag}(1, e^{2\pi i/2^m})$ between qubits  
3. **Bit-reversal swaps** at the end

The complete circuit for qubit $j$ (indexed from $n-1$ down to $0$):

$$
\text{QFT}_N = \text{SWAP}_{\text{reverse}} \cdot \left(\prod_{j=n-1}^{0} \mathbf{H}_j \prod_{k=j+1}^{n-1} R_{k-j+1}^{(k,j)}\right)
$$

where $R_m^{(k,j)}$ denotes controlled-$R_m$ with control on qubit $k$ and target on qubit $j$.

**Gate Complexity:**  
The circuit requires:
- $n$ Hadamard gates  
- $\sum_{j=0}^{n-1}(n-1-j) = \frac{n(n-1)}{2}$ controlled rotations  
- $\lfloor n/2 \rfloor$ swap gates

Total: $\mathcal{O}(n^2)$ gates, exponentially better than the classical FFT's $\mathcal{O}(N\log N) = \mathcal{O}(n \cdot 2^n)$ operations.

**Inverse QFT:**  
The inverse operation is:

$$
\text{QFT}_N^{-1} = \text{QFT}_N^\dagger
$$

implemented by reversing gate order and conjugating rotations: $R_m \to R_m^\dagger = R_m^{-1}$.

### **Comprehension Check**

!!! note "Quiz"
    **1. What is $\omega_N$ in the QFT definition?**
    
    - A. A normalization constant  
    - B. A twiddle factor/root of unity  
    - C. A probability amplitude  
    - D. A diffusion parameter  
    
??? info "See Answer"
        **Correct: B.** $\omega_N=e^{2\pi i/N}$.
    
    **2. Asymptotic gate count of a straightforward QFT circuit on $n$ qubits is:**
    
    - A. $\mathcal{O}(n)$  
    - B. $\mathcal{O}(n^2)$  
    - C. $\mathcal{O}(2^n)$  
    - D. $\mathcal{O}(n\log n)$  
    
??? info "See Answer"
        **Correct: B.** Using Hadamards and controlled rotations yields $\mathcal{O}(n^2)$ gates.
    
---

!!! abstract "Interview-Style Question"
    
    **Q:** Why does the QFT not, by itself, provide a general exponential speedup when compared to the classical FFT?
    
    ???+ info "Answer Strategy"
        **The QFT Transformation:**  
        The Quantum Fourier Transform implements $\text{QFT}|j\rangle = \frac{1}{\sqrt{N}}\sum_{k=0}^{N-1} e^{2\pi ijk/N}|k\rangle$ using $\mathcal{O}(n^2)$ gates, exponentially faster than classical FFT's $\mathcal{O}(N \log N)$ operations. However, this apparent speedup has a critical limitation.
        
        $$
        \text{QFT}|j\rangle = \frac{1}{\sqrt{N}}\sum_{k=0}^{N-1} e^{2\pi ijk/N}|k\rangle
        $$
    
        **The Measurement Bottleneck:**  
        While QFT efficiently transforms amplitudes $|\psi\rangle = \sum_j \alpha_j|j\rangle \to \sum_k \tilde{\alpha}_k|k\rangle$, measurement collapses to a single outcome $|k_0\rangle$ with probability $|\tilde{\alpha}_{k_0}|^2$. Extracting all $N$ Fourier coefficients requires $\mathcal{O}(N)$ measurements, negating the speedup. Classical FFT outputs all coefficients explicitly in $\mathcal{O}(N \log N)$ operations.
    
        **When QFT Provides Advantage:**  
        QFT becomes powerful when embedded in larger algorithms exploiting interference patterns before measurement. QPE uses QFT to concentrate probability into binary phase representations. Shor's algorithm creates peaks at $k = 0, N/r, 2N/r, \ldots$ enabling period extraction. HHL manipulates eigenvalue-dependent phases.
        
        **Conclusion:**  
        QFT alone doesn't replace classical FFT due to measurement limitations. Exponential advantage emerges when QFT enables algorithmic structures that concentrate probability into polynomially many outcomes, making measurement informative.
    
---

### **<i class="fa-solid fa-flask"></i> Hands-On Projects**

#### **Project Blueprint**

| **Section**              | **Description** |
| ------------------------ | --------------- |
| **Objective**            | Compute QFT on $N=4$ for input $\|1\rangle$ and interpret phases. |
| **Mathematical Concept** | DFT over $\mathbb{Z}_4$; roots of unity. |
| **Experiment Setup**     | Two qubits; basis $\\{\|00\rangle,\|01\rangle,\|10\rangle,\|11\rangle\\}$. |
| **Process Steps**        | Apply $\mathrm{QFT}_4\|1\rangle=\tfrac{1}{2}\sum_{k=0}^3 e^{2\pi i k/4}\|k\rangle$; expand coefficients. |
| **Expected Behavior**    | Uniform magnitudes $1/2$; phases progress linearly: $1,i,-1,-i$. |
| **Tracking Variables**   | Complex amplitudes $c_k$; probabilities $|c_k|^2$. |
| **Verification Goal**    | Check normalization and phase pattern. |
| **Output**               | Statevector entries and interpretation. |

---

#### **Python Implementation**

```python
from qiskit.circuit.library import QFT
from qiskit.quantum_info import Statevector
from qiskit import QuantumCircuit
import numpy as np

# Project 1: QFT Circuit on 3 qubits

n = 3
qft_circ = QuantumCircuit(n)
qft_circ.append(QFT(n, do_swaps=True), range(n))

print("QFT circuit (n=3):")
print(qft_circ.decompose().draw())

# Apply QFT to |001> and check the output

qc = QuantumCircuit(n)
qc.x(0)     # |001>
qc.append(QFT(n, do_swaps=True), range(n))
sv = Statevector(qc)
print("\nQFT|001> amplitudes (all should have equal magnitude 1/sqrt(8)):")
for i, amp in enumerate(sv.data):
    print(f"  |{i:03b}> : {abs(amp):.4f} ∠{np.angle(amp)*180/np.pi:.1f}°")
```
**Sample Output:**
```python
QFT circuit (n=3):
     ┌──────┐
q_0: ┤0     ├
     │      │
q_1: ┤1 QFT ├
     │      │
q_2: ┤2     ├
     └──────┘

QFT|001> amplitudes (all should have equal magnitude 1/sqrt(8)):
  |000> : 0.3536 ∠0.0°
  |001> : 0.3536 ∠45.0°
  |010> : 0.3536 ∠90.0°
  |011> : 0.3536 ∠135.0°
  |100> : 0.3536 ∠180.0°
  |101> : 0.3536 ∠-135.0°
  |110> : 0.3536 ∠-90.0°
  |111> : 0.3536 ∠-45.0°
```


#### **Outcome and Interpretation**

The output exhibits equal magnitudes and a linear phase ramp; measuring yields each basis state with probability 1/4, but relative phases enable interference in downstream routines.

---

## **5.2 Quantum Phase Estimation (QPE)** {.heading-with-pill}

> **Difficulty:** ★★★☆☆
> 
> **Concept:** Binary phase readout via controlled powers and inverse QFT
> 
> **Summary:** For $U|\psi\rangle=e^{2\pi i\phi}|\psi\rangle$, QPE estimates $\phi$ to $n$ bits by applying controlled-$U^{2^j}$ from a counting register prepared by Hadamards and concluding with an inverse QFT and measurement.

### **Theoretical Background**

Quantum Phase Estimation (QPE) is the cornerstone algorithm for extracting eigenphases from unitary operators, enabling applications from Shor's algorithm to quantum chemistry simulation.

**Problem Statement:**  
Given a unitary operator $U$ and one of its eigenstates $|\psi\rangle$ satisfying:

$$
U|\psi\rangle = e^{2\pi i\phi}|\psi\rangle
$$

where the eigenphase $\phi \in [0,1)$ is unknown, estimate $\phi$ to $n$ bits of precision.

**Circuit Architecture:**  
Initialize two registers:
- **Counting register:** $n$ qubits in state $|0\rangle^{\otimes n}$  
- **Target register:** eigenstate $|\psi\rangle$

The complete state is $|\psi_0\rangle = |0\rangle^{\otimes n} \otimes |\psi\rangle$.

**Step 1: Hadamard Preparation:**  
Apply Hadamard gates to the counting register:

$$
|\psi_1\rangle = (\mathbf{H}^{\otimes n} \otimes \mathbf{I})|\psi_0\rangle = \frac{1}{2^{n/2}}\sum_{k=0}^{2^n-1} |k\rangle \otimes |\psi\rangle
$$

**Step 2: Controlled Unitary Powers:**  
For each counting qubit $j \in \{0, 1, \ldots, n-1\}$, apply controlled-$U^{2^j}$ with qubit $j$ as control:

$$
|\psi_2\rangle = \frac{1}{2^{n/2}}\sum_{k=0}^{2^n-1} U^k|\psi\rangle \otimes |k\rangle = \frac{1}{2^{n/2}}\sum_{k=0}^{2^n-1} e^{2\pi i k\phi}|k\rangle \otimes |\psi\rangle
$$

Here we used the eigenvalue property: $U^k|\psi\rangle = (e^{2\pi i\phi})^k|\psi\rangle = e^{2\pi ik\phi}|\psi\rangle$.

Note the target register factors out—it remains in $|\psi\rangle$ throughout, unentangled with the counting register.

**Step 3: Inverse QFT:**  
Apply $\text{QFT}_N^{-1}$ to the counting register. Using the inverse transform:

$$
\text{QFT}_N^{-1}|k\rangle = \frac{1}{\sqrt{N}}\sum_{j=0}^{N-1} e^{-2\pi ijk/N}|j\rangle
$$

The state becomes:

$$
|\psi_3\rangle = \frac{1}{N}\sum_{k=0}^{N-1}\sum_{j=0}^{N-1} e^{2\pi ik(\phi - j/N)}|j\rangle \otimes |\psi\rangle
$$

**Amplitude Analysis:**  
The amplitude of computational basis state $|j\rangle$ is:

$$
\alpha_j = \frac{1}{N}\sum_{k=0}^{N-1} e^{2\pi ik(\phi - j/N)}
$$

This is a geometric series. When $\phi = j/N$ exactly (i.e., $\phi$ has an exact $n$-bit binary representation):

$$
\alpha_j = \begin{cases} 1 & \text{if } j = \lfloor N\phi \rfloor \\ 0 & \text{otherwise} \end{cases}
$$

Measurement deterministically yields $j = \lfloor 2^n \phi \rfloor$, from which $\phi = j/2^n$ exactly.

**Inexact Phase Case:**  
When $\phi$ cannot be exactly represented in $n$ bits, let $\phi = \phi_0 + \delta$ where $\phi_0 = b/2^n$ is the closest $n$-bit approximation and $|\delta| \leq 1/2^{n+1}$. The probability of measuring the best approximation $b$ is:

$$
P(b) = \left|\frac{1}{N}\sum_{k=0}^{N-1} e^{2\pi ik\delta}\right|^2 = \left|\frac{1-e^{2\pi iN\delta}}{N(1-e^{2\pi i\delta})}\right|^2 \geq \frac{4}{\pi^2} \approx 0.405
$$

Thus QPE succeeds with probability $> 40\%$ even for inexact phases, and repeating $\mathcal{O}(1)$ times yields arbitrarily high confidence.

### **Comprehension Check**

!!! note "Quiz"
    **1. Which operation prepares the counting register?**
    
    - A. $\mathrm{QFT}^{-1}$  
    - B. Hadamards  
    - C. SWAPs  
    - D. Controlled-NOTs  
    
??? info "See Answer"
        **Correct: B.** $\mathbf{H}^{\otimes n}$ creates the uniform superposition.
    
    **2. Why use powers $U^{2^j}$?**
    
    - A. To reduce depth  
    - B. To linearize the phase  
    - C. To encode successive binary digits of $\phi$  
    - D. To avoid entanglement  
    
??? info "See Answer"
        **Correct: C.** Exponential powers map bits of $\phi$ into separable phase patterns decodable by $\mathrm{QFT}^{-1}$.
    
---

!!! abstract "Interview-Style Question"
    
    **Q:** What happens when $|\psi\rangle$ is not an eigenstate of $U$?
    
    ???+ info "Answer Strategy"
        **Eigenstate Decomposition:**  
        QPE extracts eigenphase $\phi$ when the target is an eigenstate $U|\psi_\phi\rangle = e^{2\pi i \phi}|\psi_\phi\rangle$. For non-eigenstates, decompose as $|\psi\rangle = \sum_j c_j |\psi_j\rangle$ where $|\psi_j\rangle$ are eigenstates with eigenvalues $e^{2\pi i \phi_j}$.
        
        $$
        |\psi\rangle = \sum_j c_j |\psi_j\rangle \quad \xrightarrow{\text{QPE}} \quad \sum_j c_j |\tilde{\phi}_j\rangle \otimes |\psi_j\rangle
        $$
    
        **Probabilistic Outcome:**  
        Measurement yields phase estimate $|\tilde{\phi}_j\rangle$ with probability $P(\phi_j) = |c_j|^2 = |\langle \psi_j|\psi\rangle|^2$, the overlap with eigenstate $|\psi_j\rangle$. This produces a random sample from the eigenphase distribution weighted by state projections.
    
        **Practical Consequences:**  
        Repeated runs yield different phases with probabilities $|c_j|^2$, sampling the eigenspectrum $\{(\phi_j, |c_j|^2)\}$. In Shor's algorithm, $|1\rangle$ decomposes over eigenstates of $U_a$, sampling uniformly from $\{k/r : k = 0, 1, \ldots, r-1\}$. Continued fractions extract period $r$ from sampled $k/r$. Post-selection on target measurements can prepare specific eigenstates with success probability $|c_k|^2$.
    
---

### **<i class="fa-solid fa-flask"></i> Hands-On Projects**

#### **Project Blueprint**

| **Section**              | **Description** |
| ------------------------ | --------------- |
| **Objective**            | Estimate $\phi$ to $n$ bits using QPE with oracle $U$. |
| **Mathematical Concept** | Phase kickback; inverse QFT decoding. |
| **Experiment Setup**     | Choose an eigenpair $(\|\psi\rangle,\phi)$; $n$ counting qubits. |
| **Process Steps**        | Prepare registers; apply controlled-$U^{2^j}$; apply $\mathrm{QFT}^{-1}$; measure. |
| **Expected Behavior**    | Output bitstring approximating $\phi$ in binary. |
| **Tracking Variables**   | Estimated bits; success probability vs precision. |
| **Verification Goal**    | Compare measured estimate to true $\phi$ within $\pm 2^{-n}$. |
| **Output**               | Estimated phase and error bound. |

---

#### **Python Implementation**

```python
from qiskit.circuit.library import QFT
from qiskit.quantum_info import Operator
from qiskit import QuantumCircuit
import numpy as np

# Project 2: Inverse QFT and round-trip verification

n = 3
iqft = QFT(n, inverse=True, do_swaps=True)

# Verify QFT • QFT^-1 = Identity

qft_mat  = Operator(QFT(n, do_swaps=True)).data
iqft_mat = Operator(iqft).data
product  = qft_mat @ iqft_mat
is_identity = np.allclose(product, np.eye(2**n), atol=1e-10)
print(f"QFT × QFT^-1 = Identity: {is_identity}")
print(f"Max deviation from I: {np.max(np.abs(product - np.eye(2**n))):.2e}")

# Round-trip a state through QFT → iQFT

qc = QuantumCircuit(n)
qc.h(0); qc.x(1)         # some initial state
qc.append(QFT(n), range(n))
qc.append(iqft, range(n))
from qiskit.quantum_info import Statevector
sv_in  = Statevector(QuantumCircuit(n).compose(QuantumCircuit(n).h(0).x(1) or QuantumCircuit(n)))
sv_out = Statevector(qc)
print("\nRound-trip state preserved:", np.allclose(sv_in.data if hasattr(sv_in,'data') else [1,0,0,0,0,0,0,0], sv_out.data, atol=1e-10))
```
**Sample Output:**
```python
QFT × QFT^-1 = Identity: True
Max deviation from I: 6.66e-16
```


#### **Outcome and Interpretation**

Controlled powers encode binary digits of the eigenphase; inverse QFT concentrates probability mass on the closest $n$-bit approximation.

---

## **5.3 Phase Kickback** {.heading-with-pill}

> **Difficulty:** ★★☆☆☆
> 
> **Concept:** Converting target phases into control-register phases
> 
> **Summary:** Preparing the control in $|{-}\rangle$ causes a controlled-$U$ to imprint the target’s eigenphase onto the control as a relative phase, enabling interference-based readout.

### **Theoretical Background**

Phase kickback is the quantum phenomenon where a phase factor from the target system of a controlled operation transfers to the control system, enabling indirect measurement of eigenphases without disturbing the eigenstate.

**Mathematical Mechanism:**  
Consider a controlled-unitary gate $\text{ctrl-}U$ acting on control qubit $c$ and target state $|\psi\rangle$ where $U|\psi\rangle = e^{2\pi i\phi}|\psi\rangle$:

$$
\text{ctrl-}U = |0\rangle\langle 0|_c \otimes \mathbf{I} + |1\rangle\langle 1|_c \otimes U
$$

When the control is in computational basis:

$$
\text{ctrl-}U\big(|0\rangle_c \otimes |\psi\rangle\big) = |0\rangle_c \otimes |\psi\rangle
$$
$$
\text{ctrl-}U\big(|1\rangle_c \otimes |\psi\rangle\big) = |1\rangle_c \otimes U|\psi\rangle = e^{2\pi i\phi}|1\rangle_c \otimes |\psi\rangle
$$

The phase appears as a global factor multiplying the entire state, not directly observable.

**Kickback via Superposition:**  
Prepare the control in $|+\rangle = \frac{1}{\sqrt{2}}(|0\rangle + |1\rangle)$:

$$
\text{ctrl-}U\left(\frac{1}{\sqrt{2}}(|0\rangle + |1\rangle)_c \otimes |\psi\rangle\right) = \frac{1}{\sqrt{2}}\Big(|0\rangle_c \otimes |\psi\rangle + e^{2\pi i\phi}|1\rangle_c \otimes |\psi\rangle\Big)
$$

Factoring out the eigenstate:

$$
= \frac{1}{\sqrt{2}}\big(|0\rangle_c + e^{2\pi i\phi}|1\rangle_c\big) \otimes |\psi\rangle
$$

The eigenphase now appears as a **relative phase** between control qubit basis states, while the target remains in $|\psi\rangle$ (separable, not entangled).

**Bloch Sphere Interpretation:**  
The control qubit state $\frac{1}{\sqrt{2}}(|0\rangle + e^{2\pi i\phi}|1\rangle)$ represents rotation about the $z$-axis by angle $2\pi\phi$:

$$
|\phi_{\text{ctrl}}\rangle = R_z(2\pi\phi)|+\rangle = e^{-i\pi\phi Z}|+\rangle
$$

**Interferometric Readout:**  
Applying Hadamard to convert relative phase to amplitude:

$$
\mathbf{H}\left(\frac{1}{\sqrt{2}}(|0\rangle + e^{2\pi i\phi}|1\rangle)\right) = \frac{1}{2}\Big[(1+e^{2\pi i\phi})|0\rangle + (1-e^{2\pi i\phi})|1\rangle\Big]
$$

Simplifying using Euler's formula $e^{2\pi i\phi} = \cos(2\pi\phi) + i\sin(2\pi\phi)$:

$$
= \cos(\pi\phi)|0\rangle + i\sin(\pi\phi)|1\rangle
$$

Measurement probabilities become:

$$
P(0) = \cos^2(\pi\phi), \quad P(1) = \sin^2(\pi\phi)
$$

enabling phase estimation from single-qubit statistics.

**Multi-Qubit Extension (QPE):**  
With $n$ control qubits and controlled-$U^{2^j}$ operations, each control $j$ experiences phase $2^j \phi$:

$$
\frac{1}{2^{n/2}}\sum_{k=0}^{2^n-1} e^{2\pi ik\phi}|k\rangle \otimes |\psi\rangle
$$

Inverse QFT on controls decodes binary digits of $\phi$ while target remains factored in eigenstate $|\psi\rangle$—the essence of quantum phase estimation.

### **Comprehension Check**

!!! note "Quiz"
    **1. Which control-state is convenient for kickback?**
    
    - A. $|0\rangle$  
    - B. $|1\rangle$  
    - C. $|+\rangle$ or $|{-}\rangle$  
    - D. $|i\rangle$  
    
??? info "See Answer"
        **Correct: C.** Superposition states convert unitary action to relative phase.
    
    **2. After kickback, how is phase read out?**
    
    - A. Direct measurement  
    - B. Apply Hadamard(s) to map phase to amplitudes  
    - C. Apply SWAPs  
    - D. Use CZ  
    
??? info "See Answer"
        **Correct: B.** Interference via Hadamards converts phase information into measurable probabilities.
    
---

!!! abstract "Interview-Style Question"
    
    **Q:** Why is kickback critical for reducing multi-qubit eigenphase information to single-qubit interference?
    
    ???+ info "Answer Strategy"
        **The Information Localization Problem:**  
        Phase $\phi$ from eigenvalue $e^{2\pi i \phi}$ is a global property of multi-qubit state $|\psi\rangle$—directly unmeasurable. Phase kickback transduces this into an observable quantity in a control register.
        
        $$
        \frac{1}{\sqrt{2}}(|0\rangle + |1\rangle) \otimes |\psi\rangle \xrightarrow{\text{ctrl-}U} \frac{1}{\sqrt{2}}(|0\rangle + e^{2\pi i \phi}|1\rangle) \otimes |\psi\rangle
        $$
    
        **Single-Qubit Interference:**  
        Eigenphase kicks back to control qubit's relative phase: $|\phi_{\text{ctrl}}\rangle = R_z(2\pi\phi) \cdot |+\rangle$. Applying Hadamard yields measurement probabilities $P(0) = \cos^2(\pi\phi)$, enabling single-qubit interferometric phase estimation. The target register remains unchanged and factored out.
    
        **Collective Decoding via QFT:**  
        In QPE with $n$ controls, each experiences controlled-$U^{2^j}$, creating $\frac{1}{\sqrt{2^n}}\sum_k e^{2\pi i k\phi}|k\rangle \otimes |\psi\rangle$. Target register is unentangled. Inverse QFT acts as matched filter, concentrating probability into $|\tilde{\phi}\rangle$, the $n$-bit binary representation of $\phi$, achieving exponential precision with polynomial gates.
        
        **Key Advantage:**  
        Without kickback, controlled operations entangle control and target, destroying clean interference. Kickback preserves separability, enabling control-only interferometry while target stores eigenstate unchanged—the architectural principle underlying quantum phase estimation algorithms.
    
---

### **<i class="fa-solid fa-flask"></i> Hands-On Projects**

#### **Project Blueprint**

| **Section**              | **Description** |
| ------------------------ | --------------- |
| **Objective**            | Demonstrate single-qubit phase kickback using a controlled-phase gate. |
| **Mathematical Concept** | Relative phase accumulation; Hadamard interferometry. |
| **Experiment Setup**     | Control qubit initialized to $|+\rangle$; target an eigenstate of $U$. |
| **Process Steps**        | Apply controlled-$U$; then Hadamard on control; measure. |
| **Expected Behavior**    | Outcome probabilities depend on $\phi$. |
| **Tracking Variables**   | Control measurement $P(0),P(1)$ as functions of $\phi$. |
| **Verification Goal**    | Match $P(0)=\cos^2(\pi\phi)$, $P(1)=\sin^2(\pi\phi)$. |
| **Output**               | Estimated $\phi$ from observed counts. |

---

#### **Python Implementation**

```python
from qiskit.circuit.library import QFT
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector
import numpy as np

# Project 3: Period-Finding Signature via QFT

# Encode a periodic state |ψ> with period r=2 on 4 qubits

n = 4
psi = np.zeros(2**n, dtype=complex)
for x in range(0, 2**n, 2):   # period r=2
    psi[x] = 1.0
psi /= np.linalg.norm(psi)

qc = QuantumCircuit(n)
from qiskit.extensions import Initialize
init_gate = Initialize(psi)
qc.append(init_gate, range(n))
qc.append(QFT(n, do_swaps=True), range(n))

sv = Statevector(qc)
probs = sv.probabilities()
print("QFT of period-2 state: high-prob outcomes (multiples of N/r = 8):")
for i, p in enumerate(probs):
    if p > 0.05: print(f"  |{i:04b}> ({i}) : p={p:.4f}")
```

#### **Outcome and Interpretation**

You convert hidden eigenphase into measurable bias on a single qubit, the primitive underpinning QPE.

---

## **5.4 Order Finding and Applications** {.heading-with-pill}

> **Difficulty:** ★★★☆☆
> 
> **Concept:** Period estimation in modular arithmetic via QPE
> 
> **Summary:** For $f(x)=a^x\bmod N$, QPE over the unitary $U_a:|x\rangle\mapsto|ax\bmod N\rangle$ estimates the order $r$ where $a^r\equiv1\pmod N$; classical post-processing via gcd yields nontrivial factors.

### **Theoretical Background**

Order finding is the quantum subroutine underlying Shor's factoring algorithm, reducing the problem of finding the multiplicative order of an element in modular arithmetic to quantum phase estimation.

**Problem Definition:**  
Given integers $a$ and $N$ with $\gcd(a,N)=1$, find the smallest positive integer $r$ (the order or period) such that:

$$
a^r \equiv 1 \pmod{N}
$$

**Modular Multiplication as Unitary:**  
Define the unitary operator $U_a$ acting on the computational basis of $\mathbb{Z}_N = \{0, 1, \ldots, N-1\}$:

$$
U_a|y\rangle = |ay \bmod N\rangle
$$

This is unitary since multiplication by $a \bmod N$ is a permutation (bijection) when $\gcd(a,N)=1$. Controlled powers can be implemented efficiently:

$$
U_a^{2^j}|y\rangle = |a^{2^j} y \bmod N\rangle
$$

using $\mathcal{O}(\log^2 N)$ gates via repeated squaring.

**Eigenvalue Structure:**  
The eigenstates of $U_a$ are:

$$
|\psi_s\rangle = \frac{1}{\sqrt{r}}\sum_{k=0}^{r-1} e^{-2\pi isk/r}|a^k \bmod N\rangle \quad \text{for } s \in \{0, 1, \ldots, r-1\}
$$

Verifying the eigenvalue property:

$$
U_a|\psi_s\rangle = \frac{1}{\sqrt{r}}\sum_{k=0}^{r-1} e^{-2\pi isk/r}|a^{k+1} \bmod N\rangle = \frac{1}{\sqrt{r}}\sum_{\ell=1}^{r} e^{-2\pi is(\ell-1)/r}|a^\ell \bmod N\rangle
$$

Substituting $\ell-1 \to k$ and using periodicity $a^r \equiv 1$:

$$
= e^{2\pi is/r} \cdot \frac{1}{\sqrt{r}}\sum_{k=0}^{r-1} e^{-2\pi isk/r}|a^k \bmod N\rangle = e^{2\pi is/r}|\psi_s\rangle
$$

Thus the eigenvalues are $\lambda_s = e^{2\pi is/r}$ with eigenphases:

$$
\phi_s = \frac{s}{r} \quad \text{for } s \in \{0, 1, \ldots, r-1\}
$$

**QPE Application:**  
Starting with $|1\rangle$ (not an eigenstate), decompose:

$$
|1\rangle = \frac{1}{\sqrt{r}}\sum_{s=0}^{r-1} |\psi_s\rangle
$$

Applying QPE produces:

$$
\frac{1}{\sqrt{r}}\sum_{s=0}^{r-1} |\tilde{\phi}_s\rangle \otimes |\psi_s\rangle
$$

Measuring the phase register yields random $s \in \{0, \ldots, r-1\}$ with equal probability $1/r$, providing estimate $\tilde{\phi} \approx s/r$.

**Continued Fractions Extraction:**  
From measured approximation $m/2^n \approx s/r$, the continued fractions algorithm finds the fraction with smallest denominator within precision:

$$
\left|\frac{s}{r} - \frac{m}{2^n}\right| \leq \frac{1}{2^{n+1}}
$$

Choosing $n = 2\log_2 N$ ensures $1/2^{n+1} < 1/(2N^2) < 1/(2r^2)$, guaranteeing $s/r$ appears as a convergent.

**Factor Extraction:**  
Once $r$ is determined, if:
1. $r$ is even, and  
2. $a^{r/2} \not\equiv -1 \pmod{N}$

then $a^r - 1 = (a^{r/2}-1)(a^{r/2}+1) \equiv 0 \pmod{N}$, but $N$ divides the product without dividing individual factors. Computing:

$$
\gcd(a^{r/2} \pm 1, N)
$$

yields nontrivial factors with probability $\geq 1/2$ over random choice of $a$.

### **Comprehension Check**

!!! note "Quiz"
    **1. Order finding seeks:**
    
    - A. Minimal $r$ with $a^r\equiv1\pmod N$  
    - B. Minimal $r$ with $a^r\equiv0\pmod N$  
    - C. $\gcd(a,N)$  
    - D. A discrete log  
    
??? info "See Answer"
        **Correct: A.** The multiplicative order.
    
    **2. The classical finishing step uses:**
    
    - A. Euclid’s algorithm  
    - B. FFT  
    - C. Gradient descent  
    - D. Simulated annealing  
    
??? info "See Answer"
        **Correct: A.** $\gcd$ computations extract factors from $a^{r/2}\pm1$.
    
---

!!! abstract "Interview-Style Question"
    
    **Q:** Why is continued-fraction decoding necessary after QPE in order finding?
    
    ???+ info "Answer Strategy"
        **The Rational Approximation Problem:**  
        QPE estimates eigenphase $\phi = k/r$ to $n$ bits, yielding measurement $m \approx 2^n \cdot k/r$. Direct division $m/2^n$ gives decimal approximation like $0.748031...$ but doesn't reveal underlying fraction $k/r$. Naively rounding is unreliable among exponentially many possible fractions.
        
        $$
        \left|\frac{k}{r} - \frac{m}{2^n}\right| \leq \frac{1}{2^{n+1}} < \frac{1}{2r^2}
        $$
    
        **Continued Fractions Algorithm:**  
        Continued fraction expansion produces convergents $p_i/q_i$ that are best rational approximations. Fundamental theorem: if $|x - k/r| \leq 1/(2r^2)$, then $k/r$ appears as a convergent. For QPE output $m/2^n$, compute convergents, check $q_i \leq N$ and verify $a^{q_i} \equiv 1 \pmod{N}$ to find order $r$.
    
        **Robustness and Efficiency:**  
        Continued fractions automatically find simplest fraction closest to measured value in $\mathcal{O}(\log N)$ operations. Handles measurement errors gracefully—even if $m$ is off by units, correct $k/r$ remains a convergent. Example: $N=15$, $a=2$, $r=4$. QPE yields $m=64$, giving $1/4$ with convergent denominator $q=4$. Checking $2^4 \equiv 1 \pmod{15}$ confirms $r=4$.
        
        **Why Alternatives Fail:**  
        Brute force testing all $r \leq N$ requires $\mathcal{O}(N)$ complexity, eliminating quantum advantage. Rounding heuristics fail for large $r$ or common factors. Continued fractions uniquely extract denominators efficiently from finite-precision approximations.
    
---

### **<i class="fa-solid fa-flask"></i> Hands-On Projects**

#### **Project Blueprint**

| **Section**              | **Description** |
| ------------------------ | --------------- |
| **Objective**            | Outline the QPE-based order-finding workflow and its classical post-processing. |
| **Mathematical Concept** | Eigenphases $k/r$; continued fractions; gcd extraction. |
| **Experiment Setup**     | Choose small $N$ (e.g., 15) and $a$ coprime to $N$. |
| **Process Steps**        | Run conceptual QPE to estimate $k/r$; apply continued fractions; compute $\gcd(a^{r/2}\pm1,N)$. |
| **Expected Behavior**    | Recover $r$ and nontrivial factors. |
| **Tracking Variables**   | Phase estimates; convergents; gcd outputs. |
| **Verification Goal**    | Confirm factors multiply to $N$. |
| **Output**               | $r$ and factors of $N$. |

---

#### **Python Implementation**

```python
import numpy as np

# Project 4: QFT vs Classical FFT Comparison

N = 8
# Classical signal: period-2 cosine

x = np.array([1, 0, 1, 0, 1, 0, 1, 0], dtype=float)

# Classical DFT (numpy FFT)

X_fft = np.fft.fft(x)
freqs  = np.fft.fftfreq(N)

print("Signal:", x)
print("\nFFT magnitudes:")
for k, (f, amp) in enumerate(zip(freqs, np.abs(X_fft))):
    if amp > 0.1: print(f"  bin {k:2d} (freq {f:.3f}): |X[k]| = {amp:.4f}")

# QFT uses the SAME unitary as DFT (up to normalization)

omega = np.exp(-2j * np.pi / N)
DFT_matrix = np.array([[omega**(j*k) for k in range(N)] for j in range(N)]) / np.sqrt(N)
X_qft = DFT_matrix @ x
print("\nQFT magnitudes (should match FFT/sqrt(N)):")
for k, amp in enumerate(np.abs(X_qft)):
    if amp > 0.05: print(f"  |{k:03b}> ({k}): {amp:.4f}")
```
**Sample Output:**
```python
Signal: [1. 0. 1. 0. 1. 0. 1. 0.]

FFT magnitudes:
  bin  0 (freq 0.000): |X[k]| = 4.0000
  bin  4 (freq -0.500): |X[k]| = 4.0000

QFT magnitudes (should match FFT/sqrt(N)):
  |000> (0): 1.4142
  |100> (4): 1.4142
```


#### **Outcome and Interpretation**

This workflow isolates the quantum advantage (phase estimation) from classical number-theoretic post-processing.

---

## **5.5 Approximate QFT and Depth Trade-Offs** {.heading-with-pill}

> **Difficulty:** ★★☆☆☆
> 
> **Concept:** Truncating small-angle rotations to reduce depth
> 
> **Summary:** Dropping controlled rotations below a threshold yields an approximate QFT with lower depth and gate count; the induced error can be bounded and is often acceptable on NISQ devices.

### **Theoretical Background**

The approximate QFT reduces circuit depth by truncating small-angle controlled rotations while maintaining sufficient accuracy for phase estimation applications on NISQ hardware.

**Exact QFT Gate Structure:**  
The standard QFT on qubit $j$ requires controlled rotations from all higher qubits $k > j$:

$$
\mathbf{H}_j \prod_{k=j+1}^{n-1} R_{k-j+1}^{(k,j)} \quad \text{where} \quad R_m = \begin{pmatrix} 1 & 0 \\ 0 & e^{2\pi i/2^m} \end{pmatrix}
$$

For large separation $k-j$, the rotation angle $\theta_m = 2\pi/2^m$ becomes exponentially small. For example:
- $m=10$: $\theta_{10} = 2\pi/1024 \approx 0.0061$ rad  
- $m=15$: $\theta_{15} = 2\pi/32768 \approx 0.00019$ rad  
- $m=20$: $\theta_{20} = 2\pi/1048576 \approx 6 \times 10^{-6}$ rad

**Truncation Strategy:**  
Omit all rotations $R_m$ with $m > t$ for some threshold $t$. The approximate QFT becomes:

$$
\text{QFT}_{\text{approx}} = \text{SWAP}_{\text{reverse}} \cdot \left(\prod_{j=n-1}^{0} \mathbf{H}_j \prod_{k=j+1}^{\min(j+t, n-1)} R_{k-j+1}^{(k,j)}\right)
$$

This reduces the number of controlled rotations from $\frac{n(n-1)}{2}$ to approximately $nt$.

**Error Analysis:**  
Define the fidelity between exact and approximate QFT acting on state $|\psi\rangle$:

$$
F = |\langle\psi|\text{QFT}^\dagger_{\text{approx}} \text{QFT}_{\text{exact}}|\psi\rangle|^2
$$

For uniformly random input states, the average fidelity is bounded by:

$$
\mathbb{E}[F] \geq 1 - \epsilon \quad \text{where} \quad \epsilon \lesssim \frac{n}{2^t}
$$

Thus choosing $t = \log_2(n) + b$ yields error $\epsilon \sim 2^{-b}$.

**Phase Error in QPE:**  
The induced phase error in quantum phase estimation is:

$$
|\delta\phi| \lesssim \frac{1}{2^t}
$$

Since QPE needs precision $1/2^n$, the approximation is acceptable when:

$$
t \geq n - \log_2(n) - c
$$

for small constant $c$, typically $c \approx 3-5$.

**Circuit Depth Reduction:**  
Exact QFT has depth $\mathcal{O}(n^2)$ due to $n$ layers each with $\mathcal{O}(n)$ gates. Approximate QFT reduces depth to:

$$
D_{\text{approx}} \approx n + t \cdot \log_2(\text{connectivity})
$$

For $t = \mathcal{O}(\log n)$, this becomes $\mathcal{O}(n \log n)$, a quadratic improvement.

**NISQ Hardware Considerations:**  
On devices with gate error rate $\epsilon_{\text{gate}} \sim 10^{-3}$ and coherence time limiting depth to $D_{\max} \sim 100-200$ gates, choose truncation level where algorithmic error matches hardware noise:

$$
2^{-t} \sim \epsilon_{\text{gate}} \cdot D_{\text{approx}} \implies t \approx \log_2\left(\frac{1}{\epsilon_{\text{gate}} \cdot n}\right)
$$

Typically $t \in [8, 15]$ for $n \in [10, 25]$ qubits on current NISQ devices.

### **Comprehension Check**

!!! note "Quiz"
    **1. Approximating QFT mainly reduces:**
    
    - A. Width  
    - B. Depth and two-qubit gates  
    - C. Classical post-processing  
    - D. Measurement shots  
    
??? info "See Answer"
        **Correct: B.** Small-angle rotations are costly and sensitive to noise.
    
    **2. The trade-off of approximation is:**
    
    - A. No change  
    - B. Bounded phase error  
    - C. Fewer qubits  
    - D. Exact results  
    
??? info "See Answer"
        **Correct: B.** Errors grow with dropped angles but can be analytically bounded.
    
---

!!! abstract "Interview-Style Question"
    
    **Q:** When would you prefer an approximate QFT in QPE on NISQ hardware?
    
    ???+ info "Answer Strategy"
        **The Depth-Precision Trade-off:**  
        Exact QFT requires $\mathcal{O}(n^2)$ gates including controlled rotations $R_k(\theta)$ with angles $\theta_j = 2\pi/2^j$. For large $j$, rotations become tiny ($\theta_{15} \approx 0.0002$ rad). On NISQ devices with gate errors $\epsilon_{\text{gate}} \sim 10^{-3}$ and coherence $T_2 \sim 50-500~\mu$s, these small rotations are overwhelmed by noise.
        
        $$
        |\delta\phi| \lesssim \frac{1}{2^m}
        $$
    
        **When to Use Approximate QFT:**  
        Omit rotations with $j > m$ when noise magnitude exceeds signal. For Shor's algorithm factoring $N \sim 2048$ needing $\sim 22$ bits, exact QFT requires $\sim 484$ gates exceeding typical depth budget of $\sim 200$ gates. Approximate QFT truncating to $m = 15$ uses $\sim 225$ gates, fitting within coherence limits while providing sufficient $1/2^{15}$ precision for continued fractions.
    
        **Circuit Depth Reduction:**  
        Approximate QFT reduces gate count from $\mathcal{O}(n^2)$ to $\mathcal{O}(nm)$ and depth proportionally. Example: $n=20$, $m=10$ reduces gates from $\sim 400$ to $\sim 200$ and depth from $\sim 190$ to $\sim 95$. Choose $m$ where $1/2^m \sim \epsilon_{\text{hw}}$ (matching noise floor) and $1/2^m < \epsilon_{\text{app}}$ (meeting application requirements).
        
        **Practical Decision:**  
        On IBM Quantum with $\epsilon_{\text{hw}} \sim 10^{-3}$ and depth budget $\sim 150$ gates, use $m = 12$ yielding precision $1/2^{12} \approx 2.4 \times 10^{-4}$ and depth $\sim 132$ gates. Exact QFT would require $\sim 288$ gates, guaranteed failure. On fault-tolerant devices with $\epsilon_{\text{gate}} < 10^{-10}$, use exact QFT for maximum precision.
    
---

### **<i class="fa-solid fa-flask"></i> Hands-On Projects**

#### **Project Blueprint**

| **Section**              | **Description** |
| ------------------------ | --------------- |
| **Objective**            | Compare depth and expected phase error between exact and approximate QFT for $n$ qubits. |
| **Mathematical Concept** | Thresholding controlled rotations; error vs precision. |
| **Experiment Setup**     | Choose $n\in\{4,6,8\}$; drop rotations below angle $2\pi/2^t$. |
| **Process Steps**        | Count gates and layers for exact vs truncated; estimate phase error bound. |
| **Expected Behavior**    | Significant depth reduction with small increase in error. |
| **Tracking Variables**   | Gate counts, depth, error bound. |
| **Verification Goal**    | Confirm error within application tolerance. |
| **Output**               | Depth/error table and narrative. |

---

#### **Python Implementation**

```python
from qiskit.circuit.library import QFT
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector
import numpy as np

# Project 5: QPE Precision vs Number of Ancilla Bits

def qpe_precision(n_ancilla, phase_target):
    """Estimate how precisely QPE estimates a phase with n_ancilla bits."""
    qc = QuantumCircuit(n_ancilla + 1)
    qc.h(range(n_ancilla))
    qc.x(n_ancilla)  # eigenstate
    for k in range(n_ancilla):
        angle = 2 * np.pi * phase_target * (2**k)
        qc.cp(angle, k, n_ancilla)
    from qiskit.circuit.library import QFT
    qc.append(QFT(n_ancilla, inverse=True), range(n_ancilla))
    sv = Statevector(qc)
    probs = sv.probabilities()[:2**n_ancilla]
    best = np.argmax(probs)
    phase_est = best / 2**n_ancilla
    return phase_est, abs(phase_est - phase_target)

phase_target = 0.3
print(f"QPE precision for phase = {phase_target}:")
for n in [2, 3, 4, 5]:
    est, err = qpe_precision(n, phase_target)
    print(f"  n_ancilla={n}: estimated={est:.4f}  error={err:.4f}  (1/2^n={1/2**n:.4f})")
```
**Sample Output:**
```python
QPE precision for phase = 0.3:
  n_ancilla=2: estimated=0.0000  error=0.3000  (1/2^n=0.2500)
  n_ancilla=3: estimated=0.0000  error=0.3000  (1/2^n=0.1250)
  n_ancilla=4: estimated=0.0000  error=0.3000  (1/2^n=0.0625)
  n_ancilla=5: estimated=0.0000  error=0.3000  (1/2^n=0.0312)
```


#### **Outcome and Interpretation**

Approximate QFT provides a practical path to phase estimation on noisy hardware by trading a small accuracy loss for large depth savings.