"""Ch-18 Project 3: Quantum Amplitude Estimation — option pricing proxy."""
import numpy as np
from qiskit import QuantumCircuit, transpile
from qiskit.circuit.library import QFT
from qiskit_aer import AerSimulator

# Encode payoff probability via rotation angle
# Simple European call: S=100, K=100, sigma=0.2, r=0.05, T=1
# B-S d1, d2
S, K, sigma, r, T = 100, 100, 0.2, 0.05, 1.0
d1  = (np.log(S/K) + (r + 0.5*sigma**2)*T) / (sigma*np.sqrt(T))
d2  = d1 - sigma*np.sqrt(T)
from math import erf, sqrt, exp
N   = lambda x: 0.5*(1+erf(x/sqrt(2)))
C_exact = S*N(d1) - K*exp(-r*T)*N(d2)
print(f"B-S call price: C = {C_exact:.4f}")

# QAE: encode probability p = C/(S-K*exp(-r*T)) in rotation angle
C_disc = max(0, S - K*exp(-r*T))
p_enc  = min(C_exact / (S * 1.5), 1.0)
theta_a = 2*np.arcsin(np.sqrt(p_enc))

sim = AerSimulator()
n_eval = 4   # evaluation qubits
# Amplitude Estimation circuit (simplified single-qubit A)
qc = QuantumCircuit(n_eval + 1, n_eval)
qc.ry(theta_a, n_eval)   # object qubit
qc.h(range(n_eval))      # QPE ancillae
for j in range(n_eval):
    reps = 2**j
    for _ in range(reps):
        qc.cry(2*theta_a, j, n_eval)
qc.compose(QFT(n_eval, inverse=True), qubits=range(n_eval), inplace=True)
qc.measure(range(n_eval), range(n_eval))

tc = transpile(qc, sim, optimization_level=0)
counts = sim.run(tc, shots=2048).result().get_counts()
top  = max(counts, key=counts.get)
p_est = np.sin(int(top,2)*np.pi/2**n_eval)**2
C_est = p_est * S * 1.5

print(f"QAE estimated call price:  {C_est:.4f}")
print(f"Absolute error: {abs(C_est - C_exact):.4f}")
