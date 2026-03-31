# **Chapter 18: Quantum Finance**

---

# **Introduction**

Finance is one of the most computationally demanding application domains in industry: pricing derivative securities, estimating portfolio risk, and solving combinatorial portfolio optimisation problems all require repeated evaluation of high-dimensional expectations and integrals. Classical Monte Carlo methods — the workhorses of quantitative finance — converge with a statistical error that decreases as $O(1/\sqrt{N_{\text{samples}}})$, requiring millions of samples for high accuracy. **Quantum Monte Carlo**, leveraging the power of **Quantum Amplitude Estimation (QAE)**, offers a quadratic speedup in sample complexity: the same accuracy is achievable with $O(1/\epsilon)$ quantum circuit evaluations instead of $O(1/\epsilon^2)$ classical samples.

This chapter develops the quantum financial toolkit. We begin with **quantum distribution loading** — encoding classical probability distributions into quantum state amplitudes as the necessary first step for any financial quantum algorithm. We then analyse **Quantum Amplitude Estimation (QAE)** and its application to option pricing, demonstrating the theoretical quadratic speedup. We close with portfolio optimisation and risk estimation via **Conditional Value at Risk (CVaR)**, connecting quantum finance to the variational algorithms studied in earlier chapters. Together, these techniques define the near-term quantum advantage roadmap for quantitative finance [1, 2].

---

# **Chapter 18: Outline**

| **Sec.** | **Title** | **Core Ideas & Examples** |
| :--- | :--- | :--- |
| **18.1** | Quantum Monte Carlo for Option Pricing | Distribution loading, amplitude encoding, European call payoff circuits |
| **18.2** | Quantum Amplitude Estimation | QPE-based QAE, Grover iteration, quadratic speedup, iterative QAE |
| **18.3** | Portfolio Risk and CVaR Estimation | Multi-asset models, CVaR proxy, quantum optimisation connections |

---

## **18.1 Quantum Monte Carlo for Option Pricing**

---

Classical Monte Carlo option pricing samples paths of the underlying asset's stochastic differential equation (e.g., Black-Scholes GBM), computes the payoff for each path, and averages. Quantum Monte Carlo replaces the random sampling with a **coherent quantum superposition** of all paths simultaneously, achieving the expectation value in a single quantum circuit evaluation (up to readout noise).

### **Distribution Loading**

---

The first step is encoding a classical probability distribution $\{p_i\}$ into quantum amplitudes:

$$
|\psi_{\text{dist}}\rangle = \sum_{i=0}^{2^n-1} \sqrt{p_i} |i\rangle
$$

For a **discretised Gaussian** distribution (log-normal underlying asset prices), this state is prepared using a sequence of controlled-Ry rotations:

$$
R_Y(\theta_k)|0\rangle = \cos(\theta_k/2)|0\rangle + \sin(\theta_k/2)|1\rangle, \quad \theta_k = 2\arcsin\left(\sqrt{P(S < s_k)}\right)
$$

Exact Gaussian loading on $n$ qubits requires $O(2^n)$ gates, which is too deep for NISQ. Approximate loading using **log-normal QCBMs** (quantum circuit Born machines) or Taylor-expansion circuits reduces this to $O(n \cdot \text{poly}(\log 1/\epsilon))$ gates.

!!! tip "Amplitude Encoding vs Basis Encoding"
    **Amplitude encoding** stores $N = 2^n$ values in the amplitudes of $n$ qubits — exponentially compact but exponentially expensive to prepare exactly. **Basis encoding** stores one value per qubit — easier to prepare but uses $O(N)$ qubits. For finance, amplitude encoding is preferred because the expectation value is computed naturally via measurement.
    
### **Option Payoff Encoding**

---

For a European call option with strike price $K$, the normalised payoff function $f(S) = \max(S-K, 0)/S_{\text{max}}$ is encoded on an ancilla qubit via a controlled rotation:

$$
|i\rangle|0\rangle_{\text{anc}} \xrightarrow{R_Y(2\arcsin\sqrt{f(s_i)})} |i\rangle\left(\sqrt{1-f(s_i)}|0\rangle + \sqrt{f(s_i)}|1\rangle\right)
$$

The probability of measuring $|1\rangle$ on the ancilla is then:

$$
\Pr[|1\rangle_{\text{anc}}] = \sum_i p_i f(s_i) = \mathbb{E}[f(S)] \propto \text{Option Price}
$$

Classical estimation of this probability by repeated circuit execution converges as $O(1/\sqrt{N_{\text{shots}}})$ — identical to classical Monte Carlo. The quantum advantage enters with Quantum Amplitude Estimation, described next.

!!! example "European Call Option Pricing"
    For a 4-qubit asset distribution ($2^4 = 16$ price levels from $S_{\text{min}}=0$ to $S_{\text{max}}=2$ normalised) with strike $K = 1.0$: after preparing the Gaussian state and encoding the call payoff on an ancilla, the probability of measuring ancilla = 1 gives (after rescaling) the normalised Black-Scholes option price. A 5-qubit circuit estimates this with standard error $\sigma_{\text{MC}} \approx 0.05$ using 1000 shots.
    
??? question "Why does exact amplitude loading require exponentially many gates?"
    Loading $N$ arbitrary amplitudes $\alpha_0, \ldots, \alpha_{N-1}$ into $\log_2 N$ qubits requires a unitary with $N-1$ degrees of freedom. Exactly encoding this unitary requires $O(N)$ CNOT gates (the circuit complexity lower bound for arbitrary state preparation). For a 20-qubit register ($N = 2^{20} \approx 10^6$), exact loading needs $\sim 10^6$ gates — far beyond NISQ depth limits.
    
---

## **18.2 Quantum Amplitude Estimation**

---

**Quantum Amplitude Estimation (QAE)** is the quantum algorithm that converts the distribution-loaded + payoff-encoded circuit into a precision estimator with quadratic speedup over classical Monte Carlo.

### **The Grover-Hadamard Operator**

---

Let $\mathcal{A}$ be the state preparation circuit that creates:

$$
\mathcal{A}|0\rangle = \sqrt{1-a}|\psi_0\rangle|0\rangle + \sqrt{a}|\psi_1\rangle|1\rangle
$$

where $a = \mathbb{E}[f(S)]$ is the target expectation value. The **Grover iterate** $Q = \mathcal{A}S_0\mathcal{A}^\dagger S_\chi$ alternates reflections to amplify the amplitude of $|\psi_1\rangle|1\rangle$:

$$
Q^j|\psi\rangle \quad \text{has amplitude} \quad \sin((2j+1)\theta_a) \quad \text{where} \quad \sin^2\theta_a = a
$$

After $m$ applications of $Q$, the state's "good" amplitude oscillates as $\sin((2m+1)\theta_a)$.

### **Phase Estimation for QAE**

---

Standard QAE applies **Quantum Phase Estimation (QPE)** to the Grover iterate $Q$, estimating $\theta_a$ to precision $O(1/N_Q)$ using $N_Q$ queries to $Q$:

$$
|a^* - a| \leq \frac{\pi^2}{N_Q} \sqrt{a(1-a)} + \frac{\pi^2}{N_Q^2}
$$

This provides **quadratic speedup**: classical Monte Carlo needs $N_{\text{samples}} = O(1/\epsilon^2)$ samples for error $\epsilon$; QAE needs only $N_Q = O(1/\epsilon)$ Grover iterations.

!!! tip "Iterative QAE for NISQ"
    Classical QPE-based QAE requires a deep circuit (many ancilla qubits + controlled-$Q^{2^k}$ gates). **Iterative QAE** (IQAE) achieves the same $O(1/\epsilon)$ query complexity using only single-ancilla circuits via maximum likelihood estimation over multiple short runs — compatible with current NISQ hardware.
    
!!! example "QAE for Option Pricing Speedup"
    For option pricing to 1% accuracy ($\epsilon = 0.01$):
    - Classical Monte Carlo: $N = O(1/0.01^2) = 10,000$ simulations
    - QAE: $N_Q = O(1/0.01) = 100$ Grover iterations × depth scaling = ~100× fewer oracle calls (ignoring circuit depth overhead)
    
    In practice, the quantum circuit depth overhead reduces the effective speedup for near-term NISQ devices, but fault-tolerant estimates project a 100–1000× advantage for high-accuracy pricing.
    
??? question "Does quantum speedup apply to all Monte Carlo problems, or only option pricing?"
    QAE provides quadratic speedup for any problem expressible as estimating the expectation value $\mathbb{E}[f(X)]$ where $X$ is sampled from a distribution encodable as quantum amplitudes. This includes: option pricing, risk measures (VaR, CVaR), credit default modelling, and Monte Carlo integration. It does NOT apply to problems requiring sequential path-dependent sampling where each step depends on prior outcomes.
    
---

## **18.3 Portfolio Risk and CVaR Estimation**

---

**Portfolio Risk Estimation** using quantum computing focuses on tail-risk measures — specifically **Value at Risk (VaR)** and **Conditional Value at Risk (CVaR)**, which measure financial loss at extreme quantiles.

### **Distributional Encoding for Multi-Asset Portfolios**

---

For a portfolio of $M$ assets with joint return distribution $\{(r_1, r_2, \ldots, r_M, p_{r_1 r_2 \ldots r_M})\}$, the quantum state encodes joint returns as:

$$
|\psi_{\text{portfolio}}\rangle = \sum_{\vec{r}} \sqrt{p_{\vec{r}}} |\vec{r}\rangle
$$

For a 2-asset portfolio with 4 scenarios, this requires only 2 qubits. Real portfolios with continuous returns require discretisation and quantum loading circuits.

### **Conditional Value at Risk**

---

The $\alpha$-**CVaR** (also called Expected Shortfall) is the expected loss given that the loss exceeds the $\alpha$-th quantile:

$$
\text{CVaR}_\alpha = \frac{1}{1-\alpha}\int_\alpha^1 \text{VaR}_u \, du = \mathbb{E}[L \mid L \geq \text{VaR}_\alpha]
$$

Quantum CVaR estimation uses amplitude estimation on a circuit that encodes:
1. The joint distribution of portfolio returns
2. An indicator function for the tail region ($L \geq \text{VaR}$)
3. An ancilla qubit rotated proportionally to the tail probability

```mermaid
graph LR
    A[Joint Return Distribution<br>State Preparation] --> B[VaR Threshold<br>Controlled NOT]
    B --> C[Loss Encoding<br>Ancilla Rotation]
    C --> D[Amplitude Estimation<br>CVaR ≈ a × S_max]
    D --> E[Portfolio Risk<br>Report]
```

### **Quantum Portfolio Optimisation**

---

Beyond risk estimation, **portfolio optimisation** — finding the asset weights $\vec{w}$ maximising expected return subject to risk constraints — maps naturally to a **Quadratic Unconstrained Binary Optimisation (QUBO)** problem:

$$
\min_{\vec{w}} \vec{w}^T \Sigma \vec{w} - \mu \vec{r}^T \vec{w} \quad \text{s.t.} \quad \sum_i w_i = 1, \; w_i \in \{0, 1\}
$$

This QUBO can be solved with QAOA (Chapter 6), where the cost Hamiltonian encodes the portfolio variance and the expected return penalty. For a portfolio of $M = 8$ assets with binary fractional weights, QAOA with $p=3$ layers achieves near-optimal portfolios in simulation and has been demonstrated on hardware [3].

!!! tip "Quantum Advantage Timeline for Finance"
    Near-term (NISQ): quantum speedup for CVaR estimation demonstrated on hardware at O(10)-qubit scale, but classical advantage for realistic portfolio sizes. Mid-term (logical qubits): quadratic speedup for option pricing becomes practical at ~1000 logical qubits. Long-term (fault-tolerant): full quantum advantage for large Monte Carlo problems requiring >10^6 samples.
    
!!! example "CVaR Estimation on 2-qubit Portfolio"
    2-asset, 4-scenario portfolio with returns $\{-2, -1, +1, +2\}$ and uniform probabilities. 95% CVaR = expected loss in bottom 5% = $-2$ (worst scenario). Quantum circuit: 2 distribution qubits + 1 ancilla. After amplitude estimation on the ancilla amplitude $a = P(L = -2) = 0.25$, CVaR at 75% confidence = $(-2 \times 0.25 + (-1) \times 0.25) / 0.50 = -1.5$.
    
??? question "Is quantum finance a near-term or long-term application?"
    Quantum finance sits in between. The theoretical quadratic speedup from QAE is well-established but requires fault-tolerant hardware for industrial-scale problems. Near-term NISQ demonstrations exist at the 10–50 qubit level for toy problems. Practical financial advantage requires ~1000 logical qubits to price complex derivatives (e.g., path-dependent options) faster than state-of-the-art classical GPUs running Monte Carlo.
    
---

## **References**

[1] Stamatopoulos, N., et al. (2020). *Option pricing using quantum computers*. Quantum, 4, 291.

[2] Woerner, S., & Egger, D. J. (2019). *Quantum risk analysis*. npj Quantum Information, 5(1), 15.

[3] Egger, D. J., et al. (2021). *Quantum computing for Finance: State-of-the-Art and Future Prospects*. IEEE Transactions on Quantum Engineering, 1, 1–24.