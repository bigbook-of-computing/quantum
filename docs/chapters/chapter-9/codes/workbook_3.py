# Source: Quantum/chapter-9/workbook.md -- Block 3

    from qiskit import QuantumCircuit
    from qiskit.quantum_info import Statevector
    import numpy as np

    # The classical vector to encode
    vector = np.array([np.pi/2, np.pi/4])

    # Create a quantum circuit with a qubit for each feature
    qc = QuantumCircuit(len(vector))

    # Apply Ry gates with the feature values as angles
    for i, angle in enumerate(vector):
        qc.ry(angle, i)

    state = Statevector(qc)
    print(f"The encoded state is: {state.draw(output='latex_source')}")
    # Output: The encoded state is: 0.653 |00> + 0.271 |01> + 0.653 |10> + 0.271 |11>
