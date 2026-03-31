"""Ch-7 Project 2: Gate-count reduction bar chart — before vs after transpilation.
Saves: docs/chapters/chapter-7/codes/ch7_gate_counts.png
"""
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator

codes_dir = Path('docs/chapters/chapter-7/codes')
codes_dir.mkdir(parents=True, exist_ok=True)
sim = AerSimulator()

def test_circuit(n):
    qc = QuantumCircuit(n); qc.h(range(n))
    for i in range(n-1): qc.cx(i,i+1); qc.rz(0.3,i+1)
    for i in range(n-2,-1,-1): qc.cx(i,i+1)
    qc.measure_all(); return qc

n_vals = [2,3,4,5]
raw_cx   = []
opt3_cx  = []
for n in n_vals:
    qc = test_circuit(n)
    raw_cx.append(dict(qc.count_ops()).get('cx',0))
    tc = transpile(qc, sim, basis_gates=['cx','u3'], optimization_level=3)
    opt3_cx.append(dict(tc.count_ops()).get('cx',0))

x = np.arange(len(n_vals)); w = 0.35
fig, ax = plt.subplots(figsize=(8, 4.5))
ax.bar(x-w/2, raw_cx,  w, label='Before (raw CX)', color='salmon')
ax.bar(x+w/2, opt3_cx, w, label='After (opt=3)',   color='steelblue')
ax.set_xticks(x); ax.set_xticklabels([f'{n} qubits' for n in n_vals])
ax.set_ylabel('CX gate count'); ax.set_title('Chapter 7: CX Reduction via Optimisation')
ax.legend(); ax.grid(True, alpha=0.3, axis='y')
out = codes_dir / 'ch7_gate_counts.png'
fig.savefig(out, dpi=160, bbox_inches='tight'); plt.close(fig)
print(f"Saved figure to: {out}")
