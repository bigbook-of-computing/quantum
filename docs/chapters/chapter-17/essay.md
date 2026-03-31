# **Chapter 17: Quantum Chemistry**

---

# **Introduction**

**Quantum chemistry** — the application of quantum mechanics to predict molecular structure, reaction energies, and spectroscopic properties — is the domain where quantum computers are expected to deliver their earliest industrially valuable advantage. The central challenge is the **electronic structure problem**: finding the ground-state energy and wavefunction of a molecule by solving the many-body electronic Schrödinger equation. Classical algorithms like Coupled Cluster with Singles, Doubles, and Perturbative Triples (CCSD(T)) are highly accurate for small molecules but scale as $O(N^7)$ in the number of basis functions, rendering them computationally prohibitive for molecules with more than ~50 heavy atoms.

Quantum computers approach this problem differently. By encoding the electronic wavefunction directly in the qubit register — where a $2^n$-dimensional Hilbert space emerges naturally from $n$ qubits — quantum devices can, in principle, represent and evolve electronic structures with polynomial circuit overhead. The **Variational Quantum Eigensolver (VQE)** uses a hybrid quantum-classical loop to estimate ground state energies on NISQ devices, while fault-tolerant approaches using **Quantum Phase Estimation (QPE)** promise exponential speedup over CCSD(T) for chemically relevant problems.

This chapter builds a rigorous foundation for quantum chemistry simulation. We develop the first and second quantization formalisms, construct the electronic Hamiltonian, and study how fermionic operators are mapped to qubit operators via the Jordan-Wigner and Bravyi-Kitaev transformations introduced in Chapter 16. We then examine practical VQE workflows for small molecules and discuss the path toward fault-tolerant quantum chemistry [1, 2].

---

# **Chapter 17: Outline**

| **Sec.** | **Title** | **Core Ideas & Examples** |
| :--- | :--- | :--- |
| **17.1** | First vs Second Quantization | Wavefunction ansatz, Slater determinants, occupation number representation, Fock space |
| **17.2** | Fermionic Fock Space and Operators | Creation/annihilation operators, number operator, anti-commutation, Normal ordering |
| **17.3** | The Electronic Hamiltonian and Qubit Mapping | Born-Oppenheimer approximation, one- and two-electron integrals, JW/BK mapping, VQE workflow |

---

## **17.1 First vs Second Quantization**

---

Electronic structure theory can be formulated in two equivalent but practically distinct mathematical languages: **first quantization** (many-body wavefunction) and **second quantization** (occupation number representation). Each has distinct advantages for quantum computing.

### **First Quantization: Many-Body Wavefunction**

---

In first quantization, the $N$-electron state is a wavefunction in $3N$-dimensional real space (plus spin):

$$
\Psi(\vec{r}_1, \sigma_1; \vec{r}_2, \sigma_2; \ldots; \vec{r}_N, \sigma_N)
$$

Since electrons are **indistinguishable fermions**, $\Psi$ must be antisymmetric under particle exchange:

$$
\Psi(\ldots, \vec{r}_i, \sigma_i; \ldots, \vec{r}_j, \sigma_j; \ldots) = -\Psi(\ldots, \vec{r}_j, \sigma_j; \ldots, \vec{r}_i, \sigma_i; \ldots)
$$

The simplest antisymmetric many-body wavefunction is a **Slater determinant** — a single antisymmetrized product of one-electron orbitals $\phi_i(\vec{r}, \sigma)$:

$$
\Psi_{\text{SD}} = \frac{1}{\sqrt{N!}} \det\begin{pmatrix}
\phi_1(\vec{r}_1) & \phi_2(\vec{r}_1) & \cdots & \phi_N(\vec{r}_1) \\
\phi_1(\vec{r}_2) & \phi_2(\vec{r}_2) & \cdots & \phi_N(\vec{r}_2) \\
\vdots & & \ddots & \vdots \\
\phi_1(\vec{r}_N) & \phi_2(\vec{r}_N) & \cdots & \phi_N(\vec{r}_N)
\end{pmatrix}
$$

The Hartree-Fock approximation finds the single Slater determinant that minimises the electronic energy. Correlation methods (CISD, MP2, CCSD) add perturbative corrections.

!!! tip "First Quantization on Quantum Computers"
    First quantization on quantum computers represents electronic positions on a 3D spatial grid, using $O(\log N + \log(1/\epsilon))$ qubits per electron. Recent proposals by Babbush et al. show first-quantized quantum simulation requires fewer qubits than second-quantized approaches for large molecules, making it promising for fault-tolerant hardware.
    
### **Second Quantization: Occupation Number Representation**

---

In second quantization, rather than tracking which orbital each electron occupies, we count **how many electrons occupy each orbital**. For $M$ spin-orbitals $\{\phi_p\}$, the basis states are occupation-number vectors:

$$
|n_0, n_1, n_2, \ldots, n_{M-1}\rangle, \quad n_p \in \{0, 1\}
$$

where $n_p = 1$ means orbital $\phi_p$ is occupied and $n_p = 0$ means it is empty. The full **many-body Hilbert space** (Fock space of $M$ orbitals) has dimension $2^M$, mapping naturally to $M$ qubits.

!!! example "H₂ Occupation Number Basis"
    For H₂ in the STO-3G basis, there are $M = 4$ spin-orbitals (2 spatial orbitals × 2 spins). The $2^4 = 16$ Fock states span from the vacuum $|0000\rangle$ to the fully occupied $|1111\rangle$. The physical 2-electron sector contains $\binom{4}{2} = 6$ states.
    
??? question "Why does the number of qubits needed for second quantization scale with the number of orbitals and not the number of electrons?"
    In second quantization, each qubit represents one spin-orbital's occupancy (empty or occupied), independently of how many electrons are in the system. Encoding $M$ molecular spin-orbitals therefore requires exactly $M$ qubits. In contrast, first-quantized simulation assigns $n \sim \log(M)$ qubits per electron, favouring first-quantization for large electron numbers.
    
---

## **17.2 Fermionic Fock Space and Operators**

---

### **Creation and Annihilation Operators**

---

The algebraic engine of second quantization is the pair of **fermionic creation and annihilation operators** $a_p^\dagger$ and $a_p$ for spin-orbital $p$:

$$
a_p^\dagger |n_0, \ldots, n_p = 0, \ldots\rangle = (-1)^{S_p} |n_0, \ldots, n_p = 1, \ldots\rangle
$$
$$
a_p |n_0, \ldots, n_p = 1, \ldots\rangle = (-1)^{S_p} |n_0, \ldots, n_p = 0, \ldots\rangle
$$

where the **parity sign** $(-1)^{S_p} = (-1)^{\sum_{k<p} n_k}$ counts the number of electrons in orbitals below $p$, enforcing fermionic anti-symmetry.

The **anti-commutation relations** are fundamental:

$$
\{a_p, a_q^\dagger\} = a_p a_q^\dagger + a_q^\dagger a_p = \delta_{pq}
$$
$$
\{a_p, a_q\} = \{a_p^\dagger, a_q^\dagger\} = 0
$$

These relations encode the Pauli exclusion principle: $a_p^\dagger a_p^\dagger = 0$ (cannot create two electrons in the same spin-orbital).

!!! tip "Anti-commutation vs Commutation"
    Bosons satisfy **commutation** relations $[b_p, b_q^\dagger] = \delta_{pq}$, allowing multiple occupation. Fermions satisfy **anti-commutation** $\{a_p, a_q^\dagger\} = \delta_{pq}$, enforcing single occupancy. The sign difference between these algebras is what makes fermionic quantum simulation non-trivial on a qubit register.
    
### **The Number Operator and Normal Ordering**

---

The **number operator** $\hat{n}_p = a_p^\dagger a_p$ counts the occupation of orbital $p$:

$$
\hat{n}_p |n_0, \ldots, n_p, \ldots\rangle = n_p |n_0, \ldots, n_p, \ldots\rangle
$$

The **total electron number operator** $\hat{N} = \sum_p \hat{n}_p$ commutes with every Hamiltonian conserving particle number, providing a useful symmetry constraint for circuit design (fixing the number of electrons in the quantum state).

**Normal ordering** arranges operators with all $a_p^\dagger$ to the left of all $a_q$, providing a canonical form for computing matrix elements and implementing operator measurements.

!!! example "Expectation Value of the Number Operator"
    For the H₂ state $|\psi\rangle = 0.99|0011\rangle + 0.14|0110\rangle - 0.04|1001\rangle$:
    $$\langle \hat{N} \rangle = 0.99^2 \cdot 2 + 0.14^2 \cdot 2 + 0.04^2 \cdot 2 \approx 2.0$$
    as expected for a 2-electron system. Individual orbital occupancies reveal the electron distribution across the molecule.
    
---

## **17.3 The Electronic Hamiltonian and Qubit Mapping**

---

### **The Born-Oppenheimer Hamiltonian**

---

Under the **Born-Oppenheimer approximation** (nuclei are stationary on the timescale of electronic motion), the electronic Hamiltonian in second quantization is:

$$
H_{\text{elec}} = \sum_{pq} h_{pq} a_p^\dagger a_q + \frac{1}{2}\sum_{pqrs} g_{pqrs} a_p^\dagger a_q^\dagger a_r a_s + V_{\text{nuc}}
$$

The **one-electron integrals** $h_{pq}$ encode kinetic energy and electron-nucleus attraction:

$$
h_{pq} = \int \phi_p^*(\vec{r})\left[-\frac{\nabla^2}{2} - \sum_A \frac{Z_A}{|\vec{r}-\vec{R}_A|}\right]\phi_q(\vec{r})\,d\vec{r}
$$

The **two-electron integrals** $g_{pqrs}$ encode electron-electron repulsion:

$$
g_{pqrs} = \int\int \frac{\phi_p^*(\vec{r}_1)\phi_q^*(\vec{r}_2)\phi_r(\vec{r}_2)\phi_s(\vec{r}_1)}{|\vec{r}_1 - \vec{r}_2|}\,d\vec{r}_1 d\vec{r}_2
$$

These integrals are computed classically using quantum chemistry packages (PySCF, PSI4, OpenFermion) before encoding onto quantum hardware.

!!! tip "Number of Hamiltonian Terms"
    A molecule with $M$ spin-orbitals has $O(M^4)$ two-electron integrals. For H₂ in STO-3G ($M=4$): 256 integrals, most zero by symmetry → ~5 unique Pauli terms. For larger molecules (e.g., FeMo-cofactor, $M \approx 50$-$100$): millions of terms, requiring efficient grouping strategies for measurement.
    
### **VQE Workflow for Molecular Systems**

---

The complete VQE pipeline for quantum chemistry involves:

```mermaid
graph LR
    A[Molecule Geometry] --> B[Classical Integral Calculation<br>PySCF/OpenFermion]
    B --> C[Jordan-Wigner/BK Mapping<br>Fermionic → Qubit Hamiltonian]
    C --> D[Taper Symmetries<br>Reduce qubit count]
    D --> E[Ansatz Selection<br>UCCSD/Hardware-Efficient]
    E --> F[VQE Optimization Loop<br>Quantum Hardware]
    F --> G[Energy Convergence<br>E₀ Ground State]
```

**Step 1: Classical preprocessing** — compute $h_{pq}$, $g_{pqrs}$ using Hartree-Fock orbitals as basis

**Step 2: Qubit mapping** — apply Jordan-Wigner (JW) or Bravyi-Kitaev (BK) transformation to convert fermionic Hamiltonian to Pauli operators

**Step 3: Symmetry tapering** — use molecular symmetries ($Z_2$ symmetries, particle-number conservation, spin symmetry) to reduce qubit count by 2–4 qubits without approximation

**Step 4: Ansatz** — **UCCSD** (Unitary Coupled Cluster Singles and Doubles) is chemically motivated; hardware-efficient ansätze (two-local, RealAmplitudes) are noise-optimal but less physically motivated

**Step 5: VQE loop** — evaluate $\langle H \rangle$ on quantum hardware, classically optimize circuit parameters

!!! example "H₂ Ground-State Energy with VQE"
    For H₂ at bond length 0.735 Å in STO-3G basis: after JW mapping and symmetry reduction, the effective Hamiltonian is 2-qubit. UCCSD with a single parameter achieves chemical accuracy (~1 mHartree) in ~20 optimizer iterations, matching CCSD(T) exactly for this two-electron system.
    
### **Comparison of Qubit Mappings**

---

| Mapping | String Length | Total Pauli Weight | Qubit Count | Notes |
| :--- | :--- | :--- | :--- | :--- |
| **Jordan-Wigner** | $O(M)$ | $O(M^4)$ | $M$ | Simplest; non-local for distant orbitals |
| **Bravyi-Kitaev** | $O(\log M)$ | $O(M^4 \log M)$ | $M$ | Logarithmic locality; better depth |
| **Parity Mapping** | $O(M)$ | $O(M^4)$ | $M - 2$ | Can taper 2 qubits by symmetry |
| **BK Superfast** | $O(1)$ (local) | $O(M^5)$ | $O(M)$ | Constant locality; higher term count |

??? question "Can VQE achieve exact ground state energies, or are there fundamental accuracy limits?"
    VQE is exact in the limit of a complete ansatz — a circuit with enough expressibility to represent the exact ground state wavefunction. In practice, UCCSD is exact for two-electron systems (H₂) but approximate for larger ones (the truncation to singles and doubles introduces error). Hardware noise introduces a further accuracy floor: current NISQ devices typically achieve 1–10 mHartree accuracy for small molecules, comparable to HF but below chemical accuracy (~1 mHartree) for most cases.
    
---

## **References**

[1] Aspuru-Guzik, A., et al. (2005). *Simulated quantum computation of molecular energies*. Science, 309(5741), 1704–1707.

[2] McArdle, S., et al. (2020). *Quantum computational chemistry*. Reviews of Modern Physics, 92(1), 015003.

[3] Bravyi, S. B., & Kitaev, A. Y. (2002). *Fermionic quantum computation*. Annals of Physics, 298(1), 210–226.