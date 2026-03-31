"""Ch-9 Project 3: Encoding fidelity under depolarising noise."""
import numpy as np
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
from qiskit_aer.noise import NoiseModel, depolarizing_error
from qiskit.quantum_info import Statevector, state_fidelity

x_vals = [0.4, 0.8, 1.2]
noise_rates = [0.0, 0.01, 0.02, 0.05, 0.1]

def angle_encode(x):
    qc = QuantumCircuit(2)
    qc.ry(x, 0); qc.ry(x*1.5, 1); qc.cx(0,1)
    return qc

sim = AerSimulator()
print(f"{'x':>5}  {'noise=0':>10}  {'n=0.01':>10}  {'n=0.02':>10}  {'n=0.05':>10}  {'n=0.10':>10}")
for x in x_vals:
    qc = angle_encode(x)
    sv_ideal = Statevector(qc)
    row = [f"{x:5.1f}"]
    for rate in noise_rates:
        if rate == 0.0:
            row.append(f"{1.0:10.6f}")
        else:
            nm = NoiseModel()
            err = depolarizing_error(rate, 2)
            nm.add_all_qubit_quantum_error(err, ['cx'])
            qc_m = qc.copy(); qc_m.save_density_matrix()
            tc = transpile(qc_m, sim)
            rho = sim.run(tc, noise_model=nm).result().data()['density_matrix']
            fid = float(np.real(sv_ideal.data.conj() @ rho.data @ sv_ideal.data))
            row.append(f"{fid:10.6f}")
    print('  '.join(row))
