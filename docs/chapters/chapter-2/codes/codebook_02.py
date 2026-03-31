"""Ch-2 Project 2: Pauli expectations bar chart.
Saves: docs/chapters/chapter-2/codes/ch2_pauli_expectations.png
"""
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
from qiskit.quantum_info import SparsePauliOp

codes_dir = Path('docs/chapters/chapter-2/codes')
codes_dir.mkdir(parents=True, exist_ok=True)

paulis = {p: SparsePauliOp(p).to_matrix() for p in ['X','Y','Z']}

def sv(ops):
    from qiskit import QuantumCircuit
    from qiskit.quantum_info import Statevector
    qc = QuantumCircuit(1)
    for op in ops: getattr(qc, op)(0)
    return Statevector(qc).data

states_ops = {'|0>':[], '|1>':['x'], '|+>':['h'], '|->':['h','z'], '|i>':['h','s']}
labels = list(states_ops.keys())
x = np.arange(len(labels)); width = 0.25

expectations = {p: [] for p in ['X','Y','Z']}
for ops in states_ops.values():
    s = sv(ops)
    for p, mat in paulis.items():
        expectations[p].append(float(np.real(s.conj() @ mat @ s)))

fig, ax = plt.subplots(figsize=(9, 4.5))
for i, (p, exps) in enumerate(expectations.items()):
    ax.bar(x + i*width, exps, width, label=f'<{p}>')
ax.set_xticks(x + width); ax.set_xticklabels(labels)
ax.set_ylabel('Expectation value'); ax.set_ylim(-1.1, 1.1)
ax.set_title('Chapter 2: Pauli Expectation Values')
ax.legend(); ax.grid(True, alpha=0.3, axis='y')
out = codes_dir / 'ch2_pauli_expectations.png'
fig.savefig(out, dpi=160, bbox_inches='tight'); plt.close(fig)
print(f"Saved figure to: {out}")
