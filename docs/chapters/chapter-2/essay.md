# **Chapter 2: State and Operators**

---

# **Introduction**

This chapter provides a comprehensive mathematical foundation for quantum computing, establishing the formal language and operational framework necessary for quantum algorithm design and circuit construction. The central theme is that quantum computation is fundamentally **linear algebra over complex vector spaces**, requiring precise mathematical tools to describe quantum states, evolution, and measurement.

We begin with the elegant **Dirac notation** (bra-ket formalism) that provides the standard language for quantum states and operations. The chapter then extends to the **density matrix formalism** for handling mixed states and classical uncertainty, explores **unitary operators** as the gates of quantum computation, examines the **measurement process** and state collapse, and culminates with fundamental constraints like the **no-cloning theorem**. Mastering these mathematical foundations is essential for understanding how quantum information is encoded, manipulated, and extracted in quantum algorithms and protocols.

---

# **Chapter 2: Outline**

| **Sec.** | **Title**                                  | **Core Ideas & Examples**                                                                                                                                                |
| -------- | ------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **2.1**  | **Quantum State Vectors and Dirac Notation** | Ket and bra vectors; inner and outer products; projection operators; multi-qubit basis states; tensor product structure; orthogonality and normalization.              |
| **2.2**  | **Density Matrices and Mixed States**      | Pure vs mixed states; statistical ensembles; Hermitian, positive semidefinite, unit trace properties; idempotence condition; linear entropy; open quantum systems.     |
| **2.3**  | **Unitary Operators and Evolution**        | Unitary condition $U^\dagger U = I$; norm preservation and reversibility; Hamiltonian evolution $e^{-iHt/\hbar}$; Pauli gates, Hadamard, rotation gates.                |
| **2.4**  | **Measurement and Collapse**               | Born rule and probabilistic outcomes; measurement operators; state collapse and normalization; projective measurement; computational basis measurements.                |
| **2.5**  | **No-Cloning Theorem**                     | Impossibility of universal quantum cloning; proof by inner product preservation; implications for error correction and information flow; quantum vs classical copying. |

---

## **2.1 Quantum State Vectors and Dirac Notation**

---

The foundation of quantum computing lies in the rigorous mathematical description of state and operation using linear algebra over complex numbers. The standard language for this description is the **Dirac notation**, also known as the bra-ket notation, which elegantly captures the concepts of vectors, their duals, and products in a Hilbert space.

!!! tip "Key Insight"
    Dirac notation provides a compact, powerful formalism that unifies state representation, operations, and measurements into a single coherent mathematical language.
    
### **The Ket Vector and the State**

The state of a closed quantum system is represented by a vector, $|\psi\rangle$, residing in a complex **Hilbert space** $\mathcal{H}$ (Postulate I). This is known as the **ket vector**.

* **Qubit Representation:** For a single qubit in the computational basis $\{|0\rangle, |1\rangle\}$, the ket is written as a linear superposition:
```
$$
|\psi\rangle = \alpha|0\rangle + \beta|1\rangle = \begin{pmatrix} \alpha \\ \beta \end{pmatrix}
$$
where $\alpha$ and $\beta$ are complex **probability amplitudes**.

```
* **Normalization:** For $|\psi\rangle$ to represent a physically valid state, it must be a unit vector, ensuring that the total probability of measurement outcomes is one:
```
$$
\langle\psi|\psi\rangle = |\alpha|^2 + |\beta|^2 = 1
$$

```
### **The Bra Vector and the Inner Product**

The **bra vector**, $\langle\psi|$, is the Hermitian conjugate (or conjugate transpose) of the ket $|\psi\rangle$. This is a row vector that belongs to the dual space $\mathcal{H}^*$.

* **Conjugate Transpose:** If $|\psi\rangle = \begin{pmatrix} \alpha \\ \beta \end{pmatrix}$, then the bra is $\langle\psi| = \begin{pmatrix} \alpha^* & \beta^* \end{pmatrix}$, where the asterisk denotes complex conjugation.

The **inner product** $\langle\phi|\psi\rangle$ is the standard dot product between the bra $\langle\phi|$ and the ket $|\psi\rangle$.

* **Result:** The inner product is a **complex number** (a scalar) that quantifies the geometric **overlap** between the two state vectors.
* **Orthogonality:** If $\langle\phi|\psi\rangle = 0$, the two states are **orthogonal**. The computational basis states are mutually orthogonal: $\langle 0|1\rangle = 0$.
* **Probability:** The inner product is central to the **Born Rule** (Postulate III); the probability of measuring state $|\psi\rangle$ in the basis state $|0\rangle$ is $P(0) = |\langle 0|\psi\rangle|^2$.

!!! example "Inner Product Calculation"
    For $|\psi\rangle = \frac{1}{\sqrt{2}}(|0\rangle + |1\rangle)$ and $|\phi\rangle = |0\rangle$:
    
    $$\langle\phi|\psi\rangle = \langle 0|\left(\frac{1}{\sqrt{2}}(|0\rangle + |1\rangle)\right) = \frac{1}{\sqrt{2}}$$
    
    The probability of measuring $|0\rangle$ is $P(0) = |\langle 0|\psi\rangle|^2 = \frac{1}{2}$.
    
### **The Outer Product and Operators**

The **outer product** $|\psi\rangle\langle\phi|$ is the product of the column vector $|\psi\rangle$ and the row vector $\langle\phi|$.

* **Result:** The outer product results in a square **matrix**. In quantum mechanics, these matrices represent **operators** (such as gates or projection operators).
* **Projection Operators:** For a normalized state $|\psi\rangle$, the outer product $P = |\psi\rangle\langle\psi|$ is a **projection operator** that projects any arbitrary state onto the line spanned by $|\psi\rangle$. Projection operators are crucial in formally defining the measurement process.
* **Identity Operator:** The identity operator $I$ for a single qubit can be written as the sum of the outer products of the basis states:

```
$$
I = |0\rangle\langle 0| + |1\rangle\langle 1| = \begin{pmatrix} 1 & 0 \\ 0 & 1 \end{pmatrix}
$$

```
!!! tip "Key Insight"
    Outer products convert states into operators. This is how measurement projectors and density matrices are constructed from state vectors.
    
### **Multi-Qubit Systems and Basis States**

For a system of $N$ qubits, the state space is the tensor product of $N$ copies of $\mathcal{H}^2$ (Postulate IV).

* **Basis States:** The basis states of the composite system are formed by the tensor products of the individual basis states, e.g., for two qubits: $|00\rangle, |01\rangle, |10\rangle, |11\rangle$.
* **Example State:** A general two-qubit state $|\Psi\rangle$ is written in Dirac notation as:
```
$$
|\Psi\rangle = \alpha_{00}|00\rangle + \alpha_{01}|01\rangle + \alpha_{10}|10\rangle + \alpha_{11}|11\rangle
$$
where $\sum_{ij} |\alpha_{ij}|^2 = 1$. The corresponding column vector in the standard four-dimensional basis is $\begin{pmatrix} \alpha_{00} \\ \alpha_{01} \\ \alpha_{10} \\ \alpha_{11} \end{pmatrix}$. This exponential growth of the basis set is why $N$ qubits can manage $2^N$ complex probability amplitudes simultaneously.

```
---

## **2.2 Density Matrices and Mixed States**

---

While the state vector, $|\psi\rangle$, successfully describes a system in a **pure state** (Postulate I), this representation is insufficient when the state of the system is not known with certainty. To address this classical uncertainty over a collection of quantum states, the formalism of the **density matrix** ($\rho$) is introduced.

### **The Necessity of the Density Matrix**

A quantum system is in a **pure state** if it is described by a single, normalized state vector $|\psi\rangle$. However, in many physical and computational scenarios, the system is in a **mixed state**, meaning we have classical uncertainty, or **classical ignorance**, about which pure state the system is actually in.

- **Mixed State:** A mixed state is a statistical ensemble $\mathcal{E}$ of quantum states, where the system is in state $|\psi_i\rangle$ with classical probability $p_i$, and $\sum_i p_i = 1$. Since this ensemble cannot be represented by a single state vector $|\Psi\rangle$ (which would imply a superposition), the density matrix is required to incorporate these classical probabilities.

!!! tip "Key Insight"
    The density matrix is essential for describing **open quantum systems** that interact with an environment, or subsystems of entangled states where classical uncertainty is unavoidable.
    
### **Formal Definition and Properties**

The **density matrix** $\rho$ for a general mixed state (statistical ensemble) is defined by the convex combination of the outer products of its constituent pure states:

$$
\rho = \sum_i p_i |\psi_i\rangle\langle\psi_i|, \quad \text{with } \sum_i p_i = 1 \text{ and } p_i \ge 0
$$

The density matrix $\rho$ is a fundamental object in the Hilbert space that must satisfy three essential mathematical properties:

1. **Hermitian:** The matrix must be equal to its own conjugate transpose: $\rho^\dagger = \rho$. This ensures that all eigenvalues are real, consistent with the fact that probability amplitudes should lead to real measurement probabilities.

2. **Positive Semidefinite:** All eigenvalues of $\rho$ must be non-negative. This is required because $\rho$ represents probabilities and mixtures thereof.

3. **Unit Trace:** The sum of the diagonal elements (the trace) must be unity: $\mathrm{Tr}(\rho) = 1$. This property reflects the overall normalization condition that the total probability of finding the system in *any* state must be 1.

!!! example "Maximally Mixed State"
    For a single qubit, the maximally mixed state represents complete classical uncertainty:
    
    $$\rho_{\text{mixed}} = \frac{1}{2}|0\rangle\langle 0| + \frac{1}{2}|1\rangle\langle 1| = \frac{1}{2}\begin{pmatrix} 1 & 0 \\ 0 & 1 \end{pmatrix} = \frac{I}{2}$$
    
    This state has equal probability of being $|0\rangle$ or $|1\rangle$, and measurement yields each outcome with 50% probability.
    
### **Distinguishing Pure and Mixed States**

The density matrix formalism provides a single, unified mathematical object to describe both pure and mixed states. They are distinguished by the condition of **idempotence** ($\rho^2 = \rho$):

- **Pure State:** For a pure state $|\psi\rangle$, the density matrix is simply

  $$
  \rho_{\text{pure}} = |\psi\rangle\langle\psi|
  $$

  It satisfies the condition:

  $$
  \rho_{\text{pure}}^2 = \rho_{\text{pure}}
  $$

  A pure state has exactly one non-zero eigenvalue (equal to 1).

- **Mixed State:** For a statistical mixture, the density matrix does **not** satisfy the idempotence condition:

  $$
  \rho_{\text{mixed}}^2 \neq \rho_{\text{mixed}}
  $$

  A mixed state has multiple non-zero eigenvalues, reflecting the classical uncertainty over multiple component states. The degree of "mixedness" is often quantified by the **linear entropy**:

  $$
  S_L = 1 - \mathrm{Tr}(\rho^2)
  $$

??? question "How does the density matrix describe entangled subsystems?"
    When tracing out part of an entangled system, the remaining subsystem's density matrix is typically mixed, even if the total system is in a pure state. This is why density matrices are essential for quantum information theory.
    
    The density matrix is thus a powerful and essential tool, particularly when dealing with **open quantum systems** (systems interacting with an environment) or when describing subsystems of an entangled state, where the state of the subsystem is invariably mixed.
    
---

## **2.3 Unitary Operators and Evolution**

---

The evolution of a **closed quantum system** is fundamentally governed by the second postulate of quantum mechanics, which states that any such change must be achieved via a **unitary transformation**. These transformations are the building blocks of quantum computation, represented mathematically by **unitary operators** or **quantum gates**.

!!! tip "Key Insight"
    Unitary evolution is the only physically allowed transformation of a closed quantum system. All quantum gates must be unitary, ensuring reversibility and probability conservation.
    
### **Definition and Properties of Unitary Operators**

An operator (matrix) $U$ acting on a state vector $|\psi\rangle$ is **unitary** if it satisfies the condition:

$$
U^\dagger U = U U^\dagger = I
$$

where $U^\dagger$ is the Hermitian conjugate (conjugate transpose) of $U$, and $I$ is the identity matrix. The resulting state $|\psi'\rangle$ after the operation is simply $|\psi'\rangle = U|\psi\rangle$.

The unitary condition $U^\dagger U = I$ guarantees two crucial physical properties of quantum evolution:

- **Norm Preservation:** Unitary operators **preserve the norm** (length) of the state vector,
  
  $$
  \langle\psi'|\psi'\rangle = \langle\psi|U^\dagger U|\psi\rangle = \langle\psi|I|\psi\rangle = \langle\psi|\psi\rangle
  $$

  Since the square of the norm represents the total probability of the system, this ensures that **total probability remains unity** after any transformation.

- **Reversibility:** Every unitary operation is inherently **reversible**. Because $U^\dagger U = I$, the inverse of the transformation is simply $U^{-1} = U^\dagger$. This means the original state $|\psi\rangle$ can always be perfectly recovered from the final state $|\psi'\rangle$ by applying the inverse operation $U^\dagger$.

!!! example "Verifying Unitarity: Pauli X Gate"
    The Pauli X gate (quantum NOT) is:
    
    $$X = \begin{pmatrix} 0 & 1 \\ 1 & 0 \end{pmatrix}$$
    
    We verify: $X^\dagger X = X \cdot X = \begin{pmatrix} 1 & 0 \\ 0 & 1 \end{pmatrix} = I$. Also, $X^2 = I$, so X is its own inverse.
    
### **Time Evolution and the Hamiltonian**

In continuous time, the unitary evolution of a system is generated by its **Hamiltonian** ($H$) (Postulate II). Since the Hamiltonian is an observable associated with the system's energy, it must be a **Hermitian operator** ($H = H^\dagger$).

The unitary time evolution operator $U(t)$ that governs the change of the state vector $|\psi(t)\rangle$ over time $t$ is given by:

$$
U(t) = e^{-iHt/\hbar}
$$

where $\hbar$ is the reduced Planck constant. The function $e^{-iHt/\hbar}$ is defined by its Taylor series expansion. The fact that $H$ is Hermitian ensures that $U(t)$ is unitary, $U(t)^\dagger = U(-t)$, which is necessary for consistent physical evolution.

### **Examples in Quantum Computing**

Unitary operators form the gates of a quantum circuit. Common examples include:

- **Pauli Matrices:** $X$, $Y$, and $Z$ gates, which are also Hermitian. For instance, the Pauli $X$ matrix (quantum NOT gate) is

  $$
  X = \begin{pmatrix} 0 & 1 \\ 1 & 0 \end{pmatrix}
  $$

  which satisfies $X^2 = I$ and $X^\dagger = X$.

- **Hadamard Gate ($H$):** A key gate for creating superposition.

- **Rotation Gates:** General single-qubit rotations about the coordinate axes, $R_x(\theta)$, $R_y(\theta)$, and $R_z(\theta)$.

??? question "Why must quantum gates be reversible?"
    Unitarity ensures reversibility because $U^{-1} = U^\dagger$ always exists. This is required by fundamental physics—information cannot be destroyed in a closed quantum system, only transformed. Irreversible gates would violate probability conservation and energy conservation.
    
---

## **2.4 Measurement and Collapse**

---

Quantum evolution is smooth and unitary, but the act of observing the system—the **measurement**—is an irreversible, non-unitary process that yields a classical outcome. This process is governed by Postulate III, known as the **Measurement Postulate** or the **Born Rule**.

!!! tip "Key Insight"
    Measurement is the bridge between the quantum and classical worlds. It irreversibly extracts classical information from quantum superposition, collapsing the state in the process.
    
### **Probabilistic Outcomes (The Born Rule)**

When a measurement is performed on a quantum state, the outcome is **probabilistic**.

For a single qubit state measured in the computational basis:

$$
|\psi\rangle = \alpha|0\rangle + \beta|1\rangle
$$

The probability of obtaining outcome 0 is:

$$
P(0) = |\alpha|^2
$$

and the probability of obtaining outcome 1 is:

$$
P(1) = |\beta|^2
$$

These probabilities sum to one:

$$
P(0) + P(1) = |\alpha|^2 + |\beta|^2 = 1
$$

due to the state normalization.

!!! example "Measurement Probability Calculation"
    For the state $|\psi\rangle = \frac{1}{2}|0\rangle + \frac{\sqrt{3}}{2}|1\rangle$:
    
    - Probability of measuring $|0\rangle$: $P(0) = |\frac{1}{2}|^2 = \frac{1}{4} = 25\%$
    - Probability of measuring $|1\rangle$: $P(1) = |\frac{\sqrt{3}}{2}|^2 = \frac{3}{4} = 75\%$
    
    After measurement, the superposition is destroyed and the state becomes either $|0\rangle$ or $|1\rangle$ with these probabilities.
    
### **State Collapse and Operators**

The general framework for measurement involves **measurement operators** $M_i$ associated with the $i$-th possible outcome.

- **Probability:** The probability of observing outcome $i$ is given by:

  $$
  P(i) = \langle \psi | M_i^\dagger M_i | \psi \rangle
  $$

- **State Collapse:** If outcome $i$ is observed, the state of the system **instantaneously collapses** to the normalized post-measurement state:

  $$
  |\psi'\rangle = \frac{M_i|\psi\rangle}{\sqrt{P(i)}}
  $$

The term $\sqrt{P(i)}$ in the denominator acts as a **normalization factor** that scales the new state vector back to unit length, satisfying the normalization postulate after the collapse occurs.

In the common case of projective measurement onto the computational basis, the measurement operators are the projectors:

$$
M_0 = |0\rangle\langle 0|, \quad M_1 = |1\rangle\langle 1|
$$

??? question "Is measurement collapse instantaneous everywhere?"
    The collapse is instantaneous in the mathematical formalism, but this doesn't allow faster-than-light communication. The collapse affects correlated measurement statistics but cannot transmit information without a classical channel to compare results.
    
---

## **2.5 No-Cloning Theorem**

---

The **No-cloning theorem** is a fundamental constraint in quantum information that distinguishes it sharply from classical information.

!!! tip "Key Insight"
    The no-cloning theorem is not a technological limitation—it's a fundamental law of quantum mechanics arising from the linearity of unitary evolution. You cannot copy what you don't know.
    
### **Statement and Proof Sketch**

**Statement:** It is impossible to construct a universal quantum operation that can create an identical copy of an **arbitrary unknown quantum state**.

**Proof Sketch (by contradiction):** Assume a universal cloning unitary operator $U$ exists. Let $|0\rangle_T$ be an ancilla target state, and $|\psi\rangle$ and $|\phi\rangle$ be two arbitrary, unknown quantum states. The cloning operation must work for both states:

$$
U|\psi\rangle|0\rangle_T = |\psi\rangle|\psi\rangle \quad \text{and} \quad U|\phi\rangle|0\rangle_T = |\phi\rangle|\phi\rangle
$$

Since $U$ is unitary, it must preserve the inner product between the initial states and the final states.

Initial inner product:

$$
\langle \psi | \phi \rangle \langle 0 | 0 \rangle_T = \langle \psi | \phi \rangle
$$

Final inner product:

$$
\langle \psi | \phi \rangle \langle \psi | \phi \rangle = (\langle \psi | \phi \rangle)^2
$$

Equating both sides:

$$
\langle \psi | \phi \rangle = (\langle \psi | \phi \rangle)^2
$$

This equality holds *only* if $\langle \psi | \phi \rangle = 0$ (orthogonal states) or $\langle \psi | \phi \rangle = 1$ (identical states). Since quantum states can have arbitrary overlaps, the assumption that a universal $U$ exists leads to a contradiction. Therefore, no such universal cloning unitary exists.

!!! example "Why Classical Copying Works"
    Classical bits can be copied because they are in definite states (0 or 1). A classical COPY operation:
    
    $$\text{COPY}(0, 0) = (0, 0) \quad \text{and} \quad \text{COPY}(1, 0) = (1, 1)$$
    
    works perfectly because there's no superposition to preserve. Quantum superpositions $\alpha|0\rangle + \beta|1\rangle$ contain information in the complex amplitudes that cannot be extracted without measurement (which destroys the superposition).
    
### **Practical Implications**

The theorem is a consequence of the **linearity (unitary nature)** of quantum operators and has profound implications:

- **Error Correction:** It prevents the simple replication of quantum data for backup. As a result, **Quantum Error Correction (QEC)** must rely on encoding information redundantly across multiple entangled qubits to protect against decoherence, rather than direct state comparison.

- **Information Flow:** It ensures that the complex probability amplitudes contained within a superposition state cannot be fully extracted or replicated without perturbing or collapsing the state.

??? question "Can we clone known quantum states?"
    Yes! If you know the exact state (e.g., $|0\rangle$ or $|+\rangle$), you can prepare as many copies as you want. The no-cloning theorem only forbids copying *arbitrary unknown* states. This is why quantum key distribution protocols like BB84 are secure—eavesdroppers cannot copy unknown quantum states without detection.
    
---