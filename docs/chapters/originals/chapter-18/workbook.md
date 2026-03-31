# **Chapter 18: 18.1 Quantum Monte Carlo for Option Pricing {.heading-with-pill} () () (Workbook)**
> **Concept:** Quantum Amplitude Estimation for Financial Derivatives • **Difficulty:** ★★★★☆
> **Summary:** This chapter analyzes how Quantum Amplitude Estimation (QAE) provides a quadratic speedup over classical Monte Carlo methods for calculating the expected payoff and subsequent price of financial derivatives.

---

### **Theoretical Background**

Classical Monte Carlo methods are a cornerstone of financial engineering, used to estimate the expected payoff of derivatives by averaging outcomes from numerous random simulations. If we want to find the expected value $\mathbb{E}[f(x)]$ of a payoff function $f(x)$ over a random variable $x$, we can approximate it by drawing $N$ samples:

$$
\mathbb{E}[f(x)] \approx \frac{1}{N} \sum_{i=1}^{N} f(x_i)
$$

According to the Central Limit Theorem, the error of this estimation scales as $\mathcal{O}(1/\sqrt{N})$. To improve precision by a factor of 10, one must increase the number of samples by a factor of 100.

**Quantum Amplitude Estimation (QAE)** offers a powerful alternative. It reframes the problem as estimating an amplitude in a quantum state. By encoding the expected value into an amplitude, QAE can achieve an estimation error that scales as $\mathcal{O}(1/M)$, where $M$ is the number of quantum queries. This provides a **quadratic speedup** over its classical counterpart.

The QAE framework for option pricing involves several key steps:
1.  **State Preparation:** A quantum state $|\psi\rangle$ is prepared to encode the probability distribution of the underlying random variable (e.g., the stock's terminal price, $S_T$).
```
$$
|\psi\rangle = \sum_{x} \sqrt{p(x)} |x\rangle
$$
```
2.  **Payoff Encoding:** A controlled rotation operator, $R_f$, encodes the payoff function $f(x)$ into the amplitude of an ancilla qubit.
```
$$
R_f |x\rangle|0\rangle = |x\rangle \left( \sqrt{1 - f(x)} |0\rangle + \sqrt{f(x)} |1\rangle \right)
$$
```
3.  **Amplitude Estimation:** QAE is applied to estimate the probability of measuring the ancilla qubit in the $|1\rangle$ state, which corresponds to the expected payoff $\mathbb{E}[f(x)]$.
4.  **Discounting:** The final option price is obtained by multiplying the expected payoff by the classical discount factor $e^{-rT}$, where $r$ is the risk-free rate and $T$ is the time to maturity.

Despite its power, QAE faces challenges, such as the complexity of preparing the initial state $|\psi\rangle$ for arbitrary distributions and the large circuit depth required for the Grover-like iterations within QAE. Variants like **Iterative QAE (IQAE)** have been developed to mitigate these issues by adaptively estimating the amplitude without requiring deep circuits.

---

### **Comprehension Check**

!!! note "Quiz"
```
**1. If a classical Monte Carlo simulation requires $N$ samples to achieve precision $\epsilon$, how does the precision error $\epsilon$ scale with the number of samples $N$?**

- A. $\mathcal{O}(N)$
- B. $\mathcal{O}(1/N)$
- C. $\mathcal{O}(1/\sqrt{N})$
- D. $\mathcal{O}(1/N^2)$

??? info "See Answer"
    **Correct: C**

```
---

!!! note "Quiz"
```
**2. The primary quantum algorithm used to achieve a quadratic speedup in Monte Carlo simulations is:**

- A. Quantum Phase Estimation (QPE)
- B. Shor's Factoring Algorithm
- C. Quantum Amplitude Estimation (QAE)
- D. Variational Quantum Eigensolver (VQE)

??? info "See Answer"
    **Correct: C**

```
---

!!! note "Quiz"
```
**3. After calculating the expected payoff $\mathbb{E}[\max(S_T - K, 0)]$ using QAE, what final classical step is required to determine the option's current price $V$?**

- A. Applying the maximum function
- B. Multiplying by the discount factor $e^{-rT}$
- C. Adding the strike price $K$
- D. Dividing by the risk-free rate $r$

??? info "See Answer"
    **Correct: B**

```
---

!!! note "Quiz"
```
**4. The non-linear nature of the payoff function $f(x) = \max(x - K, 0)$ is typically handled in quantum circuits by:**

- A. Using only the Iterative QAE (IQAE) variant
- B. Approximating $f(x)$ using piecewise-linear or polynomial functions
- C. Applying a CNOT gate to the payoff register
- D. Using the Bravyi-Kitaev transformation

??? info "See Answer"
    **Correct: B**

```
---

!!! abstract "Interview-Style Question"
```
**Q:** Quantify the performance difference between classical Monte Carlo and Quantum Amplitude Estimation (QAE) in terms of computational complexity, assuming both are seeking the same accuracy $\epsilon$.

???+ info "Answer Strategy"
    The performance difference is a **quadratic speedup** in favor of the quantum approach. This can be quantified by analyzing how the required number of computational steps scales with the desired accuracy, $\epsilon$.

    1.  **Classical Monte Carlo:**
        *   **Error Scaling:** The error of a classical Monte Carlo simulation decreases with the number of samples $N$ as $\mathcal{O}(1/\sqrt{N})$.
        *   **Complexity:** To achieve a target accuracy $\epsilon$, we need the error to be at most $\epsilon$. Therefore, $1/\sqrt{N} \approx \epsilon$, which means the required number of samples $N$ scales as $\mathcal{O}(1/\epsilon^2)$.

    2.  **Quantum Amplitude Estimation (QAE):**
        *   **Error Scaling:** The error of QAE decreases with the number of quantum queries $M$ as $\mathcal{O}(1/M)$.
        *   **Complexity:** To achieve the same accuracy $\epsilon$, we need $1/M \approx \epsilon$, which means the required number of queries $M$ scales as $\mathcal{O}(1/\epsilon)$.

    **Conclusion:**
    To get 10x more accuracy (decreasing $\epsilon$ by a factor of 10), the classical method requires 100x more work, while the quantum method requires only 10x more work. This quadratic difference in scaling ($1/\epsilon^2$ vs. $1/\epsilon$) is the source of the quantum advantage.

```
---

### **<i class="fa-solid fa-flask"></i> Hands-On Project**

#### **Project:** Classical vs. Quantum Sample Scaling

---

#### **Project Blueprint**

| **Section**              | **Description**                                                                                                                                                                                                                         |
| ------------------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Objective**            | To quantify and compare the number of samples/queries required for classical Monte Carlo and Quantum Amplitude Estimation (QAE) to achieve a target pricing precision $\epsilon$.                                                      |
| **Mathematical Concept** | Classical error scaling: $\epsilon \propto 1/\sqrt{N}$, so $N \propto 1/\epsilon^2$. Quantum error scaling: $\epsilon \propto 1/M$, so $M \propto 1/\epsilon$. The speedup is the ratio $N/M$.                                             |
| **Experiment Setup**     | A financial institution requires a pricing accuracy of $\epsilon = 10^{-3}$ (0.1%). We will calculate the resources needed for both classical and quantum methods.                                                                       |
| **Process Steps**        | 1. Define the target precision $\epsilon = 10^{-3}$.<br>2. Calculate the number of classical samples $N$ needed.<br>3. Calculate the number of quantum queries $M$ needed.<br>4. Compute the speedup factor $N/M$.                        |
| **Expected Behavior**    | The number of classical samples $N$ should be significantly larger than the number of quantum queries $M$, demonstrating the quadratic advantage of the quantum algorithm.                                                              |
| **Tracking Variables**   | - $\epsilon$: Target precision<br>- $N$: Number of classical samples<br>- $M$: Number of quantum queries<br>- `SpeedupFactor`: The ratio $N/M$                                                                                             |
| **Verification Goal**    | Confirm that for $\epsilon = 10^{-3}$, $N = 1,000,000$ and $M = 1,000$, yielding a speedup of 1,000x.                                                                                                                                     |
| **Output**               | Print the calculated values for $N$, $M$, and the resulting speedup factor.                                                                                                                                                             |

---

#### **Outcome and Interpretation**

The results clearly demonstrate the power of quantum computation for this problem. To achieve a pricing accuracy of 0.1%, a classical Monte Carlo simulation requires one million samples. In contrast, QAE requires only one thousand queries to the quantum computer. This represents a **1,000x speedup**, making calculations that might be prohibitively expensive classically far more tractable on future quantum hardware. This quadratic advantage is a defining feature of quantum algorithms in finance.