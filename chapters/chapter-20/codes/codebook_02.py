"""Ch-20 Project 2: Bit-flip vs phase-flip code syndrome bar chart.
Saves: docs/chapters/chapter-20/codes/ch20_syndrome_results.png
"""
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator

codes_dir = Path('docs/chapters/chapter-20/codes')
codes_dir.mkdir(parents=True, exist_ok=True)
sim = AerSimulator()

def bitflip_code(err_q=None):
    qc = QuantumCircuit(5, 2)
    qc.cx(0,1); qc.cx(0,2)
    if err_q is not None: qc.x(err_q)
    qc.cx(0,3); qc.cx(1,3); qc.cx(1,4); qc.cx(2,4)
    qc.measure([3,4],[0,1]); return qc

def phaseflip_code(err_q=None):
    qc = QuantumCircuit(5, 2)
    qc.h([0,1,2]); qc.cx(0,1); qc.cx(0,2)
    if err_q is not None: qc.z(err_q)
    qc.cx(0,3); qc.cx(1,3); qc.cx(1,4); qc.cx(2,4)
    qc.h([0,1,2]); qc.measure([3,4],[0,1]); return qc

scenarios = {
    'BF no err':  (bitflip_code,   None),
    'BF q0 err':  (bitflip_code,   0),
    'BF q1 err':  (bitflip_code,   1),
    'BF q2 err':  (bitflip_code,   2),
    'PF no err':  (phaseflip_code, None),
    'PF q0 err':  (phaseflip_code, 0),
    'PF q1 err':  (phaseflip_code, 1),
    'PF q2 err':  (phaseflip_code, 2),
}

correct_detected = []
for label, (code_fn, err) in scenarios.items():
    qc = code_fn(err); tc = transpile(qc, sim, optimization_level=0)
    counts = sim.run(tc, shots=1024).result().get_counts()
    top = max(counts, key=counts.get)
    detected = top != '00'
    expected = (err is not None)
    correct_detected.append(1 if detected == expected else 0)

x = np.arange(len(scenarios))
colors = ['steelblue' if c else 'tomato' for c in correct_detected]

fig, ax = plt.subplots(figsize=(11, 4.5))
ax.bar(x, correct_detected, color=colors)
ax.set_xticks(x); ax.set_xticklabels(list(scenarios.keys()), rotation=35, ha='right')
ax.set_ylabel('Correct detection (1=yes, 0=no)')
ax.set_title('Chapter 20: Bit-flip / Phase-flip Syndrome Detection Results')
ax.set_ylim(-0.1, 1.2)
ax.axhline(1, color='green', linestyle='--', linewidth=0.8, alpha=0.5)
plt.tight_layout()
out = codes_dir / 'ch20_syndrome_results.png'
fig.savefig(out, dpi=160, bbox_inches='tight'); plt.close(fig)
print(f"Saved figure to: {out}")
print(f"Overall correct detection rate: {sum(correct_detected)/len(correct_detected):.0%}")
