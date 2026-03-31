# **Chapter 9: Quantum Data Encoding Techniques () () (Workbook)**

---

> **Summary:** This chapter provides a comprehensive analysis of the primary techniques for encoding classical data into quantum states, a critical step in the quantum machine learning pipeline. We examine basis, amplitude, angle, and Hamiltonian encoding, as well as quantum feature maps, evaluating their mathematical foundations, implementation complexities, and the trade-offs between data compression and circuit depth. The discussion highlights how amplitude encoding offers exponential compression at the cost of a data loading bottleneck, while angle encoding and feature maps provide the shallow circuits necessary for NISQ-era algorithms. Understanding these encoding strategies is fundamental to designing practical quantum machine learning models and realizing quantum advantage.

---

## 1. Basis Encoding

!!! question "What is Basis Encoding and what are its main limitations?"
```
Basis encoding, also known as computational basis encoding, is a method for representing classical binary data in a quantum system. It maps a classical binary string to a corresponding quantum computational basis state.

- **Mechanism**: An $n$-bit classical string $s = s_1s_2...s_n$ is mapped to the quantum state $|s\rangle = |s_1\rangle \otimes |s_2\rangle \otimes ... \otimes |s_n\rangle$.
- **Example**: The classical string `101` is encoded as the quantum state $|101\rangle$.

**Limitations**:
1.  **Resource Intensive**: It requires $N$ qubits to store $N$ bits of information, offering no data compression.
2.  **Limited Quantum Advantage**: Since it doesn't use superposition, it often fails to leverage the full power of quantum computation. Many algorithms that use basis encoding can be simulated efficiently on a classical computer.

```
<div class="heading-with-pill">
```
<div class="heading-text">Hands-on</div>
<div class="pill-right">Basis Encoding</div>
```
</div>

!!! example "Example: Encoding a Binary String"
```
Let's encode the 4-bit string `1101` into a quantum state using Qiskit.

```python
from qiskit import QuantumCircuit

# The classical binary string
binary_string = "1101"

# Create a quantum circuit with a qubit for each bit
qc = QuantumCircuit(len(binary_string))

# Apply an X gate for each '1' in the string (from right to left)
for i, bit in enumerate(reversed(binary_string)):
    if bit == '1':
        qc.x(i)

# The statevector simulator can show the resulting quantum state
from qiskit.quantum_info import Statevector
state = Statevector(qc)
print(f"The encoded state is: {state.draw(output='latex_source')}")
# Output: The encoded state is: |1101>
```
```
**Sample Output:**
```python
The encoded state is:  |1101\rangle
```

```
The circuit prepares the state $|1101\rangle$, directly corresponding to the classical input.

```
!!! abstract "Interview-Style Question"
```
**Q:** When is basis encoding preferable to amplitude or angle encoding in QML pipelines?

???+ info "Answer Strategy"
    Basis encoding is generally the least powerful encoding method, but it finds a niche in specific scenarios where its simplicity and direct mapping are advantageous. It is preferable under the following conditions:

    1.  **Discrete, Categorical Data:** When dealing with inherently discrete and non-numeric data (e.g., categories like "cat," "dog," "bird"), basis encoding provides a direct and unambiguous representation. Each category can be assigned a unique basis state (e.g., $|00\rangle, |01\rangle, |10\rangle$).
    2.  **Quantum Oracle Implementation:** It is fundamental for building oracles in algorithms like Grover's search. The oracle needs to "mark" a specific basis state corresponding to the solution, making this encoding a natural fit.
    3.  **Avoiding Non-Linearity:** If a QML model must remain simple and linear, basis encoding is a good choice. Angle and amplitude encoding introduce non-linearities that might not be desirable for all models.
    4.  **Readout Simplicity:** Measuring in the computational basis directly yields the classical data, making the readout process straightforward.

    In summary, choose basis encoding when your data is discrete, you need to implement oracles, or you require a simple, linear model without the complexities of other encodings.

```
---

## 2. Amplitude Encoding

!!! question "What is Amplitude Encoding and what is its primary bottleneck?"
```
Amplitude encoding is a powerful technique for representing a classical vector in a quantum state. It maps a normalized $N$-dimensional classical vector to the amplitudes of a quantum state with $\log_2 N$ qubits.

- **Mechanism**: A classical vector $\mathbf{x} = (x_1, x_2, ..., x_N)$ with $\|\mathbf{x}\|=1$ is encoded as the state $|\psi\rangle = \sum_{i=1}^{N} x_i |i\rangle$.
- **Advantage**: It offers exponential data compression, storing $N$ values in only $\log_2 N$ qubits.

**Primary Bottleneck**:
The main challenge is **state preparation**. For a general, arbitrary classical vector, creating the corresponding quantum state requires a circuit with a depth that scales linearly with $N$, i.e., $O(N)$. This cost of loading the data often negates the exponential speedup promised by the quantum algorithm itself, as the classical preprocessing and data loading dominate the total runtime.

```
<div class="heading-with-pill">
```
<div class="heading-text">Hands-on</div>
<div class="pill-right">Amplitude Encoding</div>
```
</div>

!!! example "Example: Encoding a 4D Vector"
```
Let's encode the normalized vector $\mathbf{x} = [0.5, 0.5, 0.5, 0.5]$ into a 2-qubit state. This specific vector corresponds to an equal superposition state.

```python
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector
import numpy as np

# The classical vector to encode
vector = np.array([0.5, 0.5, 0.5, 0.5])

# Normalize the vector (it's already normalized in this case)
norm = np.linalg.norm(vector)
normalized_vector = vector / norm

# Create a quantum circuit with log2(N) qubits
num_qubits = int(np.log2(len(normalized_vector)))
qc = QuantumCircuit(num_qubits)

# For this special case, applying H-gates creates the state
for i in range(num_qubits):
    qc.h(i)

# The initialize() method can prepare an arbitrary state
# qc.initialize(normalized_vector, range(num_qubits))

state = Statevector(qc)
print(f"The encoded state is: {state.draw(output='latex_source')}")
# Output: The encoded state is: 0.5 |00> + 0.5 |01> + 0.5 |10> + 0.5 |11>
```
```
**Sample Output:**
```python
The encoded state is: \frac{1}{2} |00\rangle+\frac{1}{2} |01\rangle+\frac{1}{2} |10\rangle+\frac{1}{2} |11\rangle
```

```
For arbitrary vectors, the `initialize()` function is used, but it hides the complex, deep circuit required for state preparation.

```
!!! abstract "Interview-Style Question"
```
**Q:** Why does amplitude encoding often fail to provide a real-world speedup despite its exponential data compression?

???+ info "Answer Strategy"
    Amplitude encoding represents a classical vector of size $N$ using only $\log_2 N$ qubits, offering exponential compression. However, this often fails to provide a wall-clock speedup due to two main bottlenecks:

    1.  **State Preparation Cost:** For a general classical vector, preparing the corresponding quantum state requires a circuit with a depth that scales as $\Theta(N)$. This classical preprocessing step dominates the overall runtime, negating the $O(\log N)$ complexity of the quantum algorithm itself.
    2.  **Data Loading:** Even before the quantum circuit runs, the classical data must be read and processed, which is a $\Theta(N)$ operation.

    A true speedup is only realized if the data is already in a quantum state or has a special structure that allows for efficient (sub-linear) state preparation.

```
---

## 3. Angle Encoding

!!! question "What is Angle Encoding and what are its key properties?"
```
Angle encoding is a data encoding technique that maps classical features to the rotation angles of single-qubit gates. It is widely used in variational quantum circuits.

- **Mechanism**: A feature vector $\mathbf{x} = (x_1, ..., x_N)$ is encoded by applying rotation gates $R_p(\phi(x_i))$ to $N$ qubits, where $p \in \{X, Y, Z\}$ and $\phi$ is a scaling function. For example, $|\psi(\mathbf{x})\rangle = \bigotimes_{i=1}^N R_y(x_i) |0\rangle_i$.

**Key Properties**:
1.  **Non-linear Mapping**: The use of trigonometric functions in rotation gates creates a non-linear mapping from the data to the quantum state's amplitudes. This allows the model to learn complex, non-linear relationships.
2.  **Hardware-Efficient**: The encoding circuit is typically shallow (depth 1 for the basic form), making it suitable for noisy intermediate-scale quantum (NISQ) devices.
3.  **No Data Compression**: It requires $N$ qubits to encode $N$ features.

```
<div class="heading-with-pill">
```
<div class="heading-text">Hands-on</div>
<div class="pill-right">Angle Encoding</div>
```
</div>

!!! example "Example: Encoding a 2D Vector"
```
Let's encode the vector $\mathbf{x} = [\pi/2, \pi/4]$ into a 2-qubit state using $R_y$ rotations.

```python
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector
import numpy as np

# The classical vector to encode
vector = np.array([np.pi/2, np.pi/4])

# Create a quantum circuit with a qubit for each feature
qc = QuantumCircuit(len(vector))

# Apply Ry gates with the feature values as angles
for i, angle in enumerate(vector):
    qc.ry(angle, i)

state = Statevector(qc)
print(f"The encoded state is: {state.draw(output='latex_source')}")
# Output: The encoded state is: 0.653 |00> + 0.271 |01> + 0.653 |10> + 0.271 |11>
```
```
**Sample Output:**
```python
The encoded state is: 0.6532814824 |00\rangle+0.6532814824 |01\rangle+0.2705980501 |10\rangle+0.2705980501 |11\rangle
```

```
The resulting state's amplitudes are non-linear functions ($\cos(\theta/2), \sin(\theta/2)$) of the input features.

```
!!! abstract "Interview-Style Question"
```
**Q:** Describe the trade-offs of using angle encoding in a QML model.

???+ info "Answer Strategy"
    Angle encoding is a feature-rich method that maps a classical feature vector $\mathbf{x} = (x_1, \ldots, x_N)$ to the rotation angles of single-qubit gates, typically using a circuit of the form $U(\mathbf{x}) = \bigotimes_{i=1}^N R_y(x_i)$, where $R_y$ is a rotation-Y gate.

    **Key Properties:**

    1.  **Non-linearity:** The mapping from data to quantum state is non-linear due to the trigonometric nature of rotation gates ($e^{-i \frac{\theta}{2} Y}$). This allows angle encoding to implicitly create complex, high-dimensional feature maps, similar to classical kernel methods. The resulting quantum model can learn non-linear decision boundaries without requiring explicit non-linear activation functions.
    2.  **Entanglement-Free:** In its basic form, angle encoding is a "product state" or "tensor product" map. Each qubit encodes exactly one feature, and no entangling gates (like CNOT) are used. This makes the circuit shallow and hardware-efficient but limits its expressivity, as it cannot capture correlations between features.
    3.  **Re-uploading for Expressivity:** To overcome the limitations of a single encoding layer, "data re-uploading" can be used. This involves alternating layers of angle encoding and variational (trainable) gates. This technique allows a fixed number of qubits to approximate any continuous function, effectively turning the circuit into a universal function approximator.

    **Trade-offs:**

    *   **Pros:** Hardware-efficient, non-linear, and easily extendable with data re-uploading.
    *   **Cons:** Uses $N$ qubits for $N$ features (no compression), and the basic form lacks entanglement, limiting its ability to model feature correlations.

    Angle encoding is a practical and powerful choice for many QML models, especially when non-linearity is desired and the number of features is manageable for current quantum hardware.

```
---

## 4. Hamiltonian Encoding

!!! question "What is Hamiltonian Encoding and where is it typically used?"
```
Hamiltonian encoding, also known as dense encoding or block encoding, embeds a matrix $A$ into a Hamiltonian $H$ such that $A$ is a sub-block of $H$. This method is more abstract than other encodings and is central to advanced quantum algorithms.

- **Mechanism**: Given a matrix $A$, we construct a Hamiltonian $H$ (often for a larger system) where $A$ can be accessed. For example, $H = \begin{pmatrix} A & \cdot \\ \cdot & \cdot \end{pmatrix}$. The algorithm then simulates the evolution $e^{-iHt}$ to apply the effects of $A$.

**Typical Use Cases**:
1.  **Quantum Simulation**: It is the natural way to represent the Hamiltonian of a physical system (like a molecule) that you want to simulate on a quantum computer.
2.  **HHL Algorithm**: The HHL algorithm for solving linear systems of equations $A\mathbf{x}=\mathbf{b}$ requires encoding the matrix $A$ into a Hamiltonian to perform quantum phase estimation and matrix inversion.
3.  **Advanced Algorithms**: Many modern quantum algorithms, particularly those based on the quantum singular value transformation (QSVT), rely on block encodings to manipulate matrices.

```
!!! abstract "Interview-Style Question"
```
**Q:** Why is Hamiltonian encoding considered less of a "data loading" technique and more of a "problem definition" technique?

???+ info "Answer Strategy"
    Hamiltonian encoding differs fundamentally from methods like angle or amplitude encoding. While the latter are designed to load classical *data vectors* into a quantum state, Hamiltonian encoding is designed to embed a classical *matrix* (representing a linear operator or a problem) into the dynamics of a quantum system.

    Here’s the distinction:

    1.  **Input Type:**
        *   **Data Loading (Angle/Amplitude):** Input is a vector $\mathbf{x}$. The goal is to create the state $|\psi(\mathbf{x})\rangle$.
        *   **Problem Definition (Hamiltonian):** Input is a matrix $A$. The goal is to create a process (time evolution $e^{-iHt}$) that *acts on* quantum states according to $A$.

    2.  **Purpose:**
        *   **Data Loading:** Prepares the input for a quantum algorithm. It's the "noun" or the subject of the computation.
        *   **Problem Definition:** Defines the core operation of the algorithm itself. It's the "verb" or the action of the computation.

    For example, in the HHL algorithm ($A\mathbf{x}=\mathbf{b}$), amplitude encoding is used to load the vector $\mathbf{b}$ into a state $|\mathbf{b}\rangle$, while Hamiltonian encoding is used to represent the matrix $A$ as an operator that can be manipulated. You are not loading the matrix $A$ as a state to be processed; you are defining the system's evolution based on $A$.

```
---

## 5. Quantum Feature Maps and Kernels

!!! question "What is a quantum feature map and how does it relate to quantum kernels?"
```
A **quantum feature map** is a procedure that maps a classical data point $\mathbf{x}$ to a quantum state $|\phi(\mathbf{x})\rangle$ in a high-dimensional Hilbert space. The encoding techniques discussed earlier (angle, amplitude, etc.) are all examples of feature maps.

- **Purpose**: To transform classical data into a quantum representation where patterns might be more easily identified. The non-linearity of angle encoding, for instance, creates a complex feature map.

A **quantum kernel** is a measure of similarity between two data points, computed in the quantum feature space. It is defined as the inner product of their corresponding quantum states.

- **Mechanism**: The kernel value for two data points $\mathbf{x}_i$ and $\mathbf{x}_j$ is given by $K(\mathbf{x}_i, \mathbf{x}_j) = |\langle \phi(\mathbf{x}_i) | \phi(\mathbf{x}_j) \rangle|^2$.
- **Application**: This kernel matrix can be fed into a classical machine learning algorithm, such as a Support Vector Machine (SVM), to perform classification. This is the basis of the "quantum kernel trick."

```
<div class="heading-with-pill">
```
<div class="heading-text">Hands-on</div>
<div class="pill-right">Quantum Kernel</div>
```
</div>

!!! example "Example: Computing a Kernel Entry"
```
Let's compute a single entry of a quantum kernel matrix using Qiskit's `Fidelity` primitive. We'll use a simple angle encoding feature map.

```python
from qiskit import QuantumCircuit
from qiskit_algorithms.primitives import Fidelity

# Define the feature map (angle encoding)
def feature_map(x):
    qc = QuantumCircuit(1)
    qc.ry(x[0], 0)
    return qc

# Two data points
x_i = [1.5]
x_j = [2.0]

# Create the circuits for the two points
qc_i = feature_map(x_i)
qc_j = feature_map(x_j)

# Use the Fidelity primitive to compute the inner product squared
fidelity = Fidelity()
result = fidelity.run(qc_i, qc_j).result()
kernel_entry = result.fidelities[0]

print(f"The kernel entry K(x_i, x_j) is: {kernel_entry:.4f}")
# Output: The kernel entry K(x_i, x_j) is: 0.9405
```
This value represents the similarity between the two data points in the quantum feature space. Repeating this for all pairs of data points creates the full kernel matrix.

```
!!! abstract "Interview-Style Question"
```
**Q:** What is the "quantum kernel trick," and what potential advantages does it offer over classical kernels?

???+ info "Answer Strategy"
    The "quantum kernel trick" is a hybrid quantum-classical machine learning method where a quantum computer is used to estimate a kernel matrix, which is then used to train a classical kernel machine like a Support Vector Machine (SVM).

    **The Workflow:**
    1.  **Feature Map:** Choose a quantum encoding (feature map) $\mathbf{x} \mapsto |\phi(\mathbf{x})\rangle$.
    2.  **Kernel Estimation (Quantum Part):** For every pair of data points $(\mathbf{x}_i, \mathbf{x}_j)$ in the training set, use a quantum computer to estimate the kernel $K(\mathbf{x}_i, \mathbf{x}_j) = |\langle \phi(\mathbf{x}_i) | \phi(\mathbf{x}_j) \rangle|^2$. This is often done using a SWAP test or an equivalent circuit.
    3.  **Classical Training (Classical Part):** Feed the resulting kernel matrix $K$ into a classical SVM solver to find the optimal separating hyperplane.

    **Potential Advantages:**
    The primary hope is that quantum feature maps can create kernels that are **classically intractable to compute**. If a quantum computer can efficiently calculate a kernel that would take exponential time for a classical computer, it could lead to a quantum advantage. This might happen if the feature space explored by the quantum map is so large and complex that classical methods cannot efficiently simulate it.

    However, a significant challenge is that many currently proposed quantum kernels can be efficiently simulated classically, or they suffer from noise and measurement errors that diminish their effectiveness. The search for provably advantageous quantum kernels is an active area of research.
```