"""Ch-16 Project 3: Zero-noise extrapolation (ZNE)."""
import numpy as np
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
from qiskit_aer.noise import NoiseModel, depolarizing_error
from qiskit.quantum_info import SparsePauliOp, Statevector

sim = AerSimulator()
H_obs = SparsePauliOp('ZZ').to_matrix()

qc = QuantumCircuit(2); qc.h(0); qc.cx(0,1)
sv_ideal = Statevector(qc)
E_ideal  = float(np.real(sv_ideal.data.conj() @ H_obs @ sv_ideal.data))

base_p = 0.02
scale_factors = [1, 2, 3, 4]

def noisy_expectation(scale):
    p = base_p * scale
    nm = NoiseModel()
    nm.add_all_qubit_quantum_error(depolarizing_error(p, 2), ['cx'])
    qc2 = qc.copy(); qc2.save_density_matrix()
    tc  = transpile(qc2, sim, optimization_level=0)
    rho = sim.run(tc, noise_model=nm).result().data()['density_matrix'].data
    return float(np.real(np.trace(H_obs @ rho)))

noisy_vals = [noisy_expectation(s) for s in scale_factors]

# Richardson extrapolation: fit quadratic, evaluate at scale=0
coeffs = np.polyfit(scale_factors, noisy_vals, deg=2)
E_zne  = np.polyval(coeffs, 0)

print(f"Ideal <ZZ>:        {E_ideal:.6f}")
print(f"Noisy (scale=1):   {noisy_vals[0]:.6f}")
print(f"ZNE extrapolated:  {E_zne:.6f}")
print(f"ZNE error:         {abs(E_zne-E_ideal):.6f}")
print(f"Naive error:       {abs(noisy_vals[0]-E_ideal):.6f}")
