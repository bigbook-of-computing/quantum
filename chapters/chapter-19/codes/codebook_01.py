"""Ch-19 Project 1: Fake backend noise model properties."""
from qiskit_aer.noise import NoiseModel
from qiskit_aer import AerSimulator

try:
    from qiskit_ibm_runtime.fake_provider import FakeManilaV2
    backend = FakeManilaV2()
    nm = NoiseModel.from_backend(backend)
    print("FakeManilaV2 noise model loaded:")
    print(f"  Basis gates: {nm.basis_gates}")
    print(f"  Noisy gates: {nm.noise_instructions}")
    print(f"  Num qubits: {backend.num_qubits}")
except Exception as e:
    print(f"FakeBackend unavailable ({e}); using custom noise model.")
    from qiskit_aer.noise import depolarizing_error, thermal_relaxation_error
    nm = NoiseModel()
    nm.add_all_qubit_quantum_error(depolarizing_error(0.001, 1), ['h', 'rx', 'ry', 'rz'])
    nm.add_all_qubit_quantum_error(depolarizing_error(0.01,  2), ['cx'])
    print("Custom noise model:")
    print(f"  Basis gates: {nm.basis_gates}")
    print(f"  Noisy gates: {nm.noise_instructions}")

print("\nNoise model ready for circuit simulation.")
