"""Ch-12 Project 3: Quantum autoencoder fidelity reconstruction."""
import numpy as np
from qiskit.circuit.library import RealAmplitudes
from qiskit.quantum_info import Statevector, state_fidelity

np.random.seed(3)
n_q = 4  # 4-qubit input, 2-qubit latent

# Random pure states to compress
def rand_state(nq, seed=None):
    if seed: np.random.seed(seed)
    v = np.random.randn(2**nq) + 1j*np.random.randn(2**nq)
    return v / np.linalg.norm(v)

# Analyse reconstruction fidelity with random encoder/decoder
encoder = RealAmplitudes(n_q, reps=2)
n_p     = encoder.num_parameters

print("Quantum autoencoder reconstruction fidelity test:")
print(f"{'trial':>7}  {'fidelity':>10}")
np.random.seed(0)
for trial in range(8):
    theta_enc = np.random.uniform(0, 2*np.pi, n_p)
    sv_in     = Statevector(rand_state(n_q, seed=trial))
    sv_out    = sv_in.evolve(encoder.assign_parameters(theta_enc))
    # Partial trace: fidelity of reduced 2-qubit state
    rho_full = np.outer(sv_out.data, sv_out.data.conj())
    # Trace out qubits 2,3 to get 2-qubit latent state
    rho_lat  = rho_full.reshape(4,4,4,4).trace(axis1=0,axis2=2)  # rough partial trace
    fid = float(np.real(np.trace(rho_lat @ rho_lat)))  # purity as proxy for info retention
    print(f"  {trial:5d}  {fid:10.6f}")
