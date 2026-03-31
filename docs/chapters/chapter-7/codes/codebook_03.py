"""Ch-7 Project 3: Custom pass manager — CX cancellation."""
from qiskit import QuantumCircuit, transpile
from qiskit.transpiler import PassManager
from qiskit.transpiler.passes import CXCancellation, Optimize1qGates

qc = QuantumCircuit(3)
qc.h(0); qc.cx(0,1); qc.cx(0,1)  # double CX cancels
qc.cx(1,2); qc.rz(0.1,1); qc.rz(0.2,1)  # two Rz merge
qc.cx(1,2); qc.h(0)
print(f"Before PM: depth={qc.depth()}  ops={dict(qc.count_ops())}")

pm = PassManager([CXCancellation(), Optimize1qGates()])
qc_opt = pm.run(qc)
print(f"After PM : depth={qc_opt.depth()}  ops={dict(qc_opt.count_ops())}")
print("\nCustom pass manager cancelled redundant CX pairs and merged 1q gates.")
