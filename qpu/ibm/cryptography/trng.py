from typing import Dict

from qiskit import Aer, QuantumCircuit, execute
from qiskit.result.result import Result
from qiskit.visualization import plot_histogram


def generate(bits: int = 5) -> QuantumCircuit:
    # Create a Quantum Circuit acting on the q register
    circuit = QuantumCircuit(bits, bits)

    # Add a H gate on qubit i (50/50 chance)
    for i in range(bits):
        circuit.h(i)

    # Map the quantum measurement to the classical bits
    circuit.measure(range(bits), range(bits))
    return circuit


def simulate(circuit: QuantumCircuit, steps: int = 3200) -> Result:
    # Use Aer's qasm_simulator
    simulator = Aer.get_backend('qasm_simulator')

    # Execute the circuit on the qasm simulator
    job = execute(circuit, simulator, shots=steps)

    # Grab and return results from the job
    return job.result()


def getCircuitAscii(circuit: QuantumCircuit) -> str:
    # Draw the circuit
    return circuit.draw()


def getResult(circuit: QuantumCircuit, result: Result) -> Dict[str, int]:
    return result.get_counts(circuit)


def plotResult(circuit: QuantumCircuit, result: Result) -> None:
    plot_histogram(result.get_counts(circuit), bar_labels=False).show()
