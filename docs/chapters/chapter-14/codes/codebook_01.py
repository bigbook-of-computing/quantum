"""Ch-14 Project 1: QUBO MaxCut formulation and brute-force."""
import numpy as np
from itertools import product

# 4-node graph
edges = [(0,1,1.0),(1,2,1.0),(2,3,1.0),(0,3,1.0),(0,2,0.5)]
n = 4

def cut_value(bitstr):
    return sum(w for i,j,w in edges if bitstr[i]!=bitstr[j])

best_cut, best_bits = 0, None
results = []
for bits in product([0,1], repeat=n):
    c = cut_value(bits)
    results.append((bits, c))
    if c > best_cut: best_cut = c; best_bits = bits

results.sort(key=lambda x: -x[1])
print(f"MaxCut brute-force: best={best_cut}  bitstring={best_bits}")
print("\nTop-5 cut values:")
for bits, c in results[:5]:
    print(f"  {''.join(map(str,bits))}  cut={c:.1f}")
