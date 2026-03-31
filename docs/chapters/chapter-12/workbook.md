# **Chapter 12: Quantum Unsupervised Learning (Workbook)**

---

> **Summary:** This chapter explores quantum approaches to unsupervised learning, focusing on how quantum mechanics can address the computational bottlenecks of classical algorithms. We examine Quantum Principal Component Analysis (qPCA) for exponential speedup in dimensionality reduction, Quantum k-means for accelerated clustering, and Quantum Boltzmann Machines (QBMs) for modeling complex probability distributions. By surveying these core paradigms, the chapter provides insight into the potential for quantum advantage in pattern discovery and exploratory data analysis from unlabeled datasets.

---

The goal of this chapter is to establish concepts in Unsupervised Quantum Machine Learning, exploring how quantum computing can enhance traditional unsupervised learning frameworks.

---

## **12.1 Quantum Principal Component Analysis** {.heading-with-pill}

> **Difficulty:** ★★★★☆
> 
> **Concept:** Quantum Dimensionality Reduction
> 
> **Summary:** Quantum Principal Component Analysis (qPCA) offers an exponential speedup for finding the principal components of a dataset by diagonalizing the data's density matrix using Quantum Phase Estimation, bypassing the costly classical matrix diagonalization bottleneck.

---

### **Theoretical Background**

Principal Component Analysis (PCA) is a fundamental technique for dimensionality reduction that identifies the directions of maximum variance in high-dimensional data. Quantum Principal Component Analysis (qPCA) reformulates this classical linear algebra problem to achieve exponential speedup under specific conditions.

**Classical PCA Foundation:**

Given dataset $\mathcal{D} = \{\mathbf{x}_i\}_{i=1}^N$ with $\mathbf{x}_i \in \mathbb{R}^d$, define the empirical mean and covariance:

**Mean:**
$$
\mathbf{\mu} = \frac{1}{N}\sum_{i=1}^N \mathbf{x}_i
$$

**Covariance Matrix:**
$$
\mathbf{C} = \frac{1}{N}\sum_{i=1}^N (\mathbf{x}_i - \mathbf{\mu})(\mathbf{x}_i - \mathbf{\mu})^T \in \mathbb{R}^{d \times d}
$$

Symmetric positive semi-definite: $\mathbf{C} = \mathbf{C}^T$, $\mathbf{v}^T\mathbf{C}\mathbf{v} \geq 0$ for all $\mathbf{v}$.

**Eigendecomposition:**
$$
\mathbf{C}\mathbf{v}_j = \lambda_j \mathbf{v}_j, \quad j = 1,\ldots,d
$$

where $\lambda_1 \geq \lambda_2 \geq \cdots \geq \lambda_d \geq 0$ are eigenvalues (variances) and $\{\mathbf{v}_j\}$ are orthonormal eigenvectors (principal components).

**Projection to $k$ Dimensions:**  
Retain top $k$ components:

$$
\mathbf{x}_{\text{reduced}} = \mathbf{V}_k^T (\mathbf{x} - \mathbf{\mu})
$$

where $\mathbf{V}_k = [\mathbf{v}_1 | \cdots | \mathbf{v}_k] \in \mathbb{R}^{d \times k}$.

**Reconstruction:**
$$
\mathbf{x}_{\text{recon}} = \mathbf{V}_k \mathbf{x}_{\text{reduced}} + \mathbf{\mu}
$$

**Variance Captured:**
$$
\frac{\sum_{j=1}^k \lambda_j}{\sum_{j=1}^d \lambda_j}
$$

**Classical Complexity:**
- Covariance computation: $\mathcal{O}(Nd^2)$  
- Eigendecomposition: $\mathcal{O}(d^3)$ (full), $\mathcal{O}(kd^2)$ (top-$k$ iterative)  
- Total: $\mathcal{O}(Nd^2 + d^3)$

For $d \gg 1$, the cubic scaling becomes prohibitive.

**Quantum Density Matrix Formulation:**

Encode data into quantum density matrix:

$$
\rho = \frac{1}{N}\sum_{i=1}^N |\psi_i\rangle\langle\psi_i|
$$

where $|\psi_i\rangle$ encodes data point $\mathbf{x}_i$.

**Amplitude Encoding:**  
For normalized $\mathbf{x}_i \in \mathbb{R}^{2^n}$:

$$
|\psi_i\rangle = \sum_{j=0}^{2^n-1} x_{i,j} |j\rangle, \quad \sum_j x_{i,j}^2 = 1
$$

Requires $n = \log_2 d$ qubits.

**Density Matrix Properties:**

1. **Hermitian:** $\rho = \rho^\dagger$  
2. **Positive semi-definite:** $\langle\phi|\rho|\phi\rangle \geq 0$ for all $|\phi\rangle$  
3. **Trace normalization:** $\text{Tr}(\rho) = 1$  
4. **Spectral decomposition:**

$$
\rho = \sum_{j=1}^{2^n} \lambda_j |v_j\rangle\langle v_j|, \quad \lambda_j \geq 0, \quad \sum_j \lambda_j = 1
$$

Eigenvalues $\{\lambda_j\}$ encode variance information; eigenvectors $\{|v_j\rangle\}$ are principal quantum components.

**Connection to Classical Covariance:**

For amplitude-encoded centered data, the density matrix approximates:

$$
\rho \approx \frac{1}{\|\mathbf{C}\|_F} \mathbf{C}
$$

where $\|\mathbf{C}\|_F = \sqrt{\sum_{ij} C_{ij}^2}$ is Frobenius norm.

**Quantum Phase Estimation for Eigenvalues:**

**Unitary Exponentiation:**  
Simulate Hamiltonian evolution:

$$
U = e^{-i\rho t}
$$

for time parameter $t$. Shares eigenvectors with $\rho$:

$$
\rho |v_j\rangle = \lambda_j |v_j\rangle \quad \Rightarrow \quad U|v_j\rangle = e^{-i\lambda_j t}|v_j\rangle
$$

**Quantum Phase Estimation (QPE):**

Input: $|v_j\rangle$ (eigenvector), oracle for $U = e^{-i\rho t}$, $m$-qubit precision register.

**Circuit:**
1. Initialize: $|0\rangle^{\otimes m} \otimes |v_j\rangle$  
2. Apply Hadamards to precision register: $\frac{1}{2^{m/2}}\sum_{k=0}^{2^m-1}|k\rangle \otimes |v_j\rangle$  
3. Controlled-$U^{2^k}$ operations for $k=0,\ldots,m-1$  
4. Inverse QFT on precision register  
5. Measure: obtain $\tilde{\lambda}_j$ approximating $\lambda_j t/(2\pi)$

**Phase Extraction:**
$$
\lambda_j \approx \frac{2\pi \tilde{\lambda}_j}{t}
$$

**Precision:**  
With $m$ bits: error $\epsilon \sim \mathcal{O}(2^{-m})$.

**QPE Complexity:**
- Qubits: $n + m$ (data + precision)  
- Gates: $\mathcal{O}(m \cdot T_U)$ where $T_U$ = cost to implement $U$  
- Controlled-$U^{2^k}$: requires $2^k$ applications of controlled-$U$

**Complete qPCA Algorithm:**

**Input:** Quantum access to density matrix $\rho$ (oracle $U_{\rho}$ preparing $\rho$ copies), precision $\epsilon$, number of components $k$.

**Step 1: Density Matrix Preparation**  
Prepare $\rho = \frac{1}{N}\sum_i |\psi_i\rangle\langle\psi_i|$ via data loading oracle.

**Step 2: Hamiltonian Simulation**  
Construct unitary $U = e^{-i\rho t}$ using:
- **Trotterization:** $e^{-i\rho t} \approx (e^{-i\rho t/r})^r$ with error $\mathcal{O}(t^2/r)$  
- **LCU (Linear Combination of Unitaries):** For $\rho = \sum_j \alpha_j U_j$

**Step 3: Eigenvector Preparation**  
Use **Quantum Singular Value Estimation (QSVE)** variant:
- Prepare maximally mixed state or random $|\psi\rangle = \sum_j c_j |v_j\rangle$  
- Apply QPE to extract each $\lambda_j$ with amplitude $|c_j|^2$

Alternatively, use **Variational Quantum Eigensolver (VQE)** for low-lying eigenvalues.

**Step 4: Eigenvalue Extraction**  
Run QPE with $m = \lceil\log_2(1/\epsilon)\rceil$ precision qubits:  
Obtain $\{\lambda_j\}_{j=1}^k$ for top $k$ eigenvalues.

**Step 5: Projection**  
Project new data $|\psi_{\text{new}}\rangle$ onto principal components:

$$
|\psi_{\text{reduced}}\rangle = \sum_{j=1}^k \langle v_j|\psi_{\text{new}}\rangle |v_j\rangle
$$

Measure overlaps $\langle v_j|\psi_{\text{new}}\rangle$ using SWAP test.

**Complexity Analysis:**

**Quantum qPCA:**
- Data encoding: $\mathcal{O}(\text{poly}(n))$ per sample (assumption: efficient oracle)  
- Density matrix preparation: $\mathcal{O}(\text{poly}(n, \log N))$  
- QPE execution: $\mathcal{O}(m \cdot T_U) = \mathcal{O}(\log(1/\epsilon) \cdot \text{poly}(n))$  
- Total per eigenvalue: $\mathcal{O}(\text{poly}(n, \log(1/\epsilon)))$

**Exponential Speedup Condition:**

Classical: $\mathcal{O}(d^3) = \mathcal{O}(2^{3n})$  
Quantum: $\mathcal{O}(\text{poly}(n))$

Speedup factor: $\mathcal{O}(2^{3n}/\text{poly}(n))$ — **exponential** in dimension.

**Critical Assumptions:**

1. **Efficient State Preparation:** Must prepare $|\psi_i\rangle$ in $\text{poly}(n)$ time  
   - If classical data requires $\Theta(d)$ operations, advantage lost  
   - Valid for quantum data or structured classical data (sparse, low-rank)

2. **Quantum RAM (qRAM):** Oracle access to data  
   - Coherent superposition over data indices: $\sum_i |i\rangle|\psi_i\rangle$  
   - Implementation challenges: coherence time, error rates

3. **Output Readout:** Classical description of eigenvectors requires $\mathcal{O}(d)$ measurements  
   - qPCA advantage for quantum downstream tasks (e.g., classification with quantum data)

**Lloyd-Mohseni-Rebentrost Algorithm (2013):**

Seminal qPCA implementation using:
- Density matrix exponentiation  
- QPE for eigenvalue estimation  
- Complexity: $\mathcal{O}(\log(Nd)/\epsilon)$ vs. classical $\mathcal{O}(Nd^2 + d^3)$

**Practical Considerations:**

1. **Gate Depth:** Hamiltonian simulation requires deep circuits  
2. **Coherence Requirements:** QPE needs long coherence times  
3. **Error Mitigation:** Noise accumulates in Trotter steps  
4. **NISQ Adaptations:** Variational approaches (VQE-based) for near-term devices

---

### **Comprehension Check**

!!! note "Quiz"
    
        1.  The primary quantum subroutine used in qPCA to extract the eigenvalues of the data density matrix is:
        2.  A key requirement for running qPCA is the ability to efficiently prepare and utilize multiple copies of what structure?
    
??? info "See Answer"
    
        1.  **Quantum Phase Estimation (QPE).** QPE is used to find the eigenvalues of the unitary $e^{-i\rho t}$, which directly relate to the eigenvalues of the density matrix $\rho$.
        2.  **The data density matrix $\rho$.** The algorithm's efficiency hinges on the ability to prepare this state representation of the classical data.
    
!!! abstract "Interview-Style Question"
    
    Explain where the potential exponential speedup in qPCA originates, contrasting it with the complexity of classical PCA.
    
    ???+ info "Answer Strategy"
        The potential for exponential speedup in qPCA comes from a fundamental shift in the computational approach, moving from classical matrix operations to quantum state manipulation.
    
        1.  **Classical Bottleneck:** Classical PCA requires diagonalizing an $N \times N$ covariance matrix, a task that scales polynomially with the data dimension $N$ (e.g., as $O(N^3)$). This becomes prohibitively expensive for very large datasets.
        2.  **Quantum Advantage:** qPCA bypasses this direct diagonalization. It instead uses the **Quantum Phase Estimation (QPE)** algorithm to find the eigenvalues of the data's density matrix. The complexity of QPE scales polynomially with $\log N$, not $N$.
        3.  **The Trade-off:** This exponential speedup is conditional on a critical assumption: the ability to efficiently prepare the quantum state (the density matrix) that represents the classical data. If this state preparation is itself classically hard, the advantage is lost.
    
        In short, qPCA trades a classical problem that scales with matrix size for a quantum problem that scales with the number of qubits needed to represent it, offering an exponential advantage for high-dimensional data.
    
---

### **<i class="fa-solid fa-flask"></i> Hands-On Projects**

#### **Project Blueprint: Analyzing qPCA Scaling**

| Component | Description |
| :--- | :--- |
| **Objective** | Analyze and contrast the computational resource scaling of classical PCA versus qPCA for a massive dataset. |
| **Mathematical Concept** | Classical matrix diagonalization complexity ($O(N^2)$ or $O(N^3)$) vs. quantum state representation ($\log_2 N$ qubits) and logarithmic time algorithms. |
| **Experiment Setup** | A hypothetical dataset with $N = 1,048,576$ ($= 2^{20}$) data points. We compare the scaling of operations in terms of $N$. |
| **Process Steps** | 1. Calculate the approximate number of operations for a classical $O(N^2)$ algorithm. <br> 2. Determine the number of qubits required to represent the $N$ data points in a quantum state. <br> 3. Compare the magnitude of the classical operation count ($N^2$) with the quantum resource count ($n = \log_2 N$). |
| **Expected Behavior** | A dramatic divergence in resource requirements, highlighting the theoretical power of quantum algorithms for large-scale linear algebra. |
| **Verification Goal** | Quantify the difference between the polynomial scaling of the classical approach and the logarithmic scaling of the quantum approach. |

---

#### **Python Implementation**

```python
import numpy as np

# Project 1: qPCA Scaling Analysis (Classical NumPy simulation)

def simulate_qpca_scaling(dims):
    """
    Classical quantum-inspired PCA: analyze the scaling of HHL for density matrix exponentiation.
    Key result: qPCA should output top-k eigenvalues in O(log(d) * k) vs classical O(d^3).
    """
    classical_costs = {d: d**3 for d in dims}             # O(d^3) classical SVD
    quantum_costs   = {d: np.log2(d) * np.sqrt(d) for d in dims}  # O(log(d)*sqrt(d)) heuristic

    print(f"{'d':>8}  {'Classical O(d^3)':>18}  {'Quantum O(log(d)*√d)':>22}  Speedup")
    for d in dims:
        cc, qc_ = classical_costs[d], quantum_costs[d]
        print(f"{d:>8}  {cc:>18.0f}  {qc_:>22.2f}  {cc/qc_:.1e}x")

simulate_qpca_scaling([8, 64, 512, 4096])
```
**Sample Output:**
```python
d    Classical O(d^3)    Quantum O(log(d)*√d)  Speedup
       8                 512                    8.49  6.0e+01x
      64              262144                   48.00  5.5e+03x
     512           134217728                  203.65  6.6e+05x
    4096         68719476736                  768.00  8.9e+07x
```


#### **Outcome and Interpretation**

Executing this analysis reveals the immense theoretical gap. Classically, the number of operations is on the order of $(10^6)^2 = 10^{12}$, a trillion operations. In contrast, the quantum approach requires only $\log_2(1,048,576) = 20$ qubits to represent the state space. Even if the quantum algorithm's runtime is polynomial in the number of qubits (e.g., $n^2 = 400$), the difference between $10^{12}$ and $400$ is astronomical. This illustrates the core promise of qPCA: converting computationally prohibitive classical linear algebra problems into manageable tasks on a quantum computer.

---

## **12.2 Quantum k-Means Clustering** {.heading-with-pill}

> **Difficulty:** ★★★☆☆
> 
> **Concept:** Quantum-Enhanced Cluster Assignment
> 
> **Summary:** Quantum k-Means enhances the classical algorithm by using quantum states to represent data points and cluster centroids. It calculates the distance between them via fidelity (state overlap), a process that can be parallelized on a quantum computer to potentially speed up the most intensive step of the classical algorithm.

---

### **Theoretical Background**

The k-Means algorithm is a foundational unsupervised learning method for clustering data into $k$ groups. Quantum k-Means leverages quantum state overlap to accelerate distance computations, the most expensive classical step.

**Classical k-Means Algorithm:**

**Input:** Dataset $\mathcal{D} = \{\mathbf{x}_i\}_{i=1}^N$ with $\mathbf{x}_i \in \mathbb{R}^d$, number of clusters $k$

**Initialization:**  
Randomly select $k$ centroids $\{\mathbf{c}_j\}_{j=1}^k$ from data or random initialization.

**Iterative Steps:**

**E-Step (Assignment):** For each point $\mathbf{x}_i$, assign to nearest centroid:

$$
z_i = \arg\min_{j \in [k]} \|\mathbf{x}_i - \mathbf{c}_j\|^2
$$

Define cluster assignments: $C_j = \{\mathbf{x}_i : z_i = j\}$

**M-Step (Update):** Recompute centroids:

$$
\mathbf{c}_j = \frac{1}{|C_j|}\sum_{\mathbf{x}_i \in C_j} \mathbf{x}_i
$$

**Convergence:** Repeat until $\|\mathbf{c}_j^{(t+1)} - \mathbf{c}_j^{(t)}\| < \epsilon$ for all $j$, or maximum iterations reached.

**Objective Function (Inertia):**
$$
J = \sum_{j=1}^k \sum_{\mathbf{x}_i \in C_j} \|\mathbf{x}_i - \mathbf{c}_j\|^2
$$

k-Means minimizes within-cluster sum of squared distances.

**Classical Complexity:**
- Per iteration: $\mathcal{O}(Nkd)$ (distance computations dominate)  
- Total: $\mathcal{O}(Ikd N)$ for $I$ iterations  
- Typical: $I = \mathcal{O}(\log N)$ to $\mathcal{O}(N)$ depending on initialization

**Quantum State Encoding:**

Map data to quantum states using amplitude encoding:

$$
\mathbf{x}_i \in \mathbb{R}^d \xrightarrow{\text{normalize}} |\psi_i\rangle = \frac{1}{\|\mathbf{x}_i\|}\sum_{\alpha=0}^{d-1} x_{i,\alpha} |\alpha\rangle
$$

Requires $n = \lceil\log_2 d\rceil$ qubits.

**Normalization:**
$$
\|\mathbf{x}_i\| = \sqrt{\sum_{\alpha=0}^{d-1} x_{i,\alpha}^2}
$$

Quantum state automatically normalized: $\langle\psi_i|\psi_i\rangle = 1$.

**Centroid Encoding:**  
Similarly encode centroids:

$$
|c_j\rangle = \frac{1}{\|\mathbf{c}_j\|}\sum_{\alpha=0}^{d-1} c_{j,\alpha} |\alpha\rangle
$$

**Quantum Distance Metric:**

**Fidelity (State Overlap):**
$$
F(\mathbf{x}_i, \mathbf{c}_j) = |\langle\psi_i|c_j\rangle|^2
$$

Measures similarity: $F = 1$ (identical), $F = 0$ (orthogonal).

**Quantum Distance:**  
Define metric compatible with classical Euclidean distance:

$$
d_Q(\mathbf{x}_i, \mathbf{c}_j) = \sqrt{2(1 - \text{Re}\langle\psi_i|c_j\rangle)}
$$

For real vectors, simplifies to:

$$
d_Q(\mathbf{x}_i, \mathbf{c}_j) = \sqrt{2(1 - \langle\psi_i|c_j\rangle)}
$$

**Relationship to Euclidean Distance:**

Expand normalized inner product:

$$
\langle\psi_i|c_j\rangle = \frac{\mathbf{x}_i \cdot \mathbf{c}_j}{\|\mathbf{x}_i\| \|\mathbf{c}_j\|}
$$

Classical squared distance:

$$
\|\mathbf{x}_i - \mathbf{c}_j\|^2 = \|\mathbf{x}_i\|^2 + \|\mathbf{c}_j\|^2 - 2\mathbf{x}_i \cdot \mathbf{c}_j
$$

Normalized version:

$$
\frac{\|\mathbf{x}_i - \mathbf{c}_j\|^2}{\|\mathbf{x}_i\| \|\mathbf{c}_j\|} = \frac{\|\mathbf{x}_i\|}{\|\mathbf{c}_j\|} + \frac{\|\mathbf{c}_j\|}{\|\mathbf{x}_i\|} - 2\langle\psi_i|c_j\rangle
$$

For similarly-normed vectors ($\|\mathbf{x}_i\| \approx \|\mathbf{c}_j\|$):

$$
d_Q^2 \approx \frac{\|\mathbf{x}_i - \mathbf{c}_j\|^2}{\|\mathbf{x}_i\|^2}
$$

So quantum distance preserves classical clustering structure.

**SWAP Test for Fidelity Estimation:**

**Circuit Architecture:**

1. **Registers:** Ancilla $|0\rangle$, data register A in $|\psi_i\rangle$, centroid register B in $|c_j\rangle$  
2. **Hadamard:** Apply $\mathbf{H}$ to ancilla: $\frac{1}{\sqrt{2}}(|0\rangle + |1\rangle) \otimes |\psi_i\rangle \otimes |c_j\rangle$  
3. **Controlled-SWAP:** $\text{CSWAP}_{A \leftrightarrow B}$ controlled by ancilla:

$$
\frac{1}{\sqrt{2}}\left(|0\rangle|\psi_i\rangle|c_j\rangle + |1\rangle|c_j\rangle|\psi_i\rangle\right)
$$

4. **Hadamard:** Apply $\mathbf{H}$ to ancilla  
5. **Measurement:** Measure ancilla in computational basis

**Final State Before Measurement:**

$$
|\Psi\rangle = \frac{1}{2}\left[|0\rangle(|\psi_i\rangle|c_j\rangle + |c_j\rangle|\psi_i\rangle) + |1\rangle(|\psi_i\rangle|c_j\rangle - |c_j\rangle|\psi_i\rangle)\right]
$$

**Measurement Probabilities:**

$$
P(|0\rangle) = \frac{1 + |\langle\psi_i|c_j\rangle|^2}{2}
$$

$$
P(|1\rangle) = \frac{1 - |\langle\psi_i|c_j\rangle|^2}{2}
$$

**Fidelity Estimation:**  
From $M$ shots, estimate:

$$
\hat{F} = 2\hat{P}(|0\rangle) - 1 = 2\frac{n_0}{M} - 1
$$

where $n_0$ = count of $|0\rangle$ outcomes.

**Statistical Error:**  
Variance of estimator:

$$
\text{Var}[\hat{F}] = \frac{4P(|0\rangle)(1 - P(|0\rangle))}{M} \leq \frac{1}{M}
$$

Standard deviation: $\sigma \sim \mathcal{O}(1/\sqrt{M})$.

For precision $\epsilon$: require $M = \mathcal{O}(1/\epsilon^2)$ shots.

**Quantum k-Means Algorithm:**

**Input:** Quantum access to dataset $\{|\psi_i\rangle\}_{i=1}^N$, number of clusters $k$, precision $\epsilon$

**Initialization:**  
Randomly select $k$ data points as initial centroids: $\{|c_j^{(0)}\rangle\}_{j=1}^k$

**Iteration $t$:**

**Step 1: Quantum Distance Computation**  
For each pair $(i, j) \in [N] \times [k]$:
- Prepare $|\psi_i\rangle$ and $|c_j^{(t)}\rangle$  
- Execute SWAP test with $M = \mathcal{O}(1/\epsilon^2)$ shots  
- Estimate fidelity $\hat{F}_{ij}$  
- Compute distance: $d_{ij} = \sqrt{2(1 - \hat{F}_{ij})}$

Total quantum circuits: $Nk$ per iteration

**Step 2: Classical Assignment**  
For each $i \in [N]$:

$$
z_i^{(t)} = \arg\min_{j \in [k]} d_{ij}
$$

Form clusters: $C_j^{(t)} = \{i : z_i^{(t)} = j\}$

**Step 3: Classical Centroid Update**  
For each $j \in [k]$:

$$
\mathbf{c}_j^{(t+1)} = \frac{1}{|C_j^{(t)}|}\sum_{i \in C_j^{(t)}} \mathbf{x}_i
$$

Prepare quantum state $|c_j^{(t+1)}\rangle$ via amplitude encoding.

**Step 4: Convergence Check**  
If $\max_j \|\mathbf{c}_j^{(t+1)} - \mathbf{c}_j^{(t)}\| < \delta$, terminate. Else $t \leftarrow t+1$, repeat.

**Complexity Analysis:**

**Per Iteration:**
- Quantum distance evaluations: $Nk$  
- Shots per evaluation: $M = \mathcal{O}(1/\epsilon^2)$  
- Total measurements: $\mathcal{O}(Nk/\epsilon^2)$  
- Classical assignment: $\mathcal{O}(Nk)$  
- Classical centroid update: $\mathcal{O}(Nd)$  
- Quantum state preparation: $\mathcal{O}(kT_{\text{prep}})$ where $T_{\text{prep}}$ = encoding cost

**Total per iteration:** $\mathcal{O}(Nk/\epsilon^2 + Nd + kT_{\text{prep}})$

**Classical Comparison:**  
Classical per iteration: $\mathcal{O}(Nkd)$

**Quantum Advantage Conditions:**

1. **Efficient State Preparation:** $T_{\text{prep}} = \text{poly}(\log d)$  
2. **Shot Budget:** $M \ll d$ (i.e., $1/\epsilon^2 \ll d$)  
3. **High Dimension:** $d \gg k, N$

Under these: quantum cost $\mathcal{O}(Nk/\epsilon^2) \ll \mathcal{O}(Nkd)$.

**Speedup Factor:** Potentially $\mathcal{O}(d\epsilon^2)$ for high-dimensional data.

**Practical Challenges:**

1. **State Preparation Bottleneck:**  
   - Loading classical vector $\mathbf{x}_i \in \mathbb{R}^d$ requires $\Theta(d)$ operations  
   - Negates advantage unless data inherently quantum or has special structure

2. **Centroid Encoding:**  
   - After classical update, must re-encode $k$ centroids  
   - Requires $\mathcal{O}(kd)$ operations per iteration

3. **Shot Noise:**  
   - Large $M$ needed for accurate distances  
   - Errors propagate through iterations, affecting convergence

4. **Hybrid Overhead:**  
   - Classical-quantum communication costs  
   - Measurement readout and post-processing

**Variations and Extensions:**

**1. Quantum Parallelization:**  
Use amplitude amplification to search for minimum distance in $\mathcal{O}(\sqrt{k})$ instead of $\mathcal{O}(k)$.

**2. Quantum Minimum Finding:**  
Dürr-Høyer algorithm finds minimum among $k$ items in $\mathcal{O}(\sqrt{k})$ queries.

**3. Fully Quantum k-Means:**  
Maintain centroids as quantum superpositions, avoiding repeated encoding.

**4. Quantum Fuzzy k-Means:**  
Assign partial membership probabilities using quantum amplitude estimation.

---

### **Comprehension Check**

!!! note "Quiz"
    
        1.  In Quantum k-means, the dissimilarity between a data point and a centroid is calculated using what property of their quantum states?
        2.  What is the primary computational bottleneck in classical k-means that quantum versions aim to accelerate?
    
??? info "See Answer"
    
        1.  The **fidelity** or **squared overlap** ($|\langle \psi(x) | \psi(c) \rangle|^2$) of their corresponding quantum states. The distance is typically a function of this value, like $\sqrt{1 - |\text{overlap}|^2}$.
        2.  The requirement to **calculate the distance** between every data point and every cluster centroid in each iteration of the algorithm.
    
!!! abstract "Interview-Style Question"
    
    A colleague suggests that since the Swap Test provides the distance, a quantum computer can run the entire k-Means algorithm with exponential speedup. What is a more nuanced take on this claim?
    
    ???+ info "Answer Strategy"
        The claim is an oversimplification. While quantum methods can accelerate a key part of the k-Means algorithm, the overall speedup is more nuanced due to the algorithm's hybrid nature.
    
        1.  **Acknowledge the Quantum Step:** The core idea is valid. Using quantum subroutines like the Swap Test to calculate distances between data points and centroids is where the potential for a significant speedup lies. This step can be faster than its classical counterpart.
        2.  **Identify the Classical Bottlenecks:** The quantum k-Means algorithm is **hybrid**. Several crucial steps remain classical:
            *   **Data Loading (I/O):** Loading the classical data into quantum states can be a major bottleneck that limits overall performance.
            *   **Centroid Recalculation:** After points are assigned to clusters, the new centroids must be computed. This is a classical computation that must be performed in each iteration.
        3.  **Conclusion on Speedup:** The overall speedup is constrained by these classical components. Therefore, while the quantum distance calculation offers a significant advantage, the total speedup for the *entire* k-Means algorithm is not guaranteed to be exponential. It is a potential polynomial improvement on a specific subroutine, leading to a valuable but not unlimited, overall performance gain.
    
---

### **<i class="fa-solid fa-flask"></i> Hands-On Projects**

#### **Project Blueprint: Quantum vs. Classical Distance**

| Component | Description |
| :--- | :--- |
| **Objective** | Demonstrate that two classically orthogonal vectors can have a non-zero distance in a quantum representation, highlighting the difference between geometric spaces. |
| **Mathematical Concept** | Classical orthogonality ($\mathbf{a} \cdot \mathbf{b} = 0$) vs. quantum state overlap ($\langle \psi_a | \psi_b \rangle$). |
| **Experiment Setup** | Two classical vectors represented as quantum states: $\|x\rangle = \|+\rangle = \frac{1}{\sqrt{2}}(\|0\rangle + \|1\rangle)$ and $\|c\rangle = \|-\rangle = \frac{1}{\sqrt{2}}(\|0\rangle - \|1\rangle)$. |
| **Process Steps** | 1. Calculate the classical dot product of the corresponding vectors $(1, 1)$ and $(1, -1)$. <br> 2. Calculate the quantum inner product (overlap) $\langle x | c \rangle$. <br> 3. Compute the quantum distance using the fidelity-based metric. |
| **Expected Behavior** | The classical dot product will be zero, indicating orthogonality. The quantum overlap will also be zero, resulting in a maximal quantum distance. This project shows how quantum distance can reflect classical geometric properties. |
| **Verification Goal** | Confirm that classically orthogonal vectors can be mapped to orthogonal quantum states, leading to a specific, calculable quantum distance. |

---

#### **Python Implementation**

```python
import numpy as np
from scipy.spatial.distance import cdist

# Project 2: Quantum vs Classical Distance Calculation

def classical_euclidean(x1, x2):
    return np.linalg.norm(np.array(x1) - np.array(x2))

def quantum_swap_test_distance(x1, x2):
    """Swap-test estimate of 1 - |<x1|x2>|^2 (uses normalized vectors)."""
    v1 = np.array(x1, dtype=float)
    v2 = np.array(x2, dtype=float)
    v1 /= np.linalg.norm(v1); v2 /= np.linalg.norm(v2)
    fidelity = abs(np.dot(v1, v2))**2
    # Quantum distance ∝ 1 - fidelity (after normalization)
    return 1 - fidelity

x_pairs = [
    ([1,0], [0,1]),
    ([1,1], [1,1]),
    ([1,0], [1,0]),
    ([2,3], [1,2]),
]
print(f"{'x1':<12} {'x2':<12} {'Euclidean':>12} {'Quantum dist':>14}")
for x1, x2 in x_pairs:
    print(f"{str(x1):<12} {str(x2):<12} {classical_euclidean(x1,x2):>12.4f} {quantum_swap_test_distance(x1,x2):>14.4f}")
```
**Sample Output:**
```python
x1           x2              Euclidean   Quantum dist
[1, 0]       [0, 1]             1.4142         1.0000
[1, 1]       [1, 1]             0.0000         0.0000
[1, 0]       [1, 0]             0.0000         0.0000
[2, 3]       [1, 2]             1.4142         0.0154
```


#### **Outcome and Interpretation**

The calculation shows that the quantum overlap $\langle + | - \rangle = 0$. Consequently, the quantum distance is $\sqrt{1 - 0} = 1$, its maximum possible value. This aligns perfectly with the classical dot product of $(1, 1)$ and $(1, -1)$ being $1-1=0$. This exercise demonstrates that the quantum fidelity-based distance is a valid and intuitive measure of similarity that can directly map from classical geometric notions of orthogonality, forming a reliable foundation for the quantum k-Means algorithm.

---

## **12.3 Quantum Boltzmann Machines** {.heading-with-pill}

> **Difficulty:** ★★★★☆
> 
> **Concept:** Quantum Generative Modeling
> 
> **Summary:** Quantum Boltzmann Machines (QBMs) are generative models that learn the underlying probability distribution of a dataset. They use a parameterized quantum Hamiltonian to define a thermal state, leveraging quantum effects like entanglement to capture complex correlations that are intractable for classical models.

---

### **Theoretical Background**

Quantum Boltzmann Machines (QBMs) are generative models that leverage quantum mechanics—particularly entanglement and superposition—to represent complex probability distributions intractable for classical Boltzmann machines.

**Classical Boltzmann Machine Foundation:**

**Energy Function:**  
Define binary system with visible units $\mathbf{v} \in \{0,1\}^{n_v}$ and hidden units $\mathbf{h} \in \{0,1\}^{n_h}$.

Energy of configuration $(\mathbf{v}, \mathbf{h})$:

$$
E(\mathbf{v}, \mathbf{h}; \theta) = -\sum_{i,j} W_{ij}^{vv} v_i v_j - \sum_{k,\ell} W_{k\ell}^{hh} h_k h_\ell - \sum_{i,k} W_{ik}^{vh} v_i h_k - \sum_i b_i^v v_i - \sum_k b_k^h h_k
$$

where $\theta = \{\mathbf{W}^{vv}, \mathbf{W}^{hh}, \mathbf{W}^{vh}, \mathbf{b}^v, \mathbf{b}^h\}$ are parameters.

**Boltzmann Distribution:**
$$
P(\mathbf{v}, \mathbf{h}; \theta) = \frac{e^{-\beta E(\mathbf{v}, \mathbf{h}; \theta)}}{Z(\theta)}
$$

**Partition Function:**
$$
Z(\theta) = \sum_{\mathbf{v}, \mathbf{h}} e^{-\beta E(\mathbf{v}, \mathbf{h}; \theta)}
$$

with inverse temperature $\beta = 1/(k_B T)$. Typically set $\beta = 1$.

**Marginal Distribution (Visible Units):**
$$
P(\mathbf{v}; \theta) = \sum_{\mathbf{h}} P(\mathbf{v}, \mathbf{h}; \theta) = \frac{1}{Z}\sum_{\mathbf{h}} e^{-E(\mathbf{v}, \mathbf{h}; \theta)}
$$

**Training Objective:**  
Maximize log-likelihood of data $\mathcal{D} = \{\mathbf{v}^{(i)}\}_{i=1}^N$:

$$
\mathcal{L}(\theta) = \frac{1}{N}\sum_{i=1}^N \log P(\mathbf{v}^{(i)}; \theta)
$$

**Gradient (Log-Likelihood):**
$$
\frac{\partial \mathcal{L}}{\partial \theta} = \mathbb{E}_{\text{data}}\left[\frac{\partial E}{\partial \theta}\right] - \mathbb{E}_{\text{model}}\left[\frac{\partial E}{\partial \theta}\right]
$$

where:
- $\mathbb{E}_{\text{data}}$: expectation over data distribution with hidden units marginalized  
- $\mathbb{E}_{\text{model}}$: expectation over model distribution $P(\mathbf{v}, \mathbf{h}; \theta)$

**Classical Training Challenge:**  
Computing $\mathbb{E}_{\text{model}}$ requires sampling from $P(\mathbf{v}, \mathbf{h}; \theta)$, typically via Markov Chain Monte Carlo (MCMC), which is exponentially hard for complex distributions.

**Quantum Boltzmann Machine Formulation:**

**Parameterized Hamiltonian:**  
Replace classical energy with quantum Hamiltonian $H(\theta)$ acting on $n$-qubit Hilbert space $\mathcal{H} = (\mathbb{C}^2)^{\otimes n}$.

**General Form:**
$$
H(\theta) = \sum_{\alpha} h_\alpha(\theta) \mathbf{P}_\alpha
$$

where $\mathbf{P}_\alpha$ are Pauli strings (products of $\{\mathbf{I}, \mathbf{X}, \mathbf{Y}, \mathbf{Z}\}$) and $h_\alpha(\theta)$ are tunable coefficients.

**Transverse-Field Ising Model (TFIM):**
$$
H(\theta) = -\sum_{\langle i,j\rangle} J_{ij} \mathbf{Z}_i \mathbf{Z}_j - \sum_i h_i^z \mathbf{Z}_i - \sum_i h_i^x \mathbf{X}_i
$$

where:
- $J_{ij}$: coupling strengths (learnable)  
- $h_i^z$: longitudinal fields (learnable)  
- $h_i^x$: transverse fields (learnable)

**Hermiticity:** $H = H^\dagger$ ensures real eigenvalues.

**Quantum Thermal (Gibbs) State:**

Analogue of Boltzmann distribution:

$$
\rho(\theta) = \frac{e^{-\beta H(\theta)}}{Z_Q(\theta)}
$$

where:

**Quantum Partition Function:**
$$
Z_Q(\theta) = \text{Tr}\left(e^{-\beta H(\theta)}\right) = \sum_{j=1}^{2^n} e^{-\beta E_j(\theta)}
$$

with $E_j$ eigenvalues of $H(\theta)$.

**Properties of Gibbs State:**

1. **Hermitian:** $\rho = \rho^\dagger$  
2. **Positive semi-definite:** $\langle\psi|\rho|\psi\rangle \geq 0$  
3. **Normalized:** $\text{Tr}(\rho) = 1$  
4. **Diagonal in energy eigenbasis:**

$$
\rho = \sum_{j=1}^{2^n} p_j |E_j\rangle\langle E_j|, \quad p_j = \frac{e^{-\beta E_j}}{Z_Q}
$$

**Probability Distribution:**  
In computational basis $\{|x\rangle\}_{x \in \{0,1\}^n}$:

$$
P_Q(x; \theta) = \langle x|\rho(\theta)|x\rangle = \sum_j p_j |\langle x|E_j\rangle|^2
$$

This is the **Born rule probability** for measuring state $|x\rangle$.

**Entanglement and Expressivity:**

Key QBM advantage: Gibbs state $\rho(\theta)$ can be highly entangled.

**Entanglement Entropy:**  
For bipartition $A \cup B$ of qubits:

$$
S_A = -\text{Tr}(\rho_A \log \rho_A)
$$

where $\rho_A = \text{Tr}_B(\rho)$ is reduced density matrix.

For volume-law entanglement: $S_A \sim |A|$ (scales with subsystem size).  
Classical models: $S_A \leq \log(\text{rank}(\mathbf{W}))$ — bounded by matrix rank.

QBMs can represent distributions requiring exponentially many parameters classically.

**Temperature Regimes:**

**High Temperature ($\beta \to 0$):**
$$
\rho \to \frac{\mathbf{I}}{2^n} \quad \text{(maximally mixed)}
$$
$$
P_Q(x) \to \frac{1}{2^n} \quad \text{(uniform)}
$$

**Low Temperature ($\beta \to \infty$):**
$$
\rho \to |E_0\rangle\langle E_0| \quad \text{(ground state)}
$$
$$
P_Q(x) \to |\langle x|E_0\rangle|^2
$$

**Intermediate:** Thermal mixture of excited states.

**Training Quantum Boltzmann Machines:**

**Objective:**  
Maximize log-likelihood of data distribution:

$$
\mathcal{L}(\theta) = \frac{1}{N}\sum_{i=1}^N \log P_Q(x^{(i)}; \theta)
$$

**Gradient Computation:**

For observable $O = |x\rangle\langle x|$:

$$
\frac{\partial \log P_Q(x; \theta)}{\partial \theta_k} = \frac{\partial}{\partial \theta_k}\log\langle x|\rho(\theta)|x\rangle
$$

Using $\frac{\partial \rho}{\partial \theta_k} = -\beta \left(\frac{\partial H}{\partial \theta_k}\rho - \rho\frac{\partial H}{\partial \theta_k}\langle \frac{\partial H}{\partial \theta_k}\rangle\right)$:

$$
\frac{\partial \mathcal{L}}{\partial \theta_k} = -\beta\left[\langle \frac{\partial H}{\partial \theta_k}\rangle_{x} - \langle \frac{\partial H}{\partial \theta_k}\rangle_{\rho}\right]
$$

where:
- $\langle \cdots \rangle_x = \langle x|(\cdots)|x\rangle$: expectation in data state  
- $\langle \cdots \rangle_\rho = \text{Tr}(\rho \cdots)$: thermal expectation

**Practical Gradient Estimation:**

**Data Term:** For each sample $x^{(i)}$:
$$
\langle \frac{\partial H}{\partial \theta_k}\rangle_{x^{(i)}} = \langle x^{(i)}|\frac{\partial H}{\partial \theta_k}|x^{(i)}\rangle
$$

Classically computable.

**Model Term:**
$$
\langle \frac{\partial H}{\partial \theta_k}\rangle_\rho = \text{Tr}\left(\rho(\theta) \frac{\partial H}{\partial \theta_k}\right)
$$

Requires:
1. Preparing Gibbs state $\rho(\theta)$  
2. Measuring observable $\frac{\partial H}{\partial \theta_k}$

**Gibbs State Preparation Methods:**

**1. Quantum Imaginary Time Evolution:**
$$
\rho(\tau) = \frac{e^{-\tau H}}{\text{Tr}(e^{-\tau H})}
$$

Simulate imaginary time $\tau = \beta$ starting from $\rho(0) = \mathbf{I}/2^n$.

**2. Variational Quantum Thermalizer:**  
Parameterize thermal state:
$$
\rho_{\text{var}}(\phi) = U(\phi) \rho_0 U^\dagger(\phi)
$$

Minimize free energy:
$$
F(\phi) = \text{Tr}(\rho_{\text{var}} H) + \frac{1}{\beta}S(\rho_{\text{var}})
$$

where $S(\rho) = -\text{Tr}(\rho \log \rho)$ is von Neumann entropy.

**3. Quantum Metropolis Sampling:**  
Quantum walk in Hilbert space converging to Gibbs distribution.

**4. Adiabatic Preparation:**  
Slowly evolve from easily prepared state:
$$
H(s) = (1-s)H_0 + sH(\theta), \quad s: 0 \to 1
$$

If $H_0$ ground state is $|\psi_0\rangle$ at high temperature, adiabatic evolution reaches thermal state.

**Training Algorithm:**

**Input:** Data $\mathcal{D} = \{x^{(i)}\}_{i=1}^N$, learning rate $\eta$, inverse temperature $\beta$

**Initialize:** Random parameters $\theta^{(0)}$

**For** $t = 1, 2, \ldots$:

**Step 1:** Prepare Gibbs state $\rho(\theta^{(t)})$ on quantum device

**Step 2:** Compute data gradient:
$$
g_{\text{data}} = \frac{1}{N}\sum_{i=1}^N \langle x^{(i)}|\frac{\partial H}{\partial \theta}|x^{(i)}\rangle
$$

**Step 3:** Estimate model gradient via measurement:
$$
g_{\text{model}} = \text{Tr}\left(\rho(\theta^{(t)}) \frac{\partial H}{\partial \theta}\right)
$$

Run $M$ measurements, average results.

**Step 4:** Update parameters:
$$
\theta^{(t+1)} = \theta^{(t)} + \eta \beta (g_{\text{data}} - g_{\text{model}})
$$

**Step 5:** Check convergence

**Complexity Challenges:**

1. **Gibbs State Preparation:** Generally BQP-complete, no efficient classical algorithm  
2. **Partition Function:** Computing $Z_Q$ exactly is #P-hard  
3. **Gradient Variance:** Shot noise in expectation estimation  
4. **Barren Plateaus:** Deep thermalizing circuits may exhibit vanishing gradients

**Quantum Advantage:**

**Representational Power:**  
QBMs with $\mathcal{O}(\text{poly}(n))$ parameters can represent distributions requiring $\mathcal{O}(2^n)$ classical parameters.

**Example:** GHZ-like correlations:
$$
P(x) = \begin{cases}1/2 & x = 0^n \text{ or } 1^n \\ 0 & \text{otherwise}\end{cases}
$$

QBM Hamiltonian: $H = -(\mathbf{X}^{\otimes n} + \mathbf{Z}^{\otimes n})$ (2 terms)  
Classical Boltzmann machine: requires exponentially many connections

**Applications:**

1. **Quantum Data Modeling:** Learning distributions of quantum measurements  
2. **Generative Sampling:** Creating synthetic quantum states  
3. **Anomaly Detection:** Identifying outliers in quantum systems  
4. **Quantum Chemistry:** Modeling molecular electronic states

---

### **Comprehension Check**

!!! note "Quiz"
    
        1.  In a QBM, the probability distribution over states is defined by the energy levels of what quantum object?
        2.  QBMs are particularly advantageous for generative modeling because they can naturally encode what property of the data using quantum mechanics?
    
??? info "See Answer"
    
        1.  A **parameterized Hamiltonian $H(\theta)$**. The probability of a state is related to its energy eigenvalue through the Boltzmann distribution.
        2.  **Complex correlations** via **entanglement**. Entanglement allows the model to capture statistical dependencies between variables that are difficult for classical models to represent.
    
!!! abstract "Interview-Style Question"
    
    Explain the conceptual difference between a Quantum Boltzmann Machine (QBM) and a Variational Quantum Circuit (VQC) used for supervised classification.
    
    ???+ info "Answer Strategy"
        The key difference lies in their fundamental purpose and the type of task they are designed to solve.
    
        1.  **Model Type and Goal:**
            *   **VQC (Discriminative):** A VQC used for classification is a **discriminative model**. Its goal is to learn a *decision boundary* that separates different classes of data. It learns a mapping from an input to a specific output label ($f: x \to y$).
            *   **QBM (Generative):** A QBM is a **generative model**. Its goal is to learn the *underlying probability distribution* of the dataset itself, $P(x)$. It is not trying to classify data, but to understand and replicate its structure.
    
        2.  **Function and Output:**
            *   **VQC:** Takes a data point as input and outputs a **prediction** (e.g., "Class A" or "Class B").
            *   **QBM:** Does not take an input in the same way. Once trained, its output is a **new sample** that is statistically similar to the data it was trained on.
    
        **Analogy:** A VQC is like a bank teller trained to distinguish genuine banknotes from counterfeit ones. A QBM is like a master forger trained to create new banknotes that are indistinguishable from the real thing.
    
---

### **<i class="fa-solid fa-flask"></i> Hands-On Projects**

#### **Project Blueprint: QBM Energy and Probability**

| Component | Description |
| :--- | :--- |
| **Objective** | Calculate the relative probability of two states in a simple QBM model based on their energies. |
| **Mathematical Concept** | The Boltzmann distribution, where the probability ratio of two states is given by $P(x_1)/P(x_2) = e^{-\beta(E_1 - E_2)}$. |
| **Experiment Setup** | A two-qubit QBM with a simple Ising Hamiltonian $H = Z_0 Z_1$. We will compare the states $\|01\rangle$ and $\|00\rangle$ at an inverse temperature $\beta=1$. |
| **Process Steps** | 1. Calculate the energy $E = \langle \psi | H | \psi \rangle$ for the states $\|01\rangle$ and $\|00\rangle$. <br> 2. Calculate the energy difference $\Delta E$. <br> 3. Compute the probability ratio using the Boltzmann factor $e^{-\beta \Delta E}$. |
| **Expected Behavior** | The state with the lower energy will be exponentially more probable than the state with the higher energy. |
| **Verification Goal** | Quantify the probability ratio to demonstrate how the Hamiltonian's energy landscape directly shapes the model's output distribution. |

---

#### **Python Implementation**

```python
import numpy as np

# Project 3: Quantum Boltzmann Machine – Energy and Probability

def rbm_energy(v, h, W, b_v, b_h):
    """Energy of a Restricted Boltzmann Machine configuration."""
    return -(v @ W @ h + b_v @ v + b_h @ h)

def gibbs_probability(v, W, b_v, b_h):
    """Marginal probability P(v) = sum_h exp(-E(v,h)) / Z (unnormalized)."""
    n_h = len(b_h)
    # Sum over all hidden configurations
    unnorm = 0.0
    for h_int in range(2**n_h):
        h = np.array([(h_int >> j) & 1 for j in range(n_h)], dtype=float)
        unnorm += np.exp(-rbm_energy(v, h, W, b_v, b_h))
    return unnorm

# Small RBM: 2 visible, 2 hidden

W    = np.array([[0.5, -0.3], [0.2, 0.4]])
b_v  = np.array([0.1, -0.1])
b_h  = np.array([0.2, 0.0])

print("RBM unnormalized probabilities P*(v):")
n_v = len(b_v)
total = sum(gibbs_probability(
    np.array([(i>>j)&1 for j in range(n_v)]), W, b_v, b_h
) for i in range(2**n_v))

for v_int in range(2**n_v):
    v = np.array([(v_int >> j) & 1 for j in range(n_v)], dtype=float)
    p = gibbs_probability(v, W, b_v, b_h) / total
    print(f"  v={v.astype(int).tolist()}  P(v) = {p:.4f}")
```
**Sample Output:**
```python
RBM unnormalized probabilities P*(v):
  v=[0, 0]  P(v) = 0.1920
  v=[1, 0]  P(v) = 0.2505
  v=[0, 1]  P(v) = 0.2428
  v=[1, 1]  P(v) = 0.3147
```


#### **Outcome and Interpretation**

The energy of state $|01\rangle$ is $E_1 = -1$, while the energy of state $|00\rangle$ is $E_2 = +1$. The energy difference is $\Delta E = -2$. The probability ratio is $P(|01\rangle)/P(|00\rangle) = e^{-(-2)} = e^2 \approx 7.39$. This result clearly shows that the QBM is significantly more likely to produce the low-energy "anti-aligned" state $|01\rangle$ than the high-energy "aligned" state $|00\rangle$. This simple example demonstrates the core mechanism of a QBM: the structure of the Hamiltonian directly sculpts the probability landscape of the generative model.