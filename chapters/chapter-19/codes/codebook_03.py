"""Ch-19 Project 3: Transpilation SWAP overhead on heavy-hex topology."""
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator

try:
    from qiskit_ibm_runtime.fake_provider import FakeManilaV2
    backend = FakeManilaV2()
    has_real = True
except Exception:
    backend = AerSimulator()
    has_real = False

circuits = {}
# All-to-all QFT (n=4)
from qiskit.circuit.library import QFT
circuits['QFT(4)'] = QFT(4)

# Random layered circuit
qc = QuantumCircuit(4)
qc.h(range(4))
for i in range(3): qc.cx(i, i+1)
qc.cx(0,3)   # non-adjacent edge
qc.rz(0.5, range(4))
circuits['Custom_4q'] = qc

sim = AerSimulator()
print(f"{'Circuit':16}  {'raw_depth':>10}  {'depth(opt0)':>12}  {'depth(opt3)':>12}  {'SWAP_count':>11}")
for name, circ in circuits.items():
    raw_d = circ.depth()
    tc0 = transpile(circ, sim, basis_gates=['cx','u3'], optimization_level=0)
    tc3 = transpile(circ, sim, basis_gates=['cx','u3'], optimization_level=3)
    swaps = dict(tc3.count_ops()).get('swap', 0)
    print(f"  {name:16s}  {raw_d:10d}  {tc0.depth():12d}  {tc3.depth():12d}  {swaps:11d}")
