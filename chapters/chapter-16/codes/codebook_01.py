"""Ch-16 Project 1: Ideal vs shot-noise TVD."""
import numpy as np
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
from qiskit.quantum_info import Statevector

sim = AerSimulator()
qc  = QuantumCircuit(3); qc.h(0); qc.cx(0,1); qc.cx(0,2)
sv  = Statevector(qc)
p_ideal = {f'{int(k):03b}': float(abs(v)**2)
           for k, v in enumerate(sv.data) if abs(v) > 1e-10}

shots_list = [64, 256, 1024, 4096, 16384]
qc_m = qc.copy(); qc_m.measure_all()
tc   = transpile(qc_m, sim, optimization_level=0)
print(f"{'shots':>8}  {'TVD':>10}")
for shots in shots_list:
    counts = sim.run(tc, shots=shots).result().get_counts()
    p_meas = {k: v/shots for k, v in counts.items()}
    tvd = 0.5*sum(abs(p_meas.get(b,0)-p_ideal.get(b,0))
                  for b in set(p_ideal)|set(p_meas))
    print(f"  {shots:6d}  {tvd:10.6f}")
print("\nTVD decreases as O(1/sqrt(shots)) — statistical convergence.")
