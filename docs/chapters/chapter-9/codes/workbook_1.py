# Source: Quantum/chapter-9/workbook.md -- Block 1

    from qiskit import QuantumCircuit

    # The classical binary string
    binary_string = "1101"

    # Create a quantum circuit with a qubit for each bit
    qc = QuantumCircuit(len(binary_string))

    # Apply an X gate for each '1' in the string (from right to left)
    for i, bit in enumerate(reversed(binary_string)):
        if bit == '1':
            qc.x(i)

    # The statevector simulator can show the resulting quantum state
    from qiskit.quantum_info import Statevector
    state = Statevector(qc)
    print(f"The encoded state is: {state.draw(output='latex_source')}")
    # Output: The encoded state is: |1101>
