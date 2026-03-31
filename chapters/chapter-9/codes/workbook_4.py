# Source: Quantum/chapter-9/workbook.md -- Block 4

    from qiskit import QuantumCircuit
    from qiskit_algorithms.primitives import Fidelity

    # Define the feature map (angle encoding)
    def feature_map(x):
        qc = QuantumCircuit(1)
        qc.ry(x[0], 0)
        return qc

    # Two data points
    x_i = [1.5]
    x_j = [2.0]

    # Create the circuits for the two points
    qc_i = feature_map(x_i)
    qc_j = feature_map(x_j)

    # Use the Fidelity primitive to compute the inner product squared
    fidelity = Fidelity()
    result = fidelity.run(qc_i, qc_j).result()
    kernel_entry = result.fidelities[0]

    print(f"The kernel entry K(x_i, x_j) is: {kernel_entry:.4f}")
    # Output: The kernel entry K(x_i, x_j) is: 0.9405
