# **Chapter 13: Quantum Reinforcement Learning () () (Codebook)**

Quantum Reinforcement Learning (QRL) replaces classical policy/value networks with parametric quantum circuits. This chapter builds a variational policy, approximates a Q-table with a VQC, and analyses the reward landscape geometry.

---

**Expected outputs** from `codes/codebook_02.py`:

- `codes/ch13_qtable_convergence.png`

## Project 1: Variational Quantum Policy Network

| Feature | Description |
| :--- | :--- |
| **Goal** | Train a 2-qubit `RealAmplitudes` circuit as a stochastic policy $\pi_\theta(a\vert s)$ for a 2-state / 2-action environment. |
| **Method** | REINFORCE-style update: sample action from measurement probabilities, compute return, shift parameters toward high-reward actions. |

---

### Complete Python Code

```python
import numpy as np
from qiskit import QuantumCircuit
from qiskit.circuit.library import RealAmplitudes
from qiskit.quantum_info import Statevector

# ── toy environment: 2 states, actions 0/1, goal: always take action 1 ───────

def env_reward(state, action):
    return 1.0 if action == 1 else -1.0

policy = RealAmplitudes(2, reps=1)
n_par  = len(policy.parameters)

def action_probs(theta, state_angle):
    # encode state as Ry rotation, then apply policy
    qc = QuantumCircuit(2)
    qc.ry(state_angle, 0)
    qc.compose(policy, inplace=True)
    sv    = Statevector(qc.assign_parameters(theta))
    probs = sv.probabilities()
    return probs[0] + probs[1], probs[2] + probs[3]  # p(action=0), p(action=1)

np.random.seed(5)
theta = np.random.uniform(0, 2*np.pi, n_par)
lr    = 0.1
gamma = 0.99
state_angles = [0.0, np.pi/2]  # 2 states

print("QRL Policy training:")
for episode in range(80):
    state = np.random.randint(0, 2)
    sa    = state_angles[state]
    p0, p1 = action_probs(theta, sa)
    action = np.random.choice([0, 1], p=[p0, p1])
    reward = env_reward(state, action)
    # REINFORCE: theta += lr * reward * d(log pi)/d(theta)
    for k in range(n_par):
        tp, tm = theta.copy(), theta.copy()
        tp[k] += np.pi/2; tm[k] -= np.pi/2
        dp0p, dp1p = action_probs(tp, sa)
        dp0m, dp1m = action_probs(tm, sa)
        if action == 1:
            dp1 = 0.5*(dp1p - dp1m)
            grad = dp1 / (p1 + 1e-8)
        else:
            dp0 = 0.5*(dp0p - dp0m)
            grad = dp0 / (p0 + 1e-8)
        theta[k] += lr * reward * grad
    if episode % 20 == 0:
        _, p_opt = action_probs(theta, state_angles[0])
        print(f"  Episode {episode:3d}  p(action=1 | s=0) = {p_opt:.4f}")

print(f"\nFinal p(action=1 | s=0) = {action_probs(theta, state_angles[0])[1]:.4f}")
print(f"Final p(action=1 | s=1) = {action_probs(theta, state_angles[1])[1]:.4f}")
```
**Sample Output:**
```python
QRL Policy training:
  Episode   0  p(action=1 | s=0) = 0.6903
  Episode  20  p(action=1 | s=0) = 0.9747
  Episode  40  p(action=1 | s=0) = 0.9960
  Episode  60  p(action=1 | s=0) = 0.9984

Final p(action=1 | s=0) = 0.9992
Final p(action=1 | s=1) = 0.9998
```

---

## Project 2: Quantum Q-Table Approximation

| Feature | Description |
| :--- | :--- |
| **Goal** | Approximate the Q-function $Q(s, a)$ of a 4-state / 2-action environment with a `ZZFeatureMap + RealAmplitudes` VQC. |
| **Method** | Encode (state, action) pairs as circuit inputs; minimise Bellman residual via parameter-shift gradient descent. |

---

### Complete Python Code

```python
import numpy as np
from qiskit.circuit.library import ZZFeatureMap, RealAmplitudes
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector, SparsePauliOp

fmap   = ZZFeatureMap(feature_dimension=2, reps=1)
ansatz = RealAmplitudes(2, reps=1)
vqc    = QuantumCircuit(2)
vqc.compose(fmap, inplace=True)
vqc.compose(ansatz, inplace=True)
obs_mat = SparsePauliOp.from_list([("ZI", 1.0)]).to_matrix()

# ── encode (state, action) -> 2-D vector ─────────────────────────────────────

def sa_encode(state, action, n_states=4):
    return np.array([state / n_states * np.pi, action * np.pi])

def q_value(state, action, theta):
    x  = sa_encode(state, action)
    pv = {**dict(zip(fmap.parameters, x)),
          **dict(zip(ansatz.parameters, theta))}
    sv = Statevector(vqc.assign_parameters(pv)).data
    return float(np.real(sv.conj() @ obs_mat @ sv))

# ── true Q-table (chain MDP, always go right -> +1) ─────────────────────────

Q_true = {(s, a): (1.0 if a == 1 and s < 3 else -0.5) for s in range(4) for a in range(2)}

np.random.seed(9)
theta = np.random.uniform(0, 2*np.pi, len(ansatz.parameters))

for step in range(60):
    total_loss = 0.0
    grads = np.zeros(len(ansatz.parameters))
    for s in range(4):
        for a in range(2):
            target = Q_true[(s, a)]
            qv     = q_value(s, a, theta)
            err    = qv - target
            total_loss += err**2
            for k in range(len(ansatz.parameters)):
                tp, tm = theta.copy(), theta.copy()
                tp[k] += np.pi/2; tm[k] -= np.pi/2
                dq = 0.5*(q_value(s, a, tp) - q_value(s, a, tm))
                grads[k] += 2 * err * dq
    theta -= 0.05 * grads / 8
    if step % 15 == 0:
        print(f"Step {step:3d}  MSE={total_loss/8:.5f}")

print("\nFinal Q-values vs true:")
for s in range(4):
    for a in range(2):
        print(f"  Q({s},{a}) = {q_value(s,a,theta):7.4f}  true = {Q_true[(s,a)]:.1f}")
```
**Sample Output:**
```python
Step   0  MSE=0.38753
Step  15  MSE=0.34730
Step  30  MSE=0.32649
Step  45  MSE=0.31577

Final Q-values vs true:
  Q(0,0) =  0.2786  true = -0.5
  Q(0,1) =  0.4631  true = 1.0
  Q(1,0) = -0.5403  true = -0.5
  Q(1,1) =  0.4981  true = 1.0
  Q(2,0) = -0.4146  true = -0.5
  Q(2,1) =  0.5331  true = 1.0
  Q(3,0) = -0.1783  true = -0.5
  Q(3,1) =  0.4981  true = -0.5
```

---

## Project 3: Reward Landscape Analysis

| Feature | Description |
| :--- | :--- |
| **Goal** | Scan the reward surface of the variational policy over two parameters to detect flat gradients (quantum barren plateaus) at varying circuit depths. |
| **Method** | Evaluate expected reward $\mathbb{E}_\pi[R]$ at each grid point; compute landscape variance. |

---

### Complete Python Code

```python
```python
import numpy as np
from qiskit.circuit.library import RealAmplitudes
from qiskit.quantum_info import Statevector

def expected_reward(theta, n_qubits, reps):
```
policy = RealAmplitudes(n_qubits, reps=reps)
qc     = policy.assign_parameters(theta)
sv     = Statevector(qc)
probs  = sv.probabilities()
```
```
    # reward +1 for action "first half of outcomes", -1 for "second half"
    mid    = len(probs) // 2
    return probs[:mid].sum() - probs[mid:].sum()

```python
np.random.seed(42)
grid = np.linspace(0, 2*np.pi, 18)

print("Reward landscape variance by circuit depth:")
print(f"{'Reps':>6}  {'Landscape Var':>16}  {'Flat?':>8}")
for reps in [1, 2, 3]:
```
n_par = RealAmplitudes(2, reps=reps).num_parameters
rewards = []
for t0 in grid:
    for t1 in grid:
        theta    = np.random.uniform(0, 2*np.pi, n_par)
        theta[0] = t0; theta[1] = t1
        rewards.append(expected_reward(theta, 2, reps))
var  = np.var(rewards)
flat = "maybe" if var < 0.01 else "no"
print(f"  {reps:4d}  {var:16.6f}  {flat:>8}")

```
```
## Notes For Chapter Bridge

# **Chapter 14: the agent and focuses purely on combinatorial optimisation: () () (Codebook)**

# QUBO problems, QAOA, and quantum-enhanced enumeration on binary graphs.