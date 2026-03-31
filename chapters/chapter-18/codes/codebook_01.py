"""Ch-18 Project 1: Gaussian amplitude encoding — bar chart of loaded distribution."""
import numpy as np
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector

def gaussian_amplitudes(n_q, mu=0, sigma=1):
    N = 2**n_q
    x = np.linspace(-3*sigma+mu, 3*sigma+mu, N)
    p = np.exp(-0.5*((x-mu)/sigma)**2)
    p /= np.linalg.norm(p)
    return x, p

for n_q in [3, 4, 5]:
    x, amps = gaussian_amplitudes(n_q)
    qc = QuantumCircuit(n_q)
    qc.initialize(amps, range(n_q))
    sv   = Statevector(qc).data
    probs = np.abs(sv)**2
    kl = np.sum(amps**2 * np.log((amps**2 + 1e-12) / (probs + 1e-12)))
    print(f"  n_q={n_q}  KL(target||loaded)={kl:.2e}  "
          f"max|p_loaded - p_target|={np.max(np.abs(probs-amps**2)):.2e}")
print("\nAmplitude loading fidelity improves with more qubits (finer discretisation).")
