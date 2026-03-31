"""Ch-1 Project 2: Born rule visualisation — P(|0>) = cos^2(theta/2) vs angle.
Saves: docs/chapters/chapter-1/codes/ch1_born_rule.png
"""
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator

codes_dir = Path('docs/chapters/chapter-1/codes')
codes_dir.mkdir(parents=True, exist_ok=True)

sim    = AerSimulator()
angles = np.linspace(0, 2*np.pi, 40)
p0_sim = []
for theta in angles:
    qc = QuantumCircuit(1); qc.ry(theta, 0); qc.measure_all()
    tc = transpile(qc, sim, optimization_level=0)
    counts = sim.run(tc, shots=2048).result().get_counts()
    p0_sim.append(counts.get('0', 0) / 2048)

p0_theory = np.cos(angles / 2) ** 2

fig, ax = plt.subplots(figsize=(8, 4.5))
ax.plot(angles, p0_theory, 'b-', linewidth=2, label='Theory: cos²(θ/2)')
ax.scatter(angles, p0_sim, s=18, color='red', alpha=0.7, label='Simulation (2048 shots)')
ax.set_xlabel('Rotation angle θ (radians)')
ax.set_ylabel('P(|0⟩)')
ax.set_title("Chapter 1: Born Rule — P(|0⟩) = cos²(θ/2)")
ax.legend(); ax.grid(True, alpha=0.35)
out = codes_dir / 'ch1_born_rule.png'
fig.savefig(out, dpi=160, bbox_inches='tight')
plt.close(fig)
print(f"Saved figure to: {out}")
