# **Chapter 11: Quantum Supervised Learning (Workbook)**

---

> **Summary:** This chapter surveys the core supervised learning algorithms in the Quantum Machine Learning (QML) landscape, where quantum mechanics is leveraged to potentially overcome classical computational barriers. We explore Quantum Support Vector Machines (QSVM) that use quantum kernels to access vast feature spaces, Quantum Neural Networks (QNNs) built on trainable variational circuits, and distance-based classifiers like Quantum k-Nearest Neighbors (QkNN). The chapter examines how these algorithms translate classical learning paradigms into the quantum domain, balancing the promise of quantum advantage with the practical constraints of NISQ-era hardware.

---

The goal of this chapter is to establish concepts in Supervised Quantum Machine Learning, exploring how quantum computing can enhance traditional supervised learning frameworks.

---

## **11.1 Quantum Support Vector Machines & Kernels** {.heading-with-pill}

> **Difficulty:** ★★★☆☆
> 
> **Concept:** Classification via High-Dimensional Feature Spaces
> 
> **Summary:** The Quantum Support Vector Machine (QSVM) leverages quantum feature maps to project classical data into an exponentially large Hilbert space. In this space, a quantum kernel measures data similarity, enabling the construction of powerful non-linear classifiers that would be intractable to compute classically.

---

### **Theoretical Background**

Quantum Support Vector Machines (QSVM) extend classical kernel methods by leveraging quantum feature maps to access exponentially large Hilbert spaces, enabling the computation of kernels that are classically intractable.

**Classical SVM Foundation:**

Given training data $\{(\mathbf{x}_i, y_i)\}_{i=1}^N$ where $\mathbf{x}_i \in \mathbb{R}^d$ and $y_i \in \{-1, +1\}$, the classical SVM seeks a hyperplane $\mathbf{w} \cdot \mathbf{x} + b = 0$ maximizing the margin between classes.

**Dual Formulation:**  
The optimization problem in dual form:

$$
\max_{\vec{\alpha}} \sum_{i=1}^N \alpha_i - \frac{1}{2}\sum_{i,j=1}^N \alpha_i \alpha_j y_i y_j K(\mathbf{x}_i, \mathbf{x}_j)
$$

subject to:

$$
0 \leq \alpha_i \leq C, \quad \sum_{i=1}^N \alpha_i y_i = 0
$$

where $C$ is regularization parameter.

**Decision Function:**
$$
f(\mathbf{x}) = \text{sign}\left(\sum_{i=1}^N \alpha_i y_i K(\mathbf{x}_i, \mathbf{x}) + b\right)
$$

**Kernel Trick:**  
For feature map $\phi: \mathbb{R}^d \to \mathcal{F}$, the kernel function:

$$
K(\mathbf{x}, \mathbf{x}') = \langle \phi(\mathbf{x}), \phi(\mathbf{x}')\rangle_{\mathcal{F}}
$$

enables working in high-dimensional feature space $\mathcal{F}$ without explicit computation of $\phi(\mathbf{x})$.

**Classical Kernels:**
- **Linear:** $K(\mathbf{x}, \mathbf{x}') = \mathbf{x} \cdot \mathbf{x}'$  
- **Polynomial:** $K(\mathbf{x}, \mathbf{x}') = (\mathbf{x} \cdot \mathbf{x}' + c)^p$  
- **RBF (Gaussian):** $K(\mathbf{x}, \mathbf{x}') = \exp(-\gamma\|\mathbf{x} - \mathbf{x}'\|^2)$

**Quantum Feature Maps:**

Map classical data to quantum states via parameterized circuit:

$$
\phi(\mathbf{x}) = |\psi(\mathbf{x})\rangle = U_{\Phi}(\mathbf{x})|0\rangle^{\otimes n}
$$

where $U_{\Phi}(\mathbf{x})$ encodes features into quantum state.

**Common Encoding Schemes:**

**1. Angle Encoding:**
$$
U_{\Phi}(\mathbf{x}) = \bigotimes_{i=1}^{\min(d,n)} R_y(x_i)
$$

Creates separable state:
$$
|\psi(\mathbf{x})\rangle = \bigotimes_{i=1}^n \left(\cos(x_i/2)|0\rangle + \sin(x_i/2)|1\rangle\right)
$$

**2. IQP-Inspired Encoding:**  
Apply Hadamards followed by diagonal unitaries:

$$
U_{\Phi}(\mathbf{x}) = U_Z(\mathbf{x}) \mathbf{H}^{\otimes n}
$$

where:

$$
U_Z(\mathbf{x}) = \exp\left(-i \sum_{S \subseteq [n]} \phi_S(\mathbf{x}) \prod_{j \in S} Z_j\right)
$$

with $\phi_S(\mathbf{x}) = \sum_{k \in S} x_k$ or polynomial features.

**Quantum Kernel Definition:**

The quantum kernel measures state overlap:

$$
K_Q(\mathbf{x}, \mathbf{x}') = |\langle\psi(\mathbf{x})|\psi(\mathbf{x}')\rangle|^2
$$

This is the **fidelity** between quantum states, satisfying:
- $0 \leq K_Q(\mathbf{x}, \mathbf{x}') \leq 1$  
- $K_Q(\mathbf{x}, \mathbf{x}) = 1$ (self-similarity)  
- Symmetry: $K_Q(\mathbf{x}, \mathbf{x}') = K_Q(\mathbf{x}', \mathbf{x})$

**Explicit Form for IQP Encoding:**

With single layer ($L=1$):

$$
K_Q(\mathbf{x}, \mathbf{x}') = \left|\frac{1}{2^n}\sum_{z \in \{0,1\}^n} e^{i[\phi(\mathbf{x},z) - \phi(\mathbf{x}',z)]}\right|^2
$$

where $\phi(\mathbf{x},z) = \sum_S \phi_S(\mathbf{x}) \prod_{j \in S} z_j$.

**Kernel Estimation via SWAP Test:**

To measure $|\langle\psi|\phi\rangle|^2$ for states $|\psi\rangle$, $|\phi\rangle$:

**Circuit:**
1. Ancilla qubit initialized to $|0\rangle$  
2. Apply Hadamard to ancilla: $\frac{1}{\sqrt{2}}(|0\rangle + |1\rangle)$  
3. Controlled-SWAP between registers conditioned on ancilla  
4. Apply Hadamard to ancilla  
5. Measure ancilla

**Probability of outcome $|0\rangle$:**

$$
P(0) = \frac{1 + |\langle\psi|\phi\rangle|^2}{2}
$$

Solving for kernel:

$$
K_Q = 2P(0) - 1
$$

With $N$ shots, estimate $\hat{P}(0) = n_0/N$ with variance $\mathcal{O}(1/N)$.

**Computational Hardness Conjecture:**

Havlíček et al. (2019) showed that for IQP circuits, computing $K_Q(\mathbf{x}, \mathbf{x}')$ is $\#P$-hard under plausible complexity assumptions (polynomial hierarchy non-collapse). This suggests classical intractability.

**QSVM Training Algorithm:**

**Step 1: Kernel Matrix Computation**  
For training set $\{(\mathbf{x}_i, y_i)\}_{i=1}^N$, compute $N \times N$ kernel matrix:

$$
\mathbf{K}_{ij} = K_Q(\mathbf{x}_i, \mathbf{x}_j)
$$

This requires $\binom{N}{2} + N = N(N+1)/2$ kernel evaluations (using symmetry).

**Step 2: Classical SVM Optimization**  
Solve dual problem using classical solver (SMO, LIBSVM) with quantum kernel matrix $\mathbf{K}$.

**Step 3: Prediction**  
For new point $\mathbf{x}_{\text{new}}$:

1. Compute $N$ kernels: $K_Q(\mathbf{x}_i, \mathbf{x}_{\text{new}})$ for $i=1,\ldots,N$  
2. Evaluate decision function:

$$
f(\mathbf{x}_{\text{new}}) = \text{sign}\left(\sum_{i=1}^N \alpha_i y_i K_Q(\mathbf{x}_i, \mathbf{x}_{\text{new}}) + b\right)
$$

**Complexity Analysis:**

**Kernel Evaluation:**
- Circuit depth: $\mathcal{O}(\text{poly}(n, d))$ for encoding + feature map  
- SWAP test: $\mathcal{O}(1)$ depth overhead  
- Shots for precision $\epsilon$: $\mathcal{O}(1/\epsilon^2)$

**Training Kernel Matrix:**
- Quantum evaluations: $\mathcal{O}(N^2)$  
- Total shots: $\mathcal{O}(N^2/\epsilon^2)$  
- Classical SVM solver: $\mathcal{O}(N^2)$ to $\mathcal{O}(N^3)$ depending on method

**Prediction:**
- Quantum evaluations: $\mathcal{O}(N)$ per new sample  
- Total prediction cost: $\mathcal{O}(N/\epsilon^2)$

**Quantum Advantage Conditions:**

1. **Kernel Hardness:** $K_Q$ must be classically hard to approximate  
2. **Sample Efficiency:** Quantum model generalizes better than classical with same $N$  
3. **End-to-End Speedup:** Quantum kernel evaluation + classical training faster than classical methods

Current evidence suggests advantage in specialized problems (e.g., certain geometric datasets, quantum data classification).

---

### **Comprehension Check**

!!! note "Quiz"
    
        1.  The primary function of a Quantum Kernel $K(\mathbf{x}, \mathbf{x}')$ is to:
        - A. Calculate the gradient of the loss function.
        - B. Measure the overlap (similarity) between two amplitude-encoded quantum states.
        - C. Define the parameterized unitary $U(\vec{\theta})$.
    
??? info "See Answer"
        **Correct: B**. The kernel quantifies the similarity of data points in the quantum feature space.
    
!!! abstract "Interview-Style Question"
    
    The QSVM decision function, $\sum_i \alpha_i y_i K(\mathbf{x}_i, \mathbf{x}) + b$, is trained classically. If the training is classical, where does the potential for quantum advantage come from?
    
    ???+ info "Answer Strategy"
        The potential for quantum advantage in a QSVM does not come from the training process itself, but from the **computation of the kernel matrix**.
    
        1.  **Classically Intractable Kernels:** A quantum computer can potentially compute kernels that are intractable for classical computers. The quantum feature map projects the classical data into a Hilbert space that is exponentially large. Calculating the inner products between all pairs of data points in this vast space is often impossible for a classical machine.
        2.  **Superior Expressive Power:** By accessing these complex, high-dimensional feature spaces, a QSVM may be able to find non-linear decision boundaries that are invisible to classical kernel methods. This could lead to higher accuracy on certain complex datasets.
    
        In essence, the quantum computer provides a more powerful "lens" through which to view the data's similarity, even though the final step of drawing the separating line is done classically.
    
---

### **<i class="fa-solid fa-flask"></i> Hands-On Projects**

#### **Project Blueprint: Kernel Estimation via Overlap**

| Component | Description |
| :--- | :--- |
| **Objective** | Analytically calculate the value of a Quantum Kernel for two simple, predefined quantum states. |
| **Mathematical Concept** | The kernel is the squared inner product of the feature-mapped states: $K(\mathbf{x}, \mathbf{x}') = \|\langle \phi(\mathbf{x}) | \phi(\mathbf{x}') \rangle\|^2$. |
| **Experiment Setup** | State 1: $\|\phi(\mathbf{x})\rangle = \|+\rangle = \frac{1}{\sqrt{2}}(\|0\rangle + \|1\rangle)$. <br> State 2: $\|\phi(\mathbf{x}')\rangle = \|0\rangle$. |
| **Process Steps** | 1. Calculate the inner product (overlap): $\langle \phi(\mathbf{x}) | \phi(\mathbf{x}') \rangle$. <br> 2. Calculate the final kernel value by taking the squared magnitude of the inner product. |
| **Expected Behavior** | The kernel value will be a real number between 0 and 1, quantifying the similarity between the two states. |
| **Verification Goal** | Obtain the exact numerical value for $K(\mathbf{x}, \mathbf{x}')$. |

---

#### **Python Implementation**

```python
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector
import numpy as np

# Project 1: Quantum Kernel Estimation via State Overlap

def angle_encoding(x, n=2):
    """Encode 2 features via Rx rotations."""
    qc = QuantumCircuit(n)
    for i, xi in enumerate(x[:n]):
        qc.rx(xi, i)
    return qc

def qkernel(x1, x2):
    """K(x1,x2) = |<φ(x1)|φ(x2)>|^2"""
    sv1 = Statevector(angle_encoding(x1))
    sv2 = Statevector(angle_encoding(x2))
    return abs(sv1.inner(sv2))**2

# Example: classify XOR-like dataset with quantum kernel

X_train = [[0.1, 0.1], [2.0, 2.0], [0.1, 2.0], [2.0, 0.1]]
y_train  = [+1, +1, -1, -1]  # XOR pattern

print("Quantum kernel matrix K[i,j] = |<phi_i|phi_j>|^2:")
K = [[qkernel(X_train[i], X_train[j]) for j in range(4)] for i in range(4)]
for row in K: print([f"{v:.3f}" for v in row])
```
**Sample Output:**
```python
Quantum kernel matrix K[i,j] = |<phi_i|phi_j>|^2:
['1.000', '0.114', '0.338', '0.338']
['0.114', '1.000', '0.338', '0.338']
['0.338', '0.338', '1.000', '0.114']
['0.338', '0.338', '0.114', '1.000']
```


#### **Outcome and Interpretation**

The inner product is $\langle + | 0 \rangle = \frac{1}{\sqrt{2}}$. The kernel value is $K = (\frac{1}{\sqrt{2}})^2 = 0.5$. This result provides a concrete measure of similarity; the state $|+\rangle$ has a 50% overlap with the state $|0\rangle$ in this feature space.

---

---

## **11.2 Quantum k-Nearest Neighbors (QkNN)** {.heading-with-pill}

> **Difficulty:** ★★☆☆☆
> 
> **Concept:** Classification by Quantum Distance
> 
> **Summary:** The Quantum k-Nearest Neighbors (QkNN) algorithm classifies data by finding the 'k' closest training examples in a quantum feature space. Distance is measured using the fidelity between quantum states, which can be estimated efficiently with quantum circuits, allowing the classical k-NN voting mechanism to be applied to quantum data.

---

### **Theoretical Background**

Quantum k-Nearest Neighbors (QkNN) adapts the classical instance-based learning paradigm by defining distance metrics in quantum Hilbert space, enabling classification via state fidelity measurements.

**Classical k-NN Algorithm:**

Given training set $\mathcal{D} = \{(\mathbf{x}_i, y_i)\}_{i=1}^N$ and test point $\mathbf{x}_{\text{test}}$:

1. Compute distances: $d_i = \|\mathbf{x}_{\text{test}} - \mathbf{x}_i\|$ for all $i$  
2. Find $k$ smallest distances: indices $\mathcal{N}_k$  
3. Predict via majority vote:

$$
\hat{y} = \text{mode}\{y_i : i \in \mathcal{N}_k\}
$$

**Quantum State Encoding:**

Map classical data to quantum states:

$$
\mathbf{x} \xrightarrow{\text{encode}} |\psi(\mathbf{x})\rangle = U_{\text{enc}}(\mathbf{x})|0\rangle^{\otimes n}
$$

**Amplitude Encoding:**  
For $d = 2^n$ features, normalize and encode:

$$
|\psi(\mathbf{x})\rangle = \frac{1}{\|\mathbf{x}\|}\sum_{i=0}^{d-1} x_i |i\rangle
$$

Requires $\mathcal{O}(d)$ gates for arbitrary vectors.

**Angle Encoding:**  
Use rotation angles:

$$
|\psi(\mathbf{x})\rangle = \bigotimes_{j=1}^n R_y(x_j)|0\rangle
$$

Creates separable state in $\mathcal{O}(n)$ depth.

**Quantum Distance Metrics:**

Define distance based on state fidelity:

**Fidelity:**
$$
F(\mathbf{x}, \mathbf{x}') = |\langle\psi(\mathbf{x})|\psi(\mathbf{x}')\rangle|^2
$$

Properties:
- $0 \leq F \leq 1$  
- $F = 1$ for identical states  
- $F = 0$ for orthogonal states

**Trace Distance:**
$$
D_T(\rho, \sigma) = \frac{1}{2}\text{Tr}|\rho - \sigma|
$$

For pure states $\rho = |\psi\rangle\langle\psi|$, $\sigma = |\phi\rangle\langle\phi|$:

$$
D_T = \sqrt{1 - |\langle\psi|\phi\rangle|^2}
$$

**Bures Distance:**
$$
D_B(\rho, \sigma) = \sqrt{2(1 - \sqrt{F(\rho,\sigma)})}
$$

For pure states:

$$
D_B = \sqrt{2(1 - |\langle\psi|\phi\rangle|)}
$$

**Standard QkNN Distance:**  
Most implementations use:

$$
d_Q(\mathbf{x}, \mathbf{x}') = \sqrt{1 - F(\mathbf{x}, \mathbf{x}')} = \sqrt{1 - |\langle\psi(\mathbf{x})|\psi(\mathbf{x}')\rangle|^2}
$$

This equals trace distance for pure states.

**Relationship to Classical Euclidean Distance:**

For angle-encoded states with small features $x_j, x_j' \ll 1$:

$$
|\psi(\mathbf{x})\rangle \approx |0\rangle^{\otimes n} + \sum_j x_j |0\cdots 1_j \cdots 0\rangle
$$

Inner product:

$$
\langle\psi(\mathbf{x})|\psi(\mathbf{x}')\rangle \approx 1 + \sum_j x_j x_j' - \frac{1}{2}\sum_j (x_j^2 + x_j'^2)
$$

For normalized states:

$$
d_Q^2 \approx \frac{1}{2}\sum_j (x_j - x_j')^2 = \frac{1}{2}\|\mathbf{x} - \mathbf{x}'\|^2
$$

So quantum distance reduces to Euclidean for small-angle encoding.

**Fidelity Estimation via SWAP Test:**

**Circuit Setup:**
1. Prepare $|\psi(\mathbf{x})\rangle$ in register A  
2. Prepare $|\psi(\mathbf{x}')\rangle$ in register B  
3. Ancilla $|0\rangle$, apply Hadamard: $\frac{1}{\sqrt{2}}(|0\rangle + |1\rangle)$  
4. Controlled-SWAP($A \leftrightarrow B$) on ancilla  
5. Hadamard on ancilla, measure

**Measurement Statistics:**

$$
P(\text{ancilla} = 0) = \frac{1 + |\langle\psi(\mathbf{x})|\psi(\mathbf{x}')\rangle|^2}{2}
$$

$$
P(\text{ancilla} = 1) = \frac{1 - |\langle\psi(\mathbf{x})|\psi(\mathbf{x}')\rangle|^2}{2}
$$

Fidelity estimate:

$$
\hat{F} = 2\hat{P}(0) - 1
$$

With $N$ shots: $\text{Var}[\hat{F}] = \mathcal{O}(1/N)$.

**Alternative: Destructive Interference Test:**

Prepare $\frac{1}{\sqrt{2}}(|\psi(\mathbf{x})\rangle + |\psi(\mathbf{x}')\rangle)$ and measure in computational basis. Overlap encoded in measurement probabilities.

**QkNN Algorithm:**

**Input:** Training set $\{(\mathbf{x}_i, y_i)\}_{i=1}^N$, test point $\mathbf{x}_{\text{test}}$, parameter $k$

**Step 1: State Preparation**  
For each $i = 1, \ldots, N$:
- Encode $|\psi_i\rangle = |\psi(\mathbf{x}_i)\rangle$  
- Encode $|\psi_{\text{test}}\rangle = |\psi(\mathbf{x}_{\text{test}})\rangle$

**Step 2: Distance Computation (Quantum)**  
For each $i$:
- Execute SWAP test between $|\psi_{\text{test}}\rangle$ and $|\psi_i\rangle$  
- Estimate fidelity $\hat{F}_i$ from $M$ shots  
- Compute distance: $d_i = \sqrt{1 - \hat{F}_i}$

Total quantum evaluations: $N \times M$ shots

**Step 3: Classical k-NN Selection**  
Sort distances: $d_{(1)} \leq d_{(2)} \leq \cdots \leq d_{(N)}$  
Identify indices of $k$ smallest: $\mathcal{N}_k = \{i_1, \ldots, i_k\}$

**Step 4: Majority Vote**

$$
\hat{y} = \arg\max_{c} \sum_{i \in \mathcal{N}_k} \mathbb{1}[y_i = c]
$$

**Complexity Analysis:**

**Per-Sample Prediction:**
- Quantum circuits: $N$ (one per training point)  
- Shots per circuit: $M = \mathcal{O}(1/\epsilon^2)$ for precision $\epsilon$  
- Total quantum cost: $\mathcal{O}(N/\epsilon^2)$  
- Classical sorting: $\mathcal{O}(N \log N)$  
- Classical voting: $\mathcal{O}(k)$

**Quantum Advantage Analysis:**

**Classical k-NN:**  
- Distance computation: $\mathcal{O}(Nd)$ for $d$-dimensional data  
- Sorting: $\mathcal{O}(N \log N)$  
- Total: $\mathcal{O}(Nd + N\log N)$

**Quantum k-NN:**  
- State encoding: $\mathcal{O}(\text{poly}(\log d))$ if efficient encoding exists  
- Distance estimation: $\mathcal{O}(N/\epsilon^2)$ shots  
- Sorting: $\mathcal{O}(N \log N)$  
- Total: $\mathcal{O}(N/\epsilon^2 + N\log N)$

**Speedup Conditions:**

Quantum advantage requires:
1. Efficient state preparation: $\text{poly}(\log d) \ll d$  
2. Shot budget $M \ll d$  
3. Quantum distance metric captures problem structure better than Euclidean

**Practical Limitations:**

1. **Data Encoding Bottleneck:** Preparing $|\psi(\mathbf{x})\rangle$ for arbitrary classical data requires $\Theta(d)$ operations, negating advantage  
2. **Online Cost:** Unlike QSVM (offline kernel computation), QkNN requires quantum computation per prediction  
3. **Shot Noise:** Large $M$ needed for accurate distance estimates

**Potential Applications:**
- **Quantum Data Classification:** When data is inherently quantum (e.g., from quantum sensors)  
- **Structured Data:** When efficient quantum encoding exists (e.g., sparse vectors, time series via QFT)  
- **Hybrid Models:** Use QkNN for small critical subset, classical k-NN for bulk

---

### **Comprehension Check**

!!! note "Quiz"
    
        1.  How is the distance between two data points primarily defined in the QkNN algorithm?
        - A. The $\ell_2$ norm of the classical feature vectors.
        - B. A function of the fidelity (overlap) between their quantum state vectors.
        - C. The Euclidean distance in the Bloch sphere.
    
??? info "See Answer"
        **Correct: B**. The distance is derived from the quantum state overlap, which measures similarity in the Hilbert space.
    
!!! abstract "Interview-Style Question"
    
    What is the key difference in the computational task performed by the quantum computer in QSVM versus QkNN?
    
    ???+ info "Answer Strategy"
        The key difference lies in the **scope and timing** of the quantum computation.
    
        1.  **QSVM (Batch Processing):**
            *   **Task:** The quantum computer's job is to compute the **entire $N \times N$ kernel matrix** for the training data, where $N$ is the number of training samples.
            *   **Timing:** This is a large, one-time, offline computation. Once the kernel is computed, the quantum computer is no longer needed for training or inference.
    
        2.  **QkNN (Real-time Inference):**
            *   **Task:** To classify a *new*, unseen data point, the quantum computer must compute the **$N$ distances** between that new point and every point in the training set.
            *   **Timing:** This is a smaller, online computation that must be performed for every single prediction.
    
        In short, QSVM uses the quantum computer for a heavy, upfront batch job on the training set, while QkNN uses it for a lighter, repeated job during inference.
    
---

### **<i class="fa-solid fa-flask"></i> Hands-On Projects**

#### **Project Blueprint: QkNN Distance Calculation**

| Component | Description |
| :--- | :--- |
| **Objective** | Analytically calculate the quantum distance between two given quantum states. |
| **Mathematical Concept** | The fidelity-based distance metric: $\text{Distance} = \sqrt{1 - \|\langle \psi(\mathbf{x}) | \psi(\mathbf{y}) \rangle\|^2}$. |
| **Experiment Setup** | State 1: $\|\psi(\mathbf{x})\rangle = \frac{3}{5}\|0\rangle + \frac{4}{5}\|1\rangle$. <br> State 2: $\|\psi(\mathbf{y})\rangle = \frac{4}{5}\|0\rangle - \frac{3}{5}\|1\rangle$. |
| **Process Steps** | 1. Calculate the inner product (overlap): $\langle \psi(\mathbf{x}) | \psi(\mathbf{y}) \rangle$. <br> 2. Calculate the squared magnitude of the overlap. <br> 3. Compute the final distance using the formula. |
| **Expected Behavior** | The overlap will be zero, indicating the states are orthogonal, and the distance will be maximal (1). |
| **Verification Goal** | Obtain the exact numerical value for the quantum distance. |

---

#### **Python Implementation**

```python
import numpy as np

# Project 2: Quantum k-NN Distance Calculation

def angle_feature_map_state(x):
    """Returns statevector of angle-encoded x (2D)."""
    a, b = x
    # |ψ(x)> = cos(a/2)cos(b/2)|00> + cos(a/2)sin(b/2)|01> + ...
    psi = np.array([
        np.cos(a/2)*np.cos(b/2),
        np.cos(a/2)*np.sin(b/2),
        np.sin(a/2)*np.cos(b/2),
        np.sin(a/2)*np.sin(b/2),
    ], dtype=complex)
    return psi / np.linalg.norm(psi)

def quantum_distance(x1, x2):
    """Fidelity-based distance: 1 - |<ψ(x1)|ψ(x2)>|^2"""
    psi1 = angle_feature_map_state(x1)
    psi2 = angle_feature_map_state(x2)
    return 1 - abs(np.dot(psi1.conj(), psi2))**2

# kNN classification for a test point

X_train = [[0.2, 0.3], [1.5, 1.6], [0.1, 0.4], [1.4, 1.5]]
y_train  = [0, 1, 0, 1]
x_test   = [0.3, 0.25]

dists = [quantum_distance(x_test, xi) for xi in X_train]
k = 3
knn_labels = [y_train[i] for i in np.argsort(dists)[:k]]
prediction = max(set(knn_labels), key=knn_labels.count)
print(f"Quantum distances: {[f'{d:.4f}' for d in dists]}")
print(f"Predicted class (k={k}): {prediction}")
```
**Sample Output:**
```python
Quantum distances: ['0.0031', '0.5848', '0.0155', '0.5220']
Predicted class (k=3): 0
```


#### **Outcome and Interpretation**

The inner product is 0, which means the states $|\psi(\mathbf{x})\rangle$ and $|\psi(\mathbf{y})\rangle$ are orthogonal. The quantum distance is $\sqrt{1 - 0^2} = 1$. This represents the maximum possible distance between two states in the feature space, indicating they are completely dissimilar.

---

---

## **11.3 Quantum Neural Networks (QNNs)** {.heading-with-pill}

> **Difficulty:** ★★★★☆
> 
> **Concept:** Trainable Quantum Circuits for Machine Learning
> 
> **Summary:** Quantum Neural Networks (QNNs) are hybrid models where a parameterized quantum circuit (PQC) acts as a trainable function approximator. Data is encoded into a quantum state, processed by layers of parameterized gates, and measured to produce a classical output. A classical optimizer then tunes the gate parameters to minimize a cost function, but training faces challenges like barren plateaus.

---

### **Theoretical Background**

Quantum Neural Networks (QNNs), also called Variational Quantum Circuits (VQCs) for supervised learning, are parameterized quantum circuits trained via hybrid quantum-classical optimization to approximate complex functions.

**QNN Architecture:**

A QNN consists of three sequential components:

**1. Feature Map (Data Encoding):**  
Classical input $\mathbf{x} \in \mathbb{R}^d$ encoded into quantum state:

$$
|\phi(\mathbf{x})\rangle = U_{\Phi}(\mathbf{x})|0\rangle^{\otimes n}
$$

Common encodings:

**Angle Encoding:**
$$
U_{\Phi}(\mathbf{x}) = \prod_{i=1}^{\min(d,n)} R_y(x_i) R_z(x_i)
$$

**Amplitude Encoding:**  
For $d = 2^n$:
$$
|\phi(\mathbf{x})\rangle = \frac{1}{\|\mathbf{x}\|}\sum_{i=0}^{d-1} x_i |i\rangle
$$

**Higher-Order Feature Maps:**
$$
U_{\Phi}(\mathbf{x}) = \prod_{k=1}^L U_Z^{(k)}(\mathbf{x}) \mathbf{H}^{\otimes n}
$$

where $U_Z^{(k)}$ encodes feature interactions.

**2. Variational Ansatz (Trainable Layers):**  
Parameterized unitary $U(\vec{\theta})$ with $m$ trainable parameters:

$$
U(\vec{\theta}) = \prod_{\ell=1}^L W_{\text{ent}}^{(\ell)} \cdot R(\vec{\theta}_{\ell})
$$

where:
- $R(\vec{\theta}_{\ell}) = \bigotimes_{i=1}^n R_y(\theta_{\ell,i}) R_z(\theta_{\ell,i+n})$ are rotation layers  
- $W_{\text{ent}}^{(\ell)}$ are entangling gates (CNOT, CZ)

**Total State:**
$$
|\psi(\mathbf{x};\vec{\theta})\rangle = U(\vec{\theta}) \cdot U_{\Phi}(\mathbf{x}) \cdot |0\rangle^{\otimes n}
$$

**3. Measurement and Output:**  
Measure observable $\hat{M}$ (Hermitian operator):

$$
f(\mathbf{x};\vec{\theta}) = \langle\psi(\mathbf{x};\vec{\theta})|\hat{M}|\psi(\mathbf{x};\vec{\theta})\rangle
$$

**Common Observables:**

**Single-Qubit:**
$$
\hat{M} = \mathbf{Z}_0 = \begin{pmatrix} 1 & 0 \\ 0 & -1 \end{pmatrix} \otimes \mathbf{I}^{\otimes (n-1)}
$$

Expectation value range: $[-1, +1]$

**Multi-Qubit:**
$$
\hat{M} = \sum_{i=0}^{n-1} w_i \mathbf{Z}_i, \quad w_i \in \mathbb{R}
$$

**Pauli String:**
$$
\hat{M} = \sum_j c_j \mathbf{P}_j, \quad \mathbf{P}_j \in \{\mathbf{X}, \mathbf{Y}, \mathbf{Z}\}^{\otimes n}
$$

**Loss Functions for Supervised Learning:**

**Binary Classification:**

**Mean Squared Error:**
$$
\mathcal{L}_{\text{MSE}}(\vec{\theta}) = \frac{1}{N}\sum_{i=1}^N \left(y_i - f(\mathbf{x}_i;\vec{\theta})\right)^2
$$

where $y_i \in \{-1, +1\}$ or $\{0, 1\}$.

**Hinge Loss:**
$$
\mathcal{L}_{\text{hinge}}(\vec{\theta}) = \frac{1}{N}\sum_{i=1}^N \max\left(0, 1 - y_i f(\mathbf{x}_i;\vec{\theta})\right)
$$

**Cross-Entropy (with sigmoid):**
$$
\sigma(x) = \frac{1}{1 + e^{-x}}, \quad \mathcal{L}_{\text{CE}}(\vec{\theta}) = -\frac{1}{N}\sum_{i=1}^N \left[y_i \log\sigma(f_i) + (1-y_i)\log(1-\sigma(f_i))\right]
$$

where $f_i = f(\mathbf{x}_i;\vec{\theta})$.

**Multi-Class Classification:**

Measure $C$ observables $\{\hat{M}_c\}_{c=1}^C$:

$$
f_c(\mathbf{x};\vec{\theta}) = \langle\psi(\mathbf{x};\vec{\theta})|\hat{M}_c|\psi(\mathbf{x};\vec{\theta})\rangle
$$

Apply softmax:

$$
p_c(\mathbf{x};\vec{\theta}) = \frac{e^{f_c(\mathbf{x};\vec{\theta})}}{\sum_{c'=1}^C e^{f_{c'}(\mathbf{x};\vec{\theta})}}
$$

Cross-entropy loss:

$$
\mathcal{L}(\vec{\theta}) = -\frac{1}{N}\sum_{i=1}^N \sum_{c=1}^C \mathbb{1}[y_i = c] \log p_c(\mathbf{x}_i;\vec{\theta})
$$

**Regression:**
$$
\mathcal{L}_{\text{reg}}(\vec{\theta}) = \frac{1}{N}\sum_{i=1}^N \left(y_i - f(\mathbf{x}_i;\vec{\theta})\right)^2, \quad y_i \in \mathbb{R}
$$

**Training via Gradient Descent:**

**Update Rule:**
$$
\vec{\theta}_{t+1} = \vec{\theta}_t - \eta \nabla_{\vec{\theta}} \mathcal{L}(\vec{\theta}_t)
$$

where $\eta > 0$ is learning rate.

**Parameter-Shift Gradient:**  
For gate $U_j(\theta_j) = e^{-i\theta_j G_j}$ with $G_j^2 = \mathbf{I}$:

$$
\frac{\partial f}{\partial \theta_j} = \frac{1}{2}\left[f(\vec{\theta}^+_j) - f(\vec{\theta}^-_j)\right]
$$

where $\vec{\theta}^\pm_j = \vec{\theta} \pm \frac{\pi}{2}\hat{e}_j$.

**Gradient of Loss:**
$$
\frac{\partial \mathcal{L}}{\partial \theta_j} = \frac{1}{N}\sum_{i=1}^N \frac{\partial \mathcal{L}}{\partial f_i} \cdot \frac{\partial f_i}{\partial \theta_j}
$$

For MSE:
$$
\frac{\partial \mathcal{L}_{\text{MSE}}}{\partial f_i} = -2(y_i - f_i)
$$

**Computational Cost per Gradient:**
- Circuit evaluations: $2m$ (parameter-shift)  
- Training samples: $N$  
- Total circuits per iteration: $2mN$  
- Shots per circuit: $M = \mathcal{O}(1/\epsilon^2)$  
- Total measurements: $2mNM$

**Barren Plateaus:**

For random deep circuits forming approximate 2-designs:

$$
\text{Var}\left[\frac{\partial \mathcal{L}}{\partial \theta_j}\right] \in \mathcal{O}\left(\frac{1}{2^n}\right)
$$

Gradient variance vanishes exponentially with qubit count $n$.

**McClean et al. Theorem:**  
For local observable $\hat{M}$ acting on $k$ qubits and random circuit:

$$
\mathbb{E}\left[\left|\frac{\partial \langle\hat{M}\rangle}{\partial \theta_j}\right|^2\right] \leq \frac{C}{2^n}
$$

where $C = \mathcal{O}(1)$ depends on observable locality.

**Mitigation Strategies:**

1. **Shallow Circuits:** Restrict depth $L \leq c\log n$  
2. **Local Cost Functions:** Use $\mathcal{L} = \sum_i w_i \langle\hat{M}_i\rangle$ with local $\hat{M}_i$  
3. **Layerwise Training:** Train one layer at a time  
4. **Problem-Inspired Ansätze:** Use structure (e.g., UCC for chemistry)  
5. **Identity Initialization:** Start with $\vec{\theta} \approx 0$ so $U(\vec{\theta}) \approx \mathbf{I}$

**Expressivity vs. Trainability:**

**Expressivity Measure:**  
How well ansatz approximates target functions. For $L$ layers:

$$
\epsilon_{\text{approx}} \sim \mathcal{O}\left(\frac{1}{\text{poly}(L)}\right)
$$

**Trainability:** Gradient magnitude:

$$
|\nabla_{\vec{\theta}} \mathcal{L}| \sim \mathcal{O}(1) \quad \text{(trainable)}
$$
$$
|\nabla_{\vec{\theta}} \mathcal{L}| \sim \mathcal{O}(2^{-n}) \quad \text{(barren plateau)}
$$

**Optimal Design:**  
Use minimal depth $L^*$ achieving target accuracy while maintaining $|\nabla \mathcal{L}| > \delta$ for threshold $\delta$.

**Universal Approximation:**  
Pérez-Salinas et al. proved QNNs with polynomial depth and periodic data re-uploading are universal approximators for continuous functions on compact domains.

**QNN vs. Classical NN:**

| Property | Classical NN | Quantum NN |
|----------|--------------|------------|
| State space | $\mathbb{R}^h$ (hidden dim) | $\mathbb{C}^{2^n}$ (Hilbert) |
| Parameters | $\mathcal{O}(h^2)$ weights | $\mathcal{O}(nL)$ angles |
| Activation | Nonlinear (ReLU, sigmoid) | Unitary evolution |
| Training | Backprop, $\mathcal{O}(h)$ per sample | Parameter-shift, $\mathcal{O}(m/\epsilon^2)$ |
| Advantage | Mature, scalable | High-dim Hilbert space, entanglement |

---

### **Comprehension Check**

!!! note "Quiz"
    
        1.  Which challenge, also faced by VQE, poses a significant risk to the effective training of deep QNNs?
        - A. The data loading bottleneck.
        - B. Risk of barren plateaus.
        - C. The No-cloning theorem.
    
??? info "See Answer"
        **Correct: B**. Barren plateaus cause gradients to vanish, stalling the optimization process.
    
!!! abstract "Interview-Style Question"
    
    What is the primary motivation for using a Quantum Neural Network (QNN) over a classical neural network?
    
    ???+ info "Answer Strategy"
        The primary motivation for using a Quantum Neural Network (QNN) is to leverage the **vast and complex Hilbert space** to create more powerful and expressive models than classical neural networks can achieve.
    
        1.  **Larger State Space:** A classical bit has 2 states, while a qubit exists in a superposition of 2 states. An $n$-qubit system has a state space of $2^n$ complex dimensions, which grows exponentially. This allows QNNs to represent and process information in ways that are classically intractable.
        2.  **Entanglement for Complex Correlations:** Entanglement allows a QNN to capture intricate, non-local correlations between features in the data that classical networks might miss or require many more parameters to learn.
        3.  **Potential for Better Generalization:** By exploring a much larger function space, QNNs may be able to find solutions that generalize better to new data, especially for problems with inherent quantum-like structures.
    
        In essence, the goal is to use the unique properties of quantum mechanics to perform computations and learn patterns that are beyond the reach of classical models.
    
---

### **<i class="fa-solid fa-flask"></i> Hands-On Projects**

#### **Project Blueprint: Conceptual QNN Prediction**

| Component | Description |
| :--- | :--- |
| **Objective** | Calculate the predicted classification output of a simple, single-qubit QNN. |
| **Mathematical Concept** | The prediction is the expectation value of an observable: $f(\mathbf{x}, \vec{\theta}) = \langle \psi | \hat{M} | \psi \rangle$. |
| **Experiment Setup** | Final State (after encoding and parameterized layers): $\|\psi\rangle = \frac{i}{\sqrt{5}}\|0\rangle + \frac{2}{\sqrt{5}}\|1\rangle$. <br> Measurement Observable (Output "Neuron"): $\hat{M} = Z$ (Pauli-Z operator). |
| **Process Steps** | 1. Write the final state $\|\psi\rangle$ as a column vector. <br> 2. Write the observable $\hat{M}=Z$ as a matrix. <br> 3. Calculate the expectation value $\langle \psi | Z | \psi \rangle$. <br> 4. Apply a classical decision rule to the expectation value to get a final label. |
| **Expected Behavior** | The expectation value will be a real number between -1 and 1, which is then mapped to a discrete class label. |
| **Verification Goal** | Determine the final predicted label based on the expectation value and a given threshold. |

---

#### **Python Implementation**

```python
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector, SparsePauliOp
from scipy.optimize import minimize
import numpy as np

# Project 3: Conceptual Quantum Neural Network (QNN) Prediction

def qnn_forward(x, theta, n=2):
    qc = QuantumCircuit(n)
    # Encoding layer
    for i in range(n): qc.ry(x[i], i)
    # Trainable layer 1
    for i in range(n): qc.ry(theta[i], i)
    qc.cx(0, 1)
    # Trainable layer 2
    for i in range(n): qc.ry(theta[n+i], i)
    return qc

observable = SparsePauliOp('ZI')

def predict(x, theta):
    qc = qnn_forward(x, theta)
    return Statevector(qc).expectation_value(observable).real

# Binary classification: threshold at 0

data   = [[0.3, 0.2], [1.8, 1.9], [0.1, 0.4], [1.5, 1.6]]
labels = [0, 1, 0, 1]   # 0→ <Z>=+1, 1→ <Z>=-1
targets = [1.0 if l==0 else -1.0 for l in labels]

def loss(theta):
    return sum((predict(x, theta) - t)**2 for x, t in zip(data, targets))

result = minimize(loss, np.random.uniform(0,1,4), method='COBYLA', options={'maxiter':500})
theta_opt = result.x
print("QNN predictions:")
for x, t in zip(data, targets):
    p = predict(x, theta_opt)
    print(f"  x={x}, target={t:+.0f}, pred={p:+.3f}, class={0 if p>0 else 1}")
```
**Sample Output:**
```python
QNN predictions:
  x=[0.3, 0.2], target=+1, pred=+0.810, class=0
  x=[1.8, 1.9], target=-1, pred=-0.917, class=1
  x=[0.1, 0.4], target=+1, pred=+0.810, class=0
  x=[1.5, 1.6], target=-1, pred=-0.730, class=1
```


#### **Outcome and Interpretation**

The expectation value is $\langle Z \rangle = -0.6$. Since $-0.6 < 0.5$, the predicted label is **1**. This project demonstrates the full QNN inference pipeline: a final quantum state is mapped to a continuous expectation value, which is then converted into a discrete class label by a classical decision function.



````python