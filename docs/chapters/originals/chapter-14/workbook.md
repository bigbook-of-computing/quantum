# **Chapter 14: Quantum Optimization (QUBO-Family) () () (Workbook)**

---

> **Summary:** This chapter explores quantum optimization, focusing on the QUBO (Quadratic Unconstrained Binary Optimization) and Ising model formulations, which provide a universal language for mapping NP-hard problems onto quantum hardware. We examine the two primary quantum approaches: Adiabatic Quantum Optimization (AQO), realized in quantum annealers, which slowly evolves a system to its optimal ground state; and the Quantum Approximate Optimization Algorithm (QAOA), a gate-based variational method for NISQ devices. By detailing the mathematical foundations and practical applications of these frameworks, the chapter provides a guide to leveraging near-term quantum computers for solving complex optimization challenges.

---

The goal of this chapter is to establish the foundational concepts and techniques of Quantum Optimization, exploring how quantum computing can enhance traditional optimization frameworks.

---

## **14.1 QUBO and the Ising Model** {.heading-with-pill}

> **Difficulty:** ★★★☆☆
> 
> **Concept:** Equivalent Optimization Frameworks
> 
> **Summary:** Many complex optimization problems can be formulated as a Quadratic Unconstrained Binary Optimization (QUBO) problem. This framework is mathematically equivalent to the Ising model from physics, allowing problems expressed with binary variables to be solved on quantum hardware that operates on spin variables.

---

### **Theoretical Background**

The core idea in quantum optimization is to map a real-world problem onto a mathematical structure that a quantum computer can solve. Two such equivalent structures are dominant:

**Quadratic Unconstrained Binary Optimization (QUBO):** 
    
This framework is used to minimize a cost function of the form:

$$
```
C(\mathbf{x}) = \mathbf{x}^T \mathbf{Q} \mathbf{x} = \sum_{i,j} Q_{ij} x_i x_j
```
$$

Here, $\mathbf{x}$ is a vector of binary variables, $x_i \in \{0, 1\}$, and $\mathbf{Q}$ is a real-valued matrix that defines the problem's cost landscape. The goal is to find the binary vector $\mathbf{x}$ that minimizes $C(\mathbf{x})$.

**Ising Model:** 

Originating from statistical mechanics, the Ising model describes the energy of a system of interacting spins. Its energy function (Hamiltonian) is:

$$
```
E(\mathbf{z}) = \sum_{i < j} J_{ij} z_i z_j + \sum_i h_i z_i
```
$$

Here, $\mathbf{z}$ is a vector of spin variables, $z_i \in \{-1, 1\}$, $J_{ij}$ are the coupling strengths between spins, and $h_i$ are external fields. Nature seeks the lowest energy state, which corresponds to the optimal solution.

The two models are mathematically equivalent via the simple transformation:

$$
z_i = 2x_i - 1 \quad \iff \quad x_i = \frac{z_i + 1}{2}
$$

This mapping is crucial because many real-world problems are naturally expressed in binary terms (QUBO), while quantum optimizers (especially annealers) are physically built to find the ground state of an Ising Hamiltonian.

---

### **Comprehension Check**

!!! note "Quiz"

    1.  The mapping $z_i = 2x_i - 1$ is used to convert a QUBO problem into an equivalent Ising model. This changes the domain of the variables from binary ($x_i \in \{0, 1\}$) to:
```
    - A. Real numbers $z_i \in [0, 1]$.
    - B. Spin variables $z_i \in \{-1, 1\}$.
    - C. Continuous angles $z_i \in [0, 2\pi]$.

??? info "See Answer"
    **Correct: B**. The transformation maps binary variables to spin variables.

```
!!! abstract "Interview-Style Question"

```
Explain the practical necessity of the mathematical equivalence between QUBO and the Ising Model in the context of commercial quantum hardware.

???+ info "Answer Strategy"
    The equivalence is a crucial bridge between how we formulate problems and how quantum hardware solves them.

    1.  **Problem Formulation (QUBO):** Many real-world optimization problems in business, logistics, and finance are most naturally expressed using binary variables ($x_i \in \{0, 1\}$), which is the language of QUBO. For example, "Should we include this asset in the portfolio or not?"

    2.  **Hardware Operation (Ising):** Quantum hardware, especially quantum annealers, is physically built to find the lowest energy state of a system of interacting spins ($z_i \in \{-1, 1\}$). This is the language of the Ising model.

    3.  **The Necessary Translator:** The mathematical equivalence acts as a compiler. It translates the problem from its natural binary language (QUBO) into the spin-based language (Ising) that the quantum hardware physically understands. Without this bridge, we could not solve practical business problems on these specialized quantum devices.

```
---

## **14.2 Adiabatic and Variational Optimization** {.heading-with-pill}

> **Difficulty:** ★★★★☆
> 
> **Concept:** Quantum Solution Finding via Evolution
> 
> **Summary:** Adiabatic Quantum Optimization (AQO) finds solutions by slowly evolving a simple initial Hamiltonian to a complex problem Hamiltonian. The Quantum Approximate Optimization Algorithm (QAOA) is a variational, gate-based alternative that approximates this process for near-term quantum devices.

---

### **Theoretical Background**

Once a problem is in the Ising form, we need a quantum algorithm to find its ground state.

**1. Adiabatic Quantum Optimization (AQO) & Quantum Annealing:**

AQO is based on the **Adiabatic Theorem**. The process is as follows:
-   Start with a simple initial Hamiltonian, $H_0$, whose ground state is easy to prepare. A common choice is $H_0 = \sum_i X_i$, where the ground state is an equal superposition of all possible solutions.
-   Define the problem Hamiltonian, $H_P$, which is the Ising model of our problem. Its ground state is the optimal solution we seek.
-   Slowly evolve the system's Hamiltonian over a total time $T$:

$$
```
H(t) = \left(1 - \frac{t}{T}\right) H_0 + \left(\frac{t}{T}\right) H_P
```
$$

-   The Adiabatic Theorem guarantees that if the evolution is sufficiently slow (i.e., $T$ is large enough), the system will remain in the ground state throughout the process. At $t=T$, the system will be in the ground state of $H_P$, and measuring it reveals the solution. **Quantum Annealing** is the physical implementation of this principle.

**2. Quantum Approximate Optimization Algorithm (QAOA):**

QAOA is a hybrid, variational algorithm designed for NISQ-era devices. It approximates the adiabatic evolution with a fixed-depth quantum circuit.
-   The circuit consists of $p$ alternating layers of two unitary operators:
```
-   $U_C(\gamma) = e^{-i\gamma H_P}$: The **cost unitary**, which applies phases based on the problem Hamiltonian.
-   $U_B(\beta) = e^{-i\beta H_0}$: The **mixer unitary**, which drives transitions between solutions.
```
-   The full state is prepared as $|\psi(\vec{\gamma}, \vec{\beta})\rangle = U_B(\beta_p)U_C(\gamma_p) \cdots U_B(\beta_1)U_C(\gamma_1) |s_0\rangle$.
-   A classical optimizer then tunes the $2p$ angles $(\vec{\gamma}, \vec{\beta})$ to minimize the expected energy $\langle \psi | H_P | \psi \rangle$.

---

### **Comprehension Check**

!!! note "Quiz"

    1.  In the QAOA circuit, the two alternating unitaries $U_C(\gamma)$ and $U_B(\beta)$ correspond to the effects of which two Hamiltonians from the adiabatic process?
```
    - A. The Entanglement Hamiltonian and the Phase Hamiltonian.
    - B. The Problem Hamiltonian ($H_P$) and the Initial Hamiltonian ($H_0$).
    - C. The Identity and the X gate.

??? info "See Answer"
    **Correct: B**. $U_C$ evolves under the problem Hamiltonian, and $U_B$ evolves under the initial/mixer Hamiltonian.

```
!!! abstract "Interview-Style Question"

```
Compare and contrast Quantum Annealing and QAOA as approaches to quantum optimization.

???+ info "Answer Strategy"
    Both are leading methods for quantum optimization, but they differ fundamentally in their approach and hardware requirements.

    | Feature | Quantum Annealing (QA) | QAOA |
    | :--- | :--- | :--- |
    | **Process** | **Analog:** A continuous, physical process that slowly morphs a simple energy landscape into the complex problem landscape. | **Digital:** A gate-based, discrete approximation of an adiabatic evolution, broken into steps. |
    | **Hardware** | **Specialized:** Runs on quantum annealers (e.g., D-Wave). | **Universal:** Runs on general-purpose, gate-based quantum computers (e.g., IBM, Google). |
    | **Control** | **Simple:** The main control knob is the total annealing (evolution) time. It's largely a "fire-and-forget" process. | **Complex & Variational:** Requires a classical optimization loop to tune a set of $2p$ circuit parameters $(\vec{\gamma}, \vec{\beta})$. |
    | **Guarantees** | **Theoretical:** The Adiabatic Theorem guarantees finding the ground state if the evolution is infinitely slow (barring thermal noise and small energy gaps). | **Heuristic:** Performance depends heavily on the circuit depth ($p$) and the success of the classical optimizer. There is no guarantee of finding the optimal solution. |

    **In short:** Annealing is an analog, hardware-specific approach with strong theoretical backing, while QAOA is a digital, flexible, and hardware-agnostic variational algorithm designed for the NISQ era.

```
---

## **14.3 Application: Portfolio Optimization** {.heading-with-pill}

> **Difficulty:** ★★★☆☆
> 
> **Concept:** Balancing Risk and Return with QUBO
> 
> **Summary:** Portfolio optimization is a classic finance problem that maps well to QUBO. The objective is to select a subset of assets that maximizes expected return while minimizing risk, which is defined by the covariance between assets.

---

### **Theoretical Background**

A key application of QUBO is in finance, specifically **portfolio optimization**. Given a set of $n$ assets, we want to choose which ones to include in our portfolio.

Let $x_i \in \{0, 1\}$ be a binary variable where $x_i=1$ means we select asset $i$. The goal is to balance two competing factors:

1.  **Expected Return:** We want to maximize the total return. This is modeled by a vector $\mathbf{\mu}$, where $\mu_i$ is the expected return of asset $i$. The total return is $\sum_i \mu_i x_i$.
2.  **Risk:** We want to minimize the portfolio's volatility. This is captured by the **covariance matrix** $\mathbf{\Sigma}$, where $\Sigma_{ij}$ measures how asset $i$ and asset $j$ move together. The total risk is $\mathbf{x}^T \mathbf{\Sigma} \mathbf{x}$.

The combined objective function to be minimized is:

$$
\text{Minimize} \quad C(\mathbf{x}) = \underbrace{-\mathbf{\mu}^T \mathbf{x}}_{\text{Maximize Return}} + \underbrace{q \cdot \mathbf{x}^T \mathbf{\Sigma} \mathbf{x}}_{\text{Minimize Risk}}
$$

Here, $q$ is a risk-aversion parameter that balances the trade-off. This expression is already in the QUBO form, where the matrix $\mathbf{Q}$ is constructed from the covariance matrix $\mathbf{\Sigma}$ and the return vector $\mathbf{\mu}$. Solving this QUBO gives the optimal portfolio $\mathbf{x}$.

---

### **Comprehension Check**

!!! note "Quiz"

    1.  In the quantum formulation of Portfolio Optimization, the risk of the portfolio is primarily encoded by which component?
```
    - A. The expected return vector $\mathbf{\mu}$.
    - B. The selection vector $\mathbf{x}$.
    - C. The covariance matrix $\mathbf{\Sigma}$.

??? info "See Answer"
    **Correct: C**. The covariance matrix defines the risk arising from assets moving together.

```
!!! abstract "Interview-Style Question"

```
A portfolio manager asks you why they should consider a quantum approach for portfolio optimization over classical solvers. What is the potential, long-term advantage you would highlight?

???+ info "Answer Strategy"
    The key long-term advantage is the potential to handle the **combinatorial explosion** inherent in portfolio selection more effectively than any classical computer.

    1.  **The Scaling Problem:** With $N$ assets, there are $2^N$ possible portfolios. As the number of available assets grows, this search space becomes astronomically large, making it impossible for classical computers to check every combination. Classical solvers must rely on heuristics and approximations that may miss the true optimal portfolio.

    2.  **The Quantum Promise:** Quantum optimization algorithms (like QAOA or Quantum Annealing) are designed to navigate these massive combinatorial spaces. By using principles like superposition and entanglement, they can explore a vast number of possibilities simultaneously. This offers the potential to find higher-quality portfolios (i.e., better risk/return profiles) that are inaccessible to classical methods.

    3.  **The Important Caveat:** It's crucial to be transparent that this is a **future-facing advantage**. Today's NISQ-era quantum computers are not yet large or robust enough to outperform state-of-the-art classical solvers on this problem. The advantage is predicated on the future development of larger, fault-tolerant quantum hardware.

```
---

## **14.4 Constraint Encoding with Penalty Terms** {.heading-with-pill}

> **Difficulty:** ★★★☆☆
> 
> **Concept:** Enforcing Rules in Optimization Problems
> 
> **Summary:** Real-world optimization problems have constraints (e.g., budget limits). In QUBO, these are handled by adding a large penalty term to the cost function. This term is designed to be zero when the constraint is satisfied and very large when it is violated, effectively forcing the optimizer to find valid solutions.

---

### **Theoretical Background**

QUBO stands for *Unconstrained* Binary Optimization, but most real-world problems have constraints. For example, in portfolio optimization, we might have a budget limiting us to select exactly $B$ assets.

The standard way to handle a constraint is to add a **penalty term** to the objective function. The full objective becomes:

$$
C_{\text{total}}(\mathbf{x}) = C_{\text{objective}}(\mathbf{x}) + \lambda \cdot P(\mathbf{x})
$$

-   $C_{\text{objective}}(\mathbf{x})$ is the original QUBO objective (e.g., risk vs. return).
-   $P(\mathbf{x})$ is the penalty function, which must be a polynomial in $x_i$ that is zero if the constraint is satisfied and positive if it is violated.
-   $\lambda$ is a large positive constant, the **penalty factor**. Its job is to make any violation of the constraint so costly that the minimizer will always prefer solutions where $P(\mathbf{x})=0$.

For example, to enforce the constraint "select exactly $B$ assets" ($\sum_i x_i = B$), the penalty function is:

$$
P(\mathbf{x}) = \left( \sum_i x_i - B \right)^2
$$

This term is zero if and only if the constraint is met. Expanding this quadratic term and adding it to the original QUBO matrix $\mathbf{Q}$ yields a new, larger QUBO that encodes the constraint directly into the cost landscape.

---

### **Comprehension Check**

!!! note "Quiz"

    1.  The most common method for handling a budget constraint in a QUBO formulation is to:
```
    - A. Use a continuous variable solver.
    - B. Add a penalty term to the cost function.
    - C. Enforce the constraint with the $H_0$ Hamiltonian.

??? info "See Answer"
    **Correct: B**. A penalty term makes invalid solutions have a very high cost.

```
!!! abstract "Interview-Style Question"

```
What is the main challenge in choosing the penalty factor $\lambda$? What happens if it's too small or too large?

???+ info "Answer Strategy"
    The main challenge is the "Goldilocks problem": the penalty factor $\lambda$ must be finely tuned to be "just right." It needs to be strong enough to enforce the constraint without overwhelming the original problem.

    *   **If $\lambda$ is too small:**
        *   **Effect:** The penalty for violating the constraint is insignificant.
        *   **Result:** The optimizer may find a solution that has a great objective score but is **invalid** because it breaks the rule (e.g., a portfolio that is over budget). The constraint is treated as a weak suggestion, not a hard rule.

    *   **If $\lambda$ is too large:**
        *   **Effect:** The penalty term dominates the entire cost function, "drowning out" the original objective. The energy landscape becomes a flat plain of valid solutions surrounded by massive penalty walls.
        *   **Result:** The optimizer will certainly find a **valid** solution, but it will likely not be the **optimal** one. The subtle variations in the original cost function that guide the search for the best solution are lost in the noise of the huge penalty values. This can also make the problem numerically unstable and harder for the solver to handle.

```
---

## **14.5 From Theory to Practice: QUBO Projects** {.heading-with-pill}

> **Difficulty:** ★★★☆☆
> 
> **Concept:** Applying QUBO Principles to Concrete Problems
> 
> **Summary:** These projects provide hands-on experience in converting problems into the QUBO and Ising frameworks, defining QUBO matrices for classic problems like Max-Cut, and implementing constraints using penalty methods.

---

### **<i class="fa-solid fa-flask"></i> Hands-On Projects**

#### Project Blueprint: QUBO to Ising Conversion

| Component | Description |
| :--- | :--- |
| **Objective** | Convert a simple QUBO objective function into its equivalent Ising model formulation. |
| **Mathematical Concept** | The transformation $x_i = (z_i + 1)/2$ maps binary variables to spin variables. |
| **Experiment Setup** | QUBO cost function: $C(x) = x_1 x_2 - 3x_1$, where $x_1, x_2 \in \{0, 1\}$. |
| **Process Steps** | 1. Substitute $x_i = (z_i + 1)/2$ into $C(x)$. <br> 2. Algebraically expand and simplify the expression. <br> 3. Group terms to match the Ising form $E(z) = J_{12} z_1 z_2 + h_1 z_1 + h_2 z_2 + \text{Const}$. <br> 4. Identify the coefficients $J_{12}$, $h_1$, and $h_2$. |
| **Expected Behavior** | The binary objective function will be perfectly transformed into a spin-based energy function with specific coupling and field terms. |
| **Verification Goal** | Find the numerical values for $J_{12}$, $h_1$, and $h_2$. |

---

#### **Python Implementation**

```python
import numpy as np
from itertools import product

# Project: QUBO Formulation and Brute-Force Solver
# MaxCut on a weighted 4-node graph → QUBO form

# Graph adjacency (weighted)
W = np.array([
    [0, 1.0, 0.5, 0  ],
    [1.0, 0, 0  , 1.5],
    [0.5, 0, 0  , 1.0],
    [0  , 1.5, 1.0, 0],
])

# QUBO matrix: Q_ij = -W_ij + delta_ij * sum_k W_ik
def maxcut_qubo(W):
    n = len(W)
    Q = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            if i == j:
                Q[i, i] = -sum(W[i, :])  # diagonal: -degree
            elif i < j:
                Q[i, j] = W[i, j]
    return Q

Q = maxcut_qubo(W)
print("QUBO matrix Q:")
print(np.round(Q, 2))

# Brute-force: find binary vector x minimizing x^T Q x
best_x, best_val = None, np.inf
n = len(W)
for bits in product([0, 1], repeat=n):
    x = np.array(bits, dtype=float)
    val = x @ Q @ x
    if val < best_val:
        best_val, best_x = val, bits

print(f"\nOptimal partition: {best_x}  (QUBO objective = {best_val:.3f})")
cut_value = sum(W[i,j] for i in range(n) for j in range(i+1,n)
                if best_x[i] != best_x[j])
print(f"MaxCut value: {cut_value}")
```
**Sample Output:**
```
QUBO matrix Q:
[[-1.5  1.   0.5  0. ]
 [ 0.  -2.5  0.   1.5]
 [ 0.   0.  -1.5  1. ]
 [ 0.   0.   0.  -2.5]]

Optimal partition: (0, 1, 1, 0)  (QUBO objective = -4.000)
MaxCut value: 4.0
```




#### Outcome and Interpretation

The QUBO function $C(x) = x_1 x_2 - 3x_1$ is equivalent to the Ising model $E(z) = 0.25 z_1 z_2 - 1.25 z_1 + 0.25 z_2 - 1.25$. This demonstrates how a binary optimization problem can be directly translated into the language of interacting spins, ready for a quantum annealer.

---

#### Project Blueprint: Max-Cut QUBO Formulation

| Component | Description |
| :--- | :--- |
| **Objective** | Define the QUBO matrix $\mathbf{Q}$ that represents the Max-Cut problem for a simple graph. |
| **Mathematical Concept** | The Max-Cut objective is to partition nodes into two sets to maximize the number of edges between them. This is equivalent to minimizing the number of edges *within* the same set. |
| **Experiment Setup** | A 3-node complete graph (triangle) with edges (1,2), (2,3), and (1,3). Let $x_i=0$ for one partition and $x_i=1$ for the other. An edge $(i,j)$ is *not* cut if $x_i=x_j$. |
| **Process Steps** | 1. Write the cost function to minimize: $C(x) = (x_1-x_2)^2 + (x_2-x_3)^2 + (x_1-x_3)^2$. This penalizes nodes in the same partition. <br> 2. Expand the expression: $C(x) = (x_1^2 - 2x_1x_2 + x_2^2) + \dots$ <br> 3. Use the identity $x_i^2 = x_i$ for binary variables to simplify into the form $\mathbf{x}^T \mathbf{Q} \mathbf{x}$. <br> 4. Construct the $3 \times 3$ QUBO matrix $\mathbf{Q}$. |
| **Expected Behavior** | The resulting $\mathbf{Q}$ matrix will encode the graph structure. Evaluating $\mathbf{x}^T \mathbf{Q} \mathbf{x}$ for different partitions will show that partitions cutting more edges have a lower cost. |
| **Verification Goal** | Show that the partition $x=(1,0,1)^T$ (2 edges cut) has a lower cost than $x=(1,1,1)^T$ (0 edges cut). |

#### Outcome and Interpretation

The cost function simplifies to $C(x) = 2(x_1+x_2+x_3) - 2(x_1x_2 + x_2x_3 + x_1x_3)$. This can be represented by a QUBO matrix. This project shows how a graph problem can be directly translated into the algebraic QUBO format, demonstrating the broad applicability of the framework.

---

#### Project Blueprint: Penalty Constraint Encoding

| Component | Description |
| :--- | :--- |
| **Objective** | Use a penalty term to enforce a hard constraint in a QUBO objective. |
| **Mathematical Concept** | The total cost is $C(x) = C_{\text{obj}} + \lambda \cdot (\text{constraint})^2$. |
| **Experiment Setup** | Objective: Minimize $C_{\text{obj}} = 2x_1 + 3x_2$. Constraint: $x_1 + x_2 = 1$. Penalty factor $\lambda=10$. |
| **Process Steps** | 1. Define the penalty function: $P(x) = (x_1 + x_2 - 1)^2$. <br> 2. Write the total cost function: $C(x) = 2x_1 + 3x_2 + 10(x_1 + x_2 - 1)^2$. <br> 3. Expand and simplify $C(x)$ into the standard QUBO form, using $x_i^2=x_i$. <br> 4. Evaluate $C(x)$ for all four binary configurations: (0,0), (0,1), (1,0), (1,1). |
| **Expected Behavior** | The configurations that violate the constraint, (0,0) and (1,1), will have a very high cost due to the penalty, while the valid configurations, (0,1) and (1,0), will have much lower costs. |
| **Verification Goal** | Show that the minimum cost corresponds to the valid configuration $(1,0)$, which correctly minimizes the original objective $2x_1+3x_2$ while satisfying the constraint. |

#### Outcome and Interpretation

-   $C(0,0) = 0 + 10(-1)^2 = 10$.
-   $C(0,1) = 3 + 10(0)^2 = 3$.
-   $C(1,0) = 2 + 10(0)^2 = 2$. **(Minimum)**
-   $C(1,1) = 5 + 10(1)^2 = 15$.

The penalty method successfully forces the solution away from the invalid states (0,0) and (1,1), and the optimizer correctly identifies (1,0) as the optimal valid solution. This demonstrates the power of penalty methods to handle constrained problems within the QUBO framework.