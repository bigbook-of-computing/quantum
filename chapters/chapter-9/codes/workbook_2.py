# Source: Quantum/chapter-9/workbook.md -- Block 2

    from qiskit import QuantumCircuit
    from qiskit.quantum_info import Statevector
    import numpy as np

    # The classical vector to encode
    vector = np.array([0.5, 0.5, 0.5, 0.5])

    # Normalize the vector (it's already normalized in this case)
    norm = np.linalg.norm(vector)
    normalized_vector = vector / norm

    # Create a quantum circuit with log2(N) qubits
    num_qubits = int(np.log2(len(normalized_vector)))
    qc = QuantumCircuit(num_qubits)

    # For this special case, applying H-gates creates the state
    for i in range(num_qubits):
        qc.h(i)

    # The initialize() method can prepare an arbitrary state
    # qc.initialize(normalized_vector, range(num_qubits))

    state = Statevector(qc)
    print(f"The encoded state is: {state.draw(output='latex_source')}")
    # Output: The encoded state is: 0.5 |00> + 0.5 |01> + 0.5 |10> + 0.5 |11>
