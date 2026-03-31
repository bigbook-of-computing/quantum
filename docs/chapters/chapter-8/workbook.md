# **Chapter 8: Quantum Machine Learning Foundations (Workbook)**

---

> **Summary:** This chapter introduces Quantum Machine Learning (QML), a field that merges quantum computing and machine learning to address classical computational bottlenecks. We explore the core motivations for QML, including quantum speedups for linear algebra and search, and the ability to process high-dimensional data in vast Hilbert spaces. The chapter contrasts quantum and classical learning paradigms, detailing both provable advantages, like the HHL algorithm's exponential speedup, and heuristic benefits from the enhanced expressivity of variational circuits. By examining supervised, unsupervised, and reinforcement learning through a quantum lens, we establish the foundational concepts of this transformative discipline.

---

The goal of this chapter is to establish concepts in Quantum Machine Learning and Optimization, exploring how quantum computing can enhance traditional machine learning and optimization frameworks.

---

## **8.1 Motivation: Feature Space and Dimensionality** {.heading-with-pill}

> **Difficulty:** ★★☆☆☆
> 
> **Concept:** Quantum states as exponentially large feature spaces
> 
> **Summary:** Using $n$ qubits yields a Hilbert space of dimension $2^n$, enabling feature mappings that are infeasible classically while confronting encoding and noise constraints.

### **Theoretical Background**

Quantum machine learning exploits the exponential dimensionality of quantum Hilbert spaces to represent and process classical data in ways intractable for classical computers, provided efficient encoding and readout mechanisms exist.

**Hilbert Space Dimension:**  
An $n$-qubit quantum system occupies a complex Hilbert space $\mathcal{H} = (\mathbb{C}^2)^{\otimes n} \cong \mathbb{C}^{2^n}$ with dimension:

$$
\dim(\mathcal{H}) = 2^n
$$

A general normalized state is:

$$
|\psi\rangle = \sum_{j=0}^{2^n-1} c_j |j\rangle, \quad c_j \in \mathbb{C}, \quad \sum_{j=0}^{2^n-1} |c_j|^2 = 1
$$

where $\{|j\rangle\}$ forms the computational basis. The state is characterized by $2^{n+1}$ real parameters (real and imaginary parts, minus normalization and global phase).

**Amplitude Encoding:**  
Given classical data $\mathbf{x} = (x_0, x_1, \ldots, x_{D-1}) \in \mathbb{R}^D$ with norm $\|\mathbf{x}\|_2 = \sqrt{\sum_{i=0}^{D-1} x_i^2}$, amplitude encoding creates:

$$
|\psi(\mathbf{x})\rangle = \frac{1}{\|\mathbf{x}\|_2} \sum_{i=0}^{D-1} x_i |i\rangle
$$

For $D \leq 2^n$, this requires $n = \lceil \log_2 D \rceil$ qubits. If $D < 2^n$, pad with zeros:

$$
|\psi(\mathbf{x})\rangle = \frac{1}{\|\mathbf{x}\|_2} \left(\sum_{i=0}^{D-1} x_i |i\rangle + \sum_{i=D}^{2^n-1} 0 \cdot |i\rangle\right)
$$

**Quantum Feature Maps:**  
A quantum feature map $\Phi: \mathbb{R}^d \to \mathcal{H}$ is implemented by a parameterized circuit:

$$
\Phi(\mathbf{x}) = |\psi(\mathbf{x})\rangle = U(\mathbf{x})|0\rangle^{\otimes n}
$$

where $U(\mathbf{x})$ applies gates whose parameters depend on input features. Common encodings:

**1. Angle Encoding (Basis Encoding):**
$$
U(\mathbf{x}) = \bigotimes_{i=1}^{\min(d,n)} R_y(x_i) = \bigotimes_{i=1}^{\min(d,n)} \begin{pmatrix} \cos(x_i/2) & -\sin(x_i/2) \\ \sin(x_i/2) & \cos(x_i/2) \end{pmatrix}_i
$$

This creates product state:
$$
|\psi(\mathbf{x})\rangle = \bigotimes_{i=1}^n \left(\cos(x_i/2)|0\rangle + \sin(x_i/2)|1\rangle\right)
$$

**2. IQP-Style Encoding:**  
Apply Hadamards, then diagonal unitaries, repeated for $L$ layers:

$$
U(\mathbf{x}) = \left[U_Z(\mathbf{x}) \cdot \mathbf{H}^{\otimes n}\right]^L, \quad U_Z(\mathbf{x}) = \exp\left(-i \sum_{S \subseteq [n]} x_S \prod_{j \in S} Z_j\right)
$$

where $x_S$ encodes feature interactions.

**Quantum Kernel Functions:**  
The inner product between feature states defines a kernel:

$$
K(\mathbf{x}, \mathbf{x}') = |\langle\psi(\mathbf{x})|\psi(\mathbf{x}')\rangle|^2
$$

For the IQP encoding with $L=1$:

$$
K(\mathbf{x}, \mathbf{x}') = \left|\frac{1}{2^n}\sum_{z\in\{0,1\}^n} e^{i\phi(\mathbf{x},z)} e^{-i\phi(\mathbf{x}',z)}\right|^2
$$

where $\phi(\mathbf{x},z) = \sum_S x_S \prod_{j\in S} z_j$. This kernel is conjectured hard to compute classically for certain parameter regimes.

**Classical Intractability:**  
Havlíček et al. showed that estimating $K(\mathbf{x}, \mathbf{x}')$ for IQP circuits is $\#P$-hard under plausible complexity assumptions, suggesting quantum advantage for kernel evaluation.

**Measurement and Overlap Estimation:**  
To estimate $K(\mathbf{x}, \mathbf{x}')$, use the SWAP test or destructive interference:

**SWAP Test Circuit:**
$$
\text{Prob}(|0\rangle_{\text{anc}}) = \frac{1 + |\langle\psi(\mathbf{x})|\psi(\mathbf{x}')\rangle|^2}{2}
$$

Solving: $K(\mathbf{x}, \mathbf{x}') = 2 \cdot \text{Prob}(|0\rangle_{\text{anc}}) - 1$

**Resource Scaling:**  
- **Qubit count:** $n = \lceil \log_2 D \rceil$ (exponential compression)  
- **State preparation:** Generic states require $\Theta(2^n)$ gates; structured encodings achieve $\mathcal{O}(\text{poly}(n))$  
- **Kernel estimation:** $\mathcal{O}(1/\epsilon^2)$ measurements for precision $\epsilon$

### **Comprehension Check**

!!! note "Quiz"
    **1. What is the dimension of an $n$-qubit Hilbert space?**
    
    - A. $n$  
    - B. $n^2$  
    - C. $2^n$  
    - D. $\log n$  
    
    **2. What does amplitude encoding require?**
    
    - A. Unnormalized amplitudes  
    - B. Normalized amplitudes with $\sum_k |c_k|^2=1$  
    - C. Only real amplitudes  
    - D. Exactly sparse vectors  
    
??? info "See Answer"
        **1: C** — $\dim\mathcal{H}=2^n$.  
        **2: B** — Quantum states must be normalized to unit length.
    
---

!!! abstract "Interview-Style Question"
    
    **Q:** Explain how quantum feature maps can alleviate the curse of dimensionality, and name a practical caveat in the NISQ era.
    
    ???+ info "Answer Strategy"
        A quantum feature map $\Phi: \mathbb{R}^d \to \mathcal{H}$ embeds classical data into a $2^n$-dimensional Hilbert space using just $n$ qubits.
    
        1.  **Exponential Feature Space:** This mapping allows access to an exponentially large feature space ($2^n$ dimensions) with linear resources ($n$ qubits), theoretically mitigating the classical "curse of dimensionality" where resources scale with dimension $d$.
        2.  **Implicit Computation:** The features, often complex polynomials and trigonometric functions of the input data, are created implicitly through quantum interference without needing classical computation.
        3.  **NISQ-Era Caveat:** The primary caveat is the **data loading bottleneck**. Creating the quantum state that encodes the classical data often requires a number of operations that scales with the size of the data, which can erase the quantum advantage. Additionally, noise on NISQ devices limits the depth of feature maps, restricting their practical expressiveness.
    
### **<i class="fa-solid fa-flask"></i> Hands-On Projects**

#### **Project Blueprint**

| **Section**              | **Description** |
| ------------------------ | --------------- |
| **Objective**            | Relate classical feature dimension $D$ to required qubits $n$ and analyze the induced quantum feature space. |
| **Mathematical Concept** | $\dim\mathcal{H}=2^n$; amplitude normalization; kernel $K(\mathbf{x},\mathbf{x}') = \|\langle\psi(\mathbf{x})|\psi(\mathbf{x}')\rangle\|^2$. |
| **Experiment Setup**     | Consider $D\in\{8, 1024\}$ and compute minimal $n$ with $2^n\ge D$. Analyze space size for $n=16$. |
| **Process Steps**        | Compute $n=\lceil\log_2 D\rceil$; discuss expressivity vs. loading cost; note normalization. |
| **Expected Behavior**    | Small increases in $n$ yield exponential feature growth; benefits depend on feasible encoding. |
| **Tracking Variables**   | $D$, $n$, $2^n$, normalization error. |
| **Verification Goal**    | Consistency with $2^n$ scaling and proper normalization of amplitudes. |
| **Output**               | Table of $(D,n,2^n)$ and discussion of practicality. |

---

#### **Python Implementation**

```python
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector
import numpy as np

# Project 1: Quantum Feature Map (ZZ feature map)

def zz_feature_map(x, reps=2):
    """ZZ feature map for 2 features x = [x0, x1]."""
    n = len(x)
    qc = QuantumCircuit(n)
    for _ in range(reps):
        qc.h(range(n))
        for i in range(n):
            qc.p(2.0 * x[i], i)
        # ZZ interaction
        qc.cx(0, 1)
        qc.p(2.0 * (np.pi - x[0]) * (np.pi - x[1]), 1)
        qc.cx(0, 1)
    return qc

x_sample = [0.5, 1.2]
qc = zz_feature_map(x_sample, reps=2)
sv = Statevector(qc)
print(f"Feature map |φ({x_sample})>:")
print(np.round(sv.data, 4))
print("Norm:", np.linalg.norm(sv.data))
```
**Sample Output:**
```python
Feature map |φ([0.5, 1.2])>:
[0.3221-0.2825j 0.4921-0.5677j 0.3246-0.1715j 0.3349-0.0715j]
Norm: 0.9999999999999997
```


#### **Outcome and Interpretation**

You will see that a modest qubit count accesses exponentially large feature spaces, but only if state preparation is practical and stable.

---

## **8.2 Learning Paradigms and Hybrid Models** {.heading-with-pill}

> **Difficulty:** ★★★☆☆
> 
> **Concept:** Supervised/unsupervised/RL in quantum settings with hybrid training loops
> 
> **Summary:** QML mirrors classical paradigms while replacing linear operators with unitaries and measurements; hybrid quantum–classical optimization dominates in the NISQ regime.

### **Theoretical Background**

Quantum machine learning adapts classical learning paradigms—supervised, unsupervised, and reinforcement learning—by replacing classical models with parameterized quantum circuits, enabling hybrid quantum-classical training loops.

**Parameterized Quantum Circuit Model:**  
A QML model consists of two components:

1. **Feature Map** $U_{\Phi}(\mathbf{x}): \mathbb{R}^d \to \mathcal{U}(2^n)$ encoding classical data  
2. **Variational Ansatz** $U(\vec{\theta}): \mathbb{R}^m \to \mathcal{U}(2^n)$ with trainable parameters $\vec{\theta} = (\theta_1, \ldots, \theta_m)$

The combined state is:

$$
|\psi(\mathbf{x}; \vec{\theta})\rangle = U(\vec{\theta}) \cdot U_{\Phi}(\mathbf{x}) \cdot |0\rangle^{\otimes n}
$$

**Supervised Learning Architecture:**  
For binary classification with labels $y \in \{-1, +1\}$, the model predicts via observable measurement:

$$
\hat{y}(\mathbf{x}; \vec{\theta}) = \text{sign}\left(\langle\psi(\mathbf{x}; \vec{\theta})|\mathbf{M}|\psi(\mathbf{x}; \vec{\theta})\rangle - b\right)
$$

where:
- $\mathbf{M}$ is a measurement observable (typically Pauli operator like $\mathbf{Z}_0$ or $\sum_i \mathbf{Z}_i$)  
- $b \in \mathbb{R}$ is a bias threshold

**Loss Functions:**  
**1. Hinge Loss (SVM-style):**
$$
\mathcal{L}_{\text{hinge}}(\vec{\theta}) = \frac{1}{N}\sum_{i=1}^N \max\left(0, 1 - y_i \langle\mathbf{M}\rangle_i\right)
$$

**2. Mean Squared Error:**
$$
\mathcal{L}_{\text{MSE}}(\vec{\theta}) = \frac{1}{N}\sum_{i=1}^N \left(y_i - \langle\mathbf{M}\rangle_i\right)^2
$$

**3. Cross-Entropy (Softmax):**  
For multi-class with $C$ classes, measure $C$ observables $\{\mathbf{M}_c\}$:

$$
p_c(\mathbf{x}; \vec{\theta}) = \frac{e^{\langle\mathbf{M}_c\rangle}}{\sum_{c'=1}^C e^{\langle\mathbf{M}_{c'}\rangle}}
$$

$$
\mathcal{L}_{\text{CE}}(\vec{\theta}) = -\frac{1}{N}\sum_{i=1}^N \sum_{c=1}^C y_{i,c} \log p_c(\mathbf{x}_i; \vec{\theta})
$$

**Gradient Computation:**  
For parameterized gates $U(\theta_j) = e^{-i\theta_j G_j}$ with generator $G_j$ satisfying $G_j^2 = \mathbf{I}$, the parameter-shift rule gives:

$$
\frac{\partial \langle\mathbf{M}\rangle}{\partial \theta_j} = \frac{1}{2}\left[\langle\mathbf{M}\rangle_{\theta_j + \pi/2} - \langle\mathbf{M}\rangle_{\theta_j - \pi/2}\right]
$$

Chain rule yields loss gradients:

$$
\frac{\partial \mathcal{L}}{\partial \theta_j} = \sum_{i=1}^N \frac{\partial \mathcal{L}}{\partial \langle\mathbf{M}\rangle_i} \cdot \frac{\partial \langle\mathbf{M}\rangle_i}{\partial \theta_j}
$$

**Unsupervised Learning:**  
**Quantum Principal Component Analysis (qPCA):**  
Given density matrix $\rho = \frac{1}{N}\sum_{i=1}^N |\psi(\mathbf{x}_i)\rangle\langle\psi(\mathbf{x}_i)|$, use variational circuits to approximate leading eigenvectors:

$$
\max_{|\phi(\vec{\theta})\rangle} \langle\phi(\vec{\theta})|\rho|\phi(\vec{\theta})\rangle
$$

subject to orthogonality with previous components.

**Quantum Clustering:**  
Use quantum state fidelity as distance metric:

$$
D(\mathbf{x}, \mathbf{x}') = \sqrt{1 - |\langle\psi(\mathbf{x})|\psi(\mathbf{x}')\rangle|^2}
$$

Apply quantum-enhanced k-means or hierarchical clustering.

**Reinforcement Learning:**  
**Quantum Policy Gradient:**  
Agent policy parameterized by quantum circuit:

$$
\pi(a|s; \vec{\theta}) = |\langle a|U(\vec{\theta})U_{\Phi}(s)|0\rangle|^2
$$

where $s$ is state, $a$ is action. The policy gradient theorem:

$$
\nabla_{\vec{\theta}} J(\vec{\theta}) = \mathbb{E}_{\tau \sim \pi_{\vec{\theta}}}\left[\sum_{t=0}^T \nabla_{\vec{\theta}} \log \pi(a_t|s_t; \vec{\theta}) \cdot R_t\right]
$$

where $R_t = \sum_{t'=t}^T \gamma^{t'-t} r_{t'}$ is return.

**Hybrid Training Loop:**

1. **Quantum Forward Pass:** Prepare $|\psi(\mathbf{x}_i; \vec{\theta})\rangle$, measure $\langle\mathbf{M}\rangle_i$  
2. **Classical Loss:** Compute $\mathcal{L}(\vec{\theta})$ from measurements  
3. **Classical Gradient:** Estimate $\nabla_{\vec{\theta}} \mathcal{L}$ via parameter-shift or finite differences  
4. **Classical Update:** $\vec{\theta}_{k+1} = \vec{\theta}_k - \eta \nabla_{\vec{\theta}} \mathcal{L}(\vec{\theta}_k)$  
5. **Iterate** until convergence

**Entanglement as Resource:**  
The quantum advantage arises from entanglement in $|\psi(\mathbf{x}; \vec{\theta})\rangle$. For separable states:

$$
|\psi\rangle = |\psi_1\rangle \otimes |\psi_2\rangle \otimes \cdots \otimes |\psi_n\rangle
$$

the model reduces to classical computation. Entanglement enables correlations:

$$
\langle Z_i Z_j \rangle \neq \langle Z_i \rangle \langle Z_j \rangle
$$

Which classical models cannot efficiently capture.

```mermaid
flowchart LR
    D[Data x] --> E["Encode U_Φ(x)"]
    E --> U["Parametric U(θ)"]
    U --> M[Measure M]
    M --> C[Classical loss/grad]
    C --> O[Optimizer update θ]
    O --> U
```

### **Comprehension Check**

!!! note "Quiz"
    **1. Which resource grants non-classical correlations in QML models?**
    
    - A. Dropout  
    - B. Entanglement  
    - C. Weight decay  
    - D. Batch norm  
    
    **2. Why are hybrid loops prevalent on NISQ devices?**
    
    - A. Unlimited coherence  
    - B. Deep circuits are error-free  
    - C. Quantum is used for feature mapping while classical optimizes  
    - D. Measurements are unnecessary  
    
??? info "See Answer"
        **1: B** — Entanglement enables correlations absent from classical models.  
        **2: C** — Hybrid training mitigates noise while leveraging quantum expressivity.
    
---

!!! abstract "Interview-Style Question"
    
    **Q:** Describe the roles of $\mathbf{U}_\Phi(\mathbf{x})$ and $\mathbf{U}(\mathbf{\theta})$ in a hybrid classifier.
    
    ???+ info "Answer Strategy"
        In a hybrid classifier, the two unitaries have distinct roles:
    
        1.  **$U_\Phi(\mathbf{x})$ (Feature Map):** This is a **fixed** circuit that **encodes** the classical input data $\mathbf{x}$ into a quantum state. It acts as the quantum equivalent of feature engineering, mapping the data into a high-dimensional Hilbert space.
        2.  **$U(\mathbf{\theta})$ (Variational Ansatz):** This is a **trainable** circuit with parameters $\mathbf{\theta}$. It processes the encoded state, and its parameters are optimized by a classical computer to learn the classification task. It is analogous to the hidden layers of a classical neural network.
    
### **<i class="fa-solid fa-flask"></i> Hands-On Projects**

#### **Project Blueprint**

| **Section**              | **Description** |
| ------------------------ | --------------- |
| **Objective**            | Draft a 4-qubit hybrid VQC classifier for binary digits (0 vs 1). |
| **Mathematical Concept** | Expectation-value classifier $\hat{y}(\mathbf{x})=\operatorname{sign}(\langle \mathbf{M} \rangle - b)$. |
| **Experiment Setup**     | Choose $\mathbf{M}=\mathbf{Z}_0$; encode $\mathbf{x}$ via $\mathbf{U}_\Phi(\mathbf{x})$; 2–3 ansatz layers. |
| **Process Steps**        | Specify encoding, ansatz, measurement, loss, and classical optimizer. |
| **Expected Behavior**    | Training reduces loss and improves accuracy on a small balanced set. |
| **Tracking Variables**   | Parameters $\mathbf{\theta}$, loss, accuracy, shot count. |
| **Verification Goal**    | Show monotone loss decrease and non-trivial accuracy (>50%). |
| **Output**               | Design spec and training log summary. |

---

#### **Python Implementation**

```python
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector
import numpy as np

# Project 2: Quantum Kernel Estimation

def zz_feature_map(x, n=2, reps=1):
    qc = QuantumCircuit(n)
    qc.h(range(n))
    for i in range(n): qc.p(2*x[i], i)
    qc.cx(0,1); qc.p(2*(np.pi-x[0])*(np.pi-x[1]),1); qc.cx(0,1)
    return qc

def quantum_kernel(x1, x2):
    """K(x1,x2) = |<phi(x1)|phi(x2)>|^2"""
    sv1 = Statevector(zz_feature_map(x1))
    sv2 = Statevector(zz_feature_map(x2))
    return abs(sv1.inner(sv2))**2

# Small kernel matrix for demonstration

X = [[0.1, 0.2], [0.5, 0.6], [0.9, 0.8]]
n = len(X)
K = np.zeros((n, n))
for i in range(n):
    for j in range(n):
        K[i, j] = quantum_kernel(X[i], X[j])

print("Quantum kernel matrix:")
print(np.round(K, 4))
print("Diagonal (self-overlap, should be ~1):", np.diag(K))
```
**Sample Output:**
```python
Quantum kernel matrix:
[[1.     0.2866 0.2841]
 [0.2866 1.     0.015 ]
 [0.2841 0.015  1.    ]]
Diagonal (self-overlap, should be ~1): [1. 1. 1.]
```


#### **Outcome and Interpretation**

This exercise clarifies the division of labor: shallow quantum feature maps plus classical optimizers deliver trainable models on NISQ devices.

---

## **8.3 Speedups vs. Representational Advantages** {.heading-with-pill}

> **Difficulty:** ★★★★☆
> 
> **Concept:** HHL/qPCA speedups and heuristic quantum kernels
> 
> **Summary:** Some quantum algorithms offer provable asymptotic speedups, while variational models and kernels provide heuristic advantages rooted in high-dimensional, entangled representations.

### **Theoretical Background**

Quantum machine learning advantages fall into two categories: provable asymptotic speedups for specific linear algebra problems, and heuristic representational benefits from high-dimensional quantum feature spaces.

**Provable Speedup: HHL Algorithm:**  
The Harrow-Hassidim-Lloyd (HHL) algorithm solves linear systems $\mathbf{A}\mathbf{x} = \mathbf{b}$ where $\mathbf{A} \in \mathbb{C}^{N \times N}$ is Hermitian and $\mathbf{b} \in \mathbb{C}^N$ with $N = 2^n$.

**Problem Setup:**  
Given quantum state $|b\rangle$ encoding $\mathbf{b}$ and oracle access to $\mathbf{A}$, prepare:

$$
|x\rangle \propto \mathbf{A}^{-1}|b\rangle = \sum_{j=1}^N \frac{\beta_j}{\lambda_j}|u_j\rangle
$$

where $\mathbf{A}|u_j\rangle = \lambda_j|u_j\rangle$ and $|b\rangle = \sum_j \beta_j |u_j\rangle$.

**HHL Protocol:**

**Step 1: Eigenvalue Estimation (QPE)**  
Apply quantum phase estimation to encode eigenvalues in ancilla register:

$$
|0\rangle_{\text{anc}} \otimes \sum_j \beta_j |u_j\rangle \xrightarrow{\text{QPE}} \sum_j \beta_j |\tilde{\lambda}_j\rangle_{\text{anc}} \otimes |u_j\rangle
$$

where $|\tilde{\lambda}_j\rangle$ encodes eigenvalue $\lambda_j$ to $t$-bit precision.

**Step 2: Controlled Rotation**  
Apply controlled rotation on auxiliary qubit:

$$
R(\lambda) = \begin{pmatrix} \sqrt{1 - C^2/\lambda^2} & -C/\lambda \\ C/\lambda & \sqrt{1 - C^2/\lambda^2} \end{pmatrix}
$$

for normalization constant $C \leq \lambda_{\min}$. The state becomes:

$$
\sum_j \beta_j |\tilde{\lambda}_j\rangle \otimes |u_j\rangle \otimes \left(\sqrt{1 - C^2/\lambda_j^2}|0\rangle + \frac{C}{\lambda_j}|1\rangle\right)
$$

**Step 3: Uncompute and Measure**  
Reverse QPE, measure auxiliary qubit. Success (outcome $|1\rangle$) yields:

$$
|x\rangle = \frac{1}{\|\mathbf{A}^{-1}\mathbf{b}\|} \sum_j \frac{\beta_j}{\lambda_j}|u_j\rangle = \frac{\mathbf{A}^{-1}|b\rangle}{\|\mathbf{A}^{-1}\mathbf{b}\|}
$$

**Complexity Analysis:**  
- **QPE depth:** $\mathcal{O}(t \cdot \tau)$ where $t = \mathcal{O}(\log(N/\epsilon))$ precision bits, $\tau$ is time to simulate $e^{i\mathbf{A}t}$  
- **Condition number:** For sparse $\mathbf{A}$ with sparsity $s$, $\tau = \mathcal{O}(s \log N)$  
- **Total complexity:** $\mathcal{O}(s \kappa^2 \log(N) / \epsilon)$ where $\kappa = \lambda_{\max}/\lambda_{\min}$ is condition number

**Classical Comparison:**  
Conjugate gradient: $\mathcal{O}(N s \kappa \log(1/\epsilon))$. Speedup is exponential in $n$ when $N = 2^n$:

$$
\frac{T_{\text{classical}}}{T_{\text{HHL}}} \sim \frac{2^n s \kappa}{s \kappa^2 n} = \frac{2^n}{n\kappa}
$$

For $\kappa = \mathcal{O}(\text{poly}(n))$, this is exponential.

**Critical Assumptions:**  
1. **Efficient state preparation:** Creating $|b\rangle$ from classical $\mathbf{b}$ requires $\mathcal{O}(N)$ operations generically  
2. **Hamiltonian simulation:** $e^{i\mathbf{A}t}$ must be implementable in $\mathcal{O}(\text{poly}(\log N))$  
3. **Quantum output:** Extracting classical $\mathbf{x}$ requires tomography ($\mathcal{O}(N)$); advantage holds only for quantum expectations $\langle x|\mathbf{O}|x\rangle$

**Quantum Principal Component Analysis (qPCA):**  
Lloyd et al.'s algorithm finds principal components of $\rho = \sum_i p_i |\psi_i\rangle\langle\psi_i|$ in time:

$$
\mathcal{O}\left(\frac{\log(N)}{\delta^2 \epsilon^2}\right)
$$

versus classical $\mathcal{O}(N^2/\epsilon)$ for $N \times N$ covariance matrix.

**Heuristic Advantage: Quantum Kernels:**  
For quantum feature map $\Phi(\mathbf{x}) = |\psi(\mathbf{x})\rangle$, the quantum kernel is:

$$
K_Q(\mathbf{x}, \mathbf{x}') = |\langle\psi(\mathbf{x})|\psi(\mathbf{x}')\rangle|^2
$$

**Computational Hardness Conjecture:**  
For IQP-type circuits, computing $K_Q(\mathbf{x}, \mathbf{x}')$ is $\#P$-hard assuming polynomial hierarchy non-collapse. No known classical algorithm computes it in poly$(n)$ time.

**Kernel Method Performance:**  
Given training data $\{(\mathbf{x}_i, y_i)\}_{i=1}^N$, kernel ridge regression predicts:

$$
f(\mathbf{x}) = \sum_{i=1}^N \alpha_i K_Q(\mathbf{x}, \mathbf{x}_i)
$$

where $\vec{\alpha} = (\mathbf{K} + \lambda \mathbf{I})^{-1}\vec{y}$ and $\mathbf{K}_{ij} = K_Q(\mathbf{x}_i, \mathbf{x}_j)$.

**Sample Complexity:**  
For hypothesis class with Rademacher complexity $\mathcal{R}_N$, generalization bound:

$$
|\mathcal{L}_{\text{test}} - \mathcal{L}_{\text{train}}| \leq 2\mathcal{R}_N + \mathcal{O}\left(\sqrt{\frac{\log(1/\delta)}{N}}\right)
$$

Quantum kernels may have smaller $\mathcal{R}_N$ for certain problems, reducing sample complexity.

**Variational Quantum Circuit Expressivity:**  
Deep variational circuits with $L$ layers create states that are $\epsilon$-close to arbitrary states with:

$$
L \sim \mathcal{O}\left(\frac{2^n}{\epsilon}\right)
$$

gates (Solovay-Kitaev). For structured problems, polynomial $L$ may suffice.

### **Comprehension Check**

!!! note "Quiz"
    **1. HHL primarily accelerates which task?**
    
    - A. Sorting  
    - B. Linear system solving  
    - C. Graph traversal  
    - D. Hashing  
    
    **2. Quantum kernels rely on what key ingredient?**
    
    - A. Low-dimensional embeddings  
    - B. Entangled, high-dimensional feature states  
    - C. Classical Fourier features  
    - D. Dropout  
    
??? info "See Answer"
        **1: B** — HHL addresses $\mathbf{A}\mathbf{x}=\mathbf{b}$.  
        **2: B** — Kernels arise from overlaps of high-dimensional quantum states.
    
---

!!! abstract "Interview-Style Question"
    
    **Q:** Contrast provable speedups (HHL, qPCA) with heuristic advantages (VQCs, kernels) in QML deployment.
    
    ???+ info "Answer Strategy"
        There are two main types of quantum advantage claims:
    
        1.  **Provable Speedups (e.g., HHL):** These algorithms offer a theoretically guaranteed, often exponential, speedup over the best-known classical algorithms for specific tasks like solving linear systems. However, they typically rely on unavailable hardware (like qRAM) and oracles, making them impractical for near-term deployment.
        2.  **Heuristic Advantages (e.g., VQCs, Quantum Kernels):** These methods leverage the unique properties of quantum mechanics, like high-dimensional Hilbert spaces and entanglement, to create powerful models. There is no formal proof of a speedup, and their performance is problem-dependent. They are compatible with today's noisy, intermediate-scale quantum (NISQ) devices but face challenges like trainability and noise.
    
        In summary, provable speedups are a long-term goal requiring fault-tolerant quantum computers, while heuristic methods are the focus of current research for finding practical applications on NISQ hardware.
    
### **<i class="fa-solid fa-flask"></i> Hands-On Projects**

#### **Project Blueprint**

| **Section**              | **Description** |
| ------------------------ | --------------- |
| **Objective**            | Compare storage/operation costs for classical $\mathbb{R}^{2^n}$ vectors vs. $n$-qubit states. |
| **Mathematical Concept** | State size vs. gate complexity; $O(\operatorname{poly}(n))$ gate depth vs. $2^n$ explicit storage. |
| **Experiment Setup**     | Evaluate $n\in\{3,10\}$; count floats for classical/quantum representations. |
| **Process Steps**        | Compute storage for $\mathbb{R}^{2^n}$ and complex amplitudes; discuss $O(\operatorname{poly}(n))$ circuit actions. |
| **Expected Behavior**    | Storage explodes classically while gate counts remain polynomial in $n$. |
| **Tracking Variables**   | $n$, storage counts, estimated gate depths. |
| **Verification Goal**    | Confirm exponential-vs-polynomial contrast. |
| **Output**               | Summary table and narrative comparison. |

---

#### **Python Implementation**

```python
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector, SparsePauliOp
from scipy.optimize import minimize
import numpy as np

# Project 3: Variational Quantum Classifier (VQC)

def vqc(x, theta):
    qc = QuantumCircuit(2)
    # Encoding layer
    qc.ry(x[0], 0); qc.ry(x[1], 1)
    # Variational layer
    qc.ry(theta[0], 0); qc.ry(theta[1], 1)
    qc.cx(0, 1)
    qc.ry(theta[2], 0); qc.ry(theta[3], 1)
    return qc

observable = SparsePauliOp('ZI')  # measure first qubit

def predict(x, theta):
    sv = Statevector(vqc(x, theta))
    return sv.expectation_value(observable).real  # in [-1, 1]

# Simple dataset: class +1 if x0>x1 else -1

data  = [[0.2,0.8],  [0.7,0.3],  [0.1,0.9],  [0.8,0.2]]
labels = [-1, +1, -1, +1]

def loss(theta):
    return sum((predict(x,theta) - y)**2 for x,y in zip(data,labels))

theta_opt = minimize(loss, x0=np.zeros(4), method='COBYLA',
                     options={'maxiter':500}).x
print("VQC predictions vs labels:")
for x, y in zip(data, labels):
    pred = predict(x, theta_opt)
    print(f"  x={x}, label={y:+d}, pred={pred:+.3f}")
```
**Sample Output:**
```python
VQC predictions vs labels:
  x=[0.2, 0.8], label=-1, pred=-0.345
  x=[0.7, 0.3], label=+1, pred=+0.344
  x=[0.1, 0.9], label=-1, pred=-0.471
  x=[0.8, 0.2], label=+1, pred=+0.470
```


#### **Outcome and Interpretation**

This comparison highlights why quantum circuits can act on exponentially large state spaces without explicitly materializing them.

---

## **8.4 Practical Constraints: Data Loading and Noise** {.heading-with-pill}

> **Difficulty:** ★★★☆☆
> 
> **Concept:** Encoding cost and measurement overhead on NISQ
> 
> **Summary:** The data-loading bottleneck and finite-shot estimation constrain end-to-end speedups; careful encoding, grouping of commuting measurements, and hybrid loops mitigate costs.

### **Theoretical Background**

While quantum algorithms offer theoretical speedups, practical quantum machine learning faces fundamental bottlenecks in data encoding and measurement that can eliminate asymptotic advantages for classical datasets.

**State Preparation Complexity:**  
Creating quantum state $|\psi\rangle = \sum_{i=0}^{N-1} c_i |i\rangle$ from classical data $\{c_i\}$ requires implementing unitary:

$$
U_{\text{prep}}: |0\rangle^{\otimes n} \mapsto \sum_{i=0}^{2^n-1} c_i |i\rangle
$$

**Generic Complexity:**  
For arbitrary $\{c_i\}$ with no structure, state preparation requires:

$$
T_{\text{prep}} = \Theta(N) = \Theta(2^n)
$$

gates. Proof via counting argument: specifying $N$ complex amplitudes requires $\Omega(N)$ real parameters, each needing $\Omega(1)$ gates to set.

**Efficient Encodings (Structured Data):**

**1. Product States:**  
For separable encoding $|\psi\rangle = \bigotimes_{i=1}^n (\alpha_i|0\rangle + \beta_i|1\rangle)$:

$$
U_{\text{prep}} = \bigotimes_{i=1}^n R_y(\theta_i)
$$

requires only $\mathcal{O}(n)$ gates, but represents limited function class.

**2. Low-Depth Circuits:**  
For functions $f: \{0,1\}^n \to \mathbb{R}$ with efficient quantum representation:

$$
|f\rangle = \frac{1}{\sqrt{N}}\sum_{x=0}^{N-1} f(x)|x\rangle
$$

Examples with $\mathcal{O}(\text{poly}(n))$ preparation:
- **Polynomial functions:** $f(x) = \sum_{k=0}^d a_k x^k$ via quantum arithmetic  
- **Trigonometric series:** $f(x) = \sum_k b_k \sin(kx)$ via QFT  
- **Sparse functions:** $\|f\|_0 = s \ll N$ requires $\mathcal{O}(s \log N)$ gates

**3. qRAM-Assisted Preparation:**  
Quantum Random Access Memory provides oracle:

$$
U_{\text{qRAM}}|i\rangle|0\rangle = |i\rangle|c_i\rangle
$$

with query depth $\mathcal{O}(\log N)$. Combined with coherent superposition creation:

$$
|\psi\rangle = \frac{1}{\sqrt{N}}\sum_{i=0}^{N-1} |i\rangle|c_i\rangle \xrightarrow{\text{arith}} \sum_{i=0}^{N-1} c_i |i\rangle|0\rangle
$$

Total depth: $\mathcal{O}(\log N)$. **Critical issue:** qRAM itself requires $\Theta(N)$ active quantum memory cells with coherent addressing—not demonstrated beyond toy systems.

**Measurement Shot Noise:**  
Estimating observable expectation $\langle\mathbf{M}\rangle = \text{Tr}(\mathbf{M}\rho)$ from finite samples:

$$
\widehat{\langle\mathbf{M}\rangle} = \frac{1}{N_{\text{shots}}}\sum_{k=1}^{N_{\text{shots}}} m_k, \quad m_k \in \{\pm 1\}
$$

For eigenvalues $\pm 1$, the variance is:

$$
\text{Var}[\widehat{\langle\mathbf{M}\rangle}] = \frac{\langle\mathbf{M}^2\rangle - \langle\mathbf{M}\rangle^2}{N_{\text{shots}}} = \frac{1 - \langle\mathbf{M}\rangle^2}{N_{\text{shots}}} \leq \frac{1}{N_{\text{shots}}}
$$

Standard error:

$$
\sigma[\widehat{\langle\mathbf{M}\rangle}] = \frac{1}{\sqrt{N_{\text{shots}}}}
$$

To achieve precision $\epsilon$, require:

$$
N_{\text{shots}} \sim \mathcal{O}(1/\epsilon^2)
$$

**Multi-Observable Estimation:**  
For Hamiltonian $\mathbf{H} = \sum_{j=1}^T c_j \mathbf{P}_j$ with $T$ Pauli terms:

**Naive approach:** Measure each term independently  
- Total measurements: $T \cdot N_{\text{shots}}$  
- Variance: $\sum_{j=1}^T c_j^2 / N_{\text{shots}}$

**Commuting group optimization:**  
Partition into $M$ commuting groups $\{\mathcal{G}_m\}$ with $M \ll T$. Optimal shot allocation:

$$
N_m^* = N_{\text{total}} \cdot \frac{\sigma_m}{\sum_{k=1}^M \sigma_k}
$$

where $\sigma_m^2 = \text{Var}[\sum_{\mathbf{P}_j \in \mathcal{G}_m} c_j \mathbf{P}_j]$. Achieves minimal variance:

$$
\text{Var}_{\min} = \frac{1}{N_{\text{total}}}\left(\sum_{m=1}^M \sigma_m\right)^2
$$

**End-to-End Complexity for Classical Data:**  
Consider HHL applied to classical dataset:

$$
T_{\text{total}} = T_{\text{prep}} + T_{\text{HHL}} + T_{\text{meas}}
$$

With $N$ data points:
- $T_{\text{prep}} = \Theta(N)$ (classical data loading)  
- $T_{\text{HHL}} = \mathcal{O}(\log N \cdot \text{poly}(\kappa))$ (quantum solver)  
- $T_{\text{meas}} = \mathcal{O}(N)$ (full readout for classical output)

**Result:** $T_{\text{total}} = \Theta(N)$—the $\mathcal{O}(\log N)$ quantum subroutine is dominated by classical I/O, eliminating exponential speedup.

**Regimes Preserving Advantage:**

1. **Quantum-to-Quantum Workflows:**  
   - Input $|b\rangle$ from quantum simulation (no classical encoding)  
   - Output $|x\rangle$ used for quantum expectation $\langle x|\mathbf{O}|x\rangle$ (no full tomography)  
   - Example: Quantum chemistry pipeline

2. **Structured Classical Data:**  
   - Polynomial functions, sparse vectors with $\mathcal{O}(\text{poly}(\log N))$ encoding  
   - Fourier-sparse signals via QFT-based preparation

3. **Query Complexity Focus:**  
   - Count oracle queries to $\mathbf{A}$, $\mathbf{b}$ rather than wall-clock time  
   - Quantum: $\mathcal{O}(\kappa^2 \log N)$ queries  
   - Classical: $\mathcal{O}(\kappa N)$ queries  
   - Meaningful if oracle evaluation expensive

**NISQ-Era Mitigation Strategies:**

1. **Hybrid data encoding:** Classical preprocessing + shallow quantum feature maps  
2. **Cached state reuse:** Prepare $|\psi(\mathbf{x})\rangle$ once, use for multiple measurements  
3. **Importance sampling:** Allocate shots based on term variance  
4. **Error mitigation:** Zero-noise extrapolation, probabilistic error cancellation

### **Comprehension Check**

!!! note "Quiz"
    **1. How many qubits are needed to encode $N$ amplitudes (power of two)?**
    
    - A. $N$  
    - B. $\sqrt{N}$  
    - C. $\log_2 N$  
    - D. $\ln N$  
    
    **2. What reduces the variance of expectation estimates?**
    
    - A. Fewer shots  
    - B. More shots and commuting-term grouping  
    - C. Ignoring noise  
    - D. Deeper ansatz  
    
??? info "See Answer"
        **1: C** — $n=\lceil\log_2 N\rceil$ qubits suffice.  
        **2: B** — Shot count and grouped measurements lower estimator variance.
    
---

!!! abstract "Interview-Style Question"
    
    **Q:** Explain why $\Theta(N)$ state preparation can erase HHL's asymptotic advantage if the dataset is classical.
    
    ???+ info "Answer Strategy"
        **HHL's Promised Speedup:**  
        The Harrow-Hassidim-Lloyd (HHL) algorithm solves linear systems $A\mathbf{x} = \mathbf{b}$ with quantum complexity $O(\log(N) s^2 \kappa^2 / \epsilon)$ versus classical $O(N s \kappa \log(1/\epsilon))$ (conjugate gradient)—an **exponential speedup**: $O(\log N)$ quantum vs $O(N)$ classical.
        
        However, this comparison **hides a critical bottleneck**: quantum state preparation.
    
        **The State Preparation Problem:**  
        HHL requires encoding classical vector $\mathbf{b} \in \mathbb{R}^N$ as a quantum state:
        
        $$
        |b\rangle = \frac{1}{\|\mathbf{b}\|} \sum_{i=1}^N b_i |i\rangle
        $$
        
        **Key Challenge**: Creating arbitrary quantum state $|b\rangle$ from classical data $\mathbf{b}$ requires:
        
        1. **Reading the data**: Access all $N$ components $b_1, \ldots, b_N$ → $\Theta(N)$ classical operations  
        2. **Gate complexity**: For generic $|b\rangle$, requires $\Theta(N)$ gates (no known efficient circuit)  
        3. **Information-theoretic bound**: $N$-dimensional vector contains $N$ real numbers; must read all values at least once → $\Omega(N)$ time
        
        **Total Runtime**: $T_{\text{total}} = T_{\text{prep}} + T_{\text{HHL}} = \Theta(N) + O(\log N) = \Theta(N)$  
        The $O(\log N)$ quantum solver is **dominated** by $\Theta(N)$ classical preprocessing—**the exponential speedup vanishes**!
    
        **The qRAM Assumption:**  
        HHL complexity analyses assume a **quantum random access memory (qRAM)** oracle that loads data in $O(\log N)$ depth:
        
        $$
        U_{\text{qRAM}} |i\rangle |0\rangle = |i\rangle |b_i\rangle
        $$
        
        **Problem**: qRAM doesn't exist!
        - Requires $\Theta(N)$ quantum memory cells with active error correction  
        - Proposed architectures (bucket-brigade) have polynomial overhead  
        - No experimental demonstration beyond toy systems ($N < 10$)  
        - Even with qRAM, loading classical data into qRAM takes $\Theta(N)$ operations—negating speedup
    
        **When Does HHL Actually Help?**  
        
        **1. Quantum-Native Data:**  
        Input state $|b\rangle$ is **already quantum**—no classical loading needed:
        - **Quantum simulation**: $|b\rangle$ is molecular wavefunction  
        - **Quantum sensors**: $|b\rangle$ from measurement apparatus  
        - **Prior quantum algorithm**: $|b\rangle$ output of previous subroutine
        
        **Example**: Quantum chemistry pipeline produces $|b\rangle$ → HHL solves linear response → output $|x\rangle$ used for property calculation. **No classical data loading**!
        
        **2. Query Complexity Model:**  
        If analyzing **query complexity** (oracle calls to $A$, $\mathbf{b}$) rather than wall-clock time:
        - Classical CG: $O(N \kappa)$ queries  
        - Quantum HHL: $O(\kappa^2 \log N)$ queries—exponential reduction meaningful if querying $A$ is expensive and we only need quantum output $|x\rangle$
        
        **3. Structured State Preparation:**  
        Some vectors have efficient circuits:
        - **Discretized functions**: $b_i = f(x_i)$ for simple $f$ → $O(\text{poly}(\log N))$ via quantum arithmetic  
        - **Sparse vectors**: $\|\mathbf{b}\|_0 = k \ll N$ → prepare in $O(k \log N)$ time  
        - **Example**: $b_i = \sin(i\pi/N)$ prepared in $O(\log^2 N)$ depth via quantum Fourier synthesis
    
        **The Matrix Encoding Problem:**  
        HHL also requires **block-encoding of $A$** as unitary $U_A$. For general dense matrix:
        - **Generic encoding**: $O(N^2)$ gates (reading all entries)—erases advantage  
        - **Sparse matrices**: $O(s \text{poly}(\log N))$ where $s$ = row sparsity  
        - **Special structure**: Hamiltonians, Toeplitz matrices have efficient encodings
    
        **Fair Comparison with Classical:**  
        
        | **Algorithm** | **Data Load** | **Solver** | **Output** | **Total** |
        |--------------|--------------|------------|------------|-----------|
        | **Classical CG** | $\Theta(N)$ | $O(N\kappa)$ | $\Theta(N)$ | $O(N\kappa)$ |
        | **HHL** | $\Theta(N)$ | $O(\kappa^2 \log N)$ | $\Theta(N)$ | $\Theta(N)$ |
        
        HHL's $O(\log N)$ solver is **asymptotically negligible** compared to $\Theta(N)$ data I/O.
    
        **Output Readout Problem:**  
        HHL produces quantum state $|x\rangle$. Extracting classical solution $\mathbf{x}$ requires:
        - **Full tomography**: $\Theta(N)$ measurements (exponential in qubits)  
        - **Expectation values**: Compute $\langle x | O | x \rangle$—useful only if downstream task is quantum
        
        **Classical output** destroys the advantage.
    
        **Dequantization Results:**  
        Recent work (Ewin Tang, 2018+) shows classical algorithms match HHL's performance via:
        - Low-rank sampling instead of exact solutions  
        - Randomized linear algebra (sketching, random projections)  
        - Result: Classical $O(\text{poly}(\log N))$ **query complexity** for sampling—matching HHL without quantum hardware!
    
        **Practical Implications:**  
        - **For classical ML data** (images, text): HHL **not useful**—state preparation dominates; classical solvers faster  
        - **For quantum-native applications** (chemistry, materials): HHL helps if $|b\rangle$ from quantum simulation, $A$ has efficient encoding, output $|x\rangle$ used in quantum expectations—**only regime with genuine speedup**
    
        **Connection to Quantum Advantage:**  
        The $\Theta(N)$ state preparation bottleneck is a **fundamental barrier** for classical datasets. Quantum advantage in ML requires:
        1. Quantum-to-quantum workflows (no classical I/O)  
        2. Efficient encodings (problem structure provides $O(\text{poly}(\log N))$ state prep)  
        3. Quantum output (downstream tasks use $|x\rangle$ directly)
        
        HHL remains a theoretical benchmark, not a practical tool for classical data. Path to advantage lies in **domain-specific applications** where quantum encoding is natural.
    
### **<i class="fa-solid fa-flask"></i> Hands-On Projects**

#### **Project Blueprint**

| **Section**              | **Description** |
| ------------------------ | --------------- |
| **Objective**            | Analyze qubit requirements and loading complexity for a dataset with $N$ samples and $M$ features. |
| **Mathematical Concept** | $n=\lceil\log_2 N\rceil$; state-prep $\Theta(N)$ for arbitrary states; shot-noise scaling. |
| **Experiment Setup**     | Assume amplitude encoding of $N$ samples; consider measurement of a single observable. |
| **Process Steps**        | Compute $n$; estimate prep time; relate shot budget to target error bar $\epsilon$. |
| **Expected Behavior**    | Large $N$ drives prep cost; reducing $\epsilon$ requires more shots. |
| **Tracking Variables**   | $N$, $n$, $T_{\text{prep}}$, $N_{\text{shots}}$, $\epsilon$. |
| **Verification Goal**    | Quantify feasibility under fixed budgets; identify bottlenecks. |
| **Output**               | Budget table and recommendation narrative. |

---

#### **Python Implementation**

```python
import numpy as np
from scipy.optimize import minimize

# Project 4: Quantum-Inspired QUBO via Classical Simulation

# Minimize f(x) = x0*x1 - x0 - x1 for binary x0,x1 ∈ {0,1}

# Optimal: x0=x1=1 → f = 1-1-1 = -1

def qubo_energy(x, Q):
    """Compute xᵀQx for binary vector x and QUBO matrix Q."""
    return x @ Q @ x

Q = np.array([[0, 1], [1, 0]], dtype=float) / 2 - np.diag([1.0, 1.0])

# Brute-force search (small problem)

best_x, best_e = None, np.inf
for i in range(4):
    x = np.array([(i >> j) & 1 for j in range(2)], dtype=float)
    e = qubo_energy(x, Q)
    print(f"x={x.astype(int).tolist()}  energy={e:.4f}")
    if e < best_e: best_e, best_x = e, x

print(f"\nOptimal: x={best_x.astype(int).tolist()}  energy={best_e:.4f}")
```
**Sample Output:**
```python
x=[0, 0]  energy=0.0000
x=[1, 0]  energy=-1.0000
x=[0, 1]  energy=-1.0000
x=[1, 1]  energy=-1.0000

Optimal: x=[1, 0]  energy=-1.0000
```


#### **Outcome and Interpretation**

You will quantify how data-loading and measurement noise dominate end-to-end runtime, guiding realistic QML designs on NISQ hardware.