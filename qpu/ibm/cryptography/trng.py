from typing import Dict, List

from qiskit import IBMQ, Aer, QuantumCircuit, assemble, execute, transpile
from qiskit.providers.ibmq import IBMQBackend
from qiskit.providers.ibmq.exceptions import IBMQAccountCredentialsNotFound  # , IBMQAccountError
from qiskit.result.result import Result
from qiskit.visualization import plot_histogram

SortedBackendList = List[IBMQBackend]


def generate(bits: int = 5) -> QuantumCircuit:
    # Create a Quantum Circuit acting on the q register
    circuit = QuantumCircuit(bits, bits)

    # Add a H gate on qubit i (50/50 chance)
    for i in range(bits):
        circuit.h(i)

    # Map the quantum measurement to the classical bits
    circuit.measure(range(bits), range(bits))
    return circuit


def simulate(circuit: QuantumCircuit, steps: int = 8000) -> Result:
    # Use Aer's qasm_simulator
    simulator = Aer.get_backend('qasm_simulator')

    # Execute the circuit on the qasm simulator
    job = execute(circuit, simulator, shots=steps)

    # Grab and return results from the job
    return job.result()


def _get_qpu_candidates(backends: List[IBMQBackend], circuit: QuantumCircuit) -> SortedBackendList:
    qpus = {}

    # Get all backends that we can execute
    for i, backend in enumerate(backends):
        # Is it a simulator?
        if 'simulator' in backend.name():
            continue

        # Enough qubits?
        if len(backend.properties().qubits) < circuit.n_qubits:
            continue

        # Enough remaining jobs?
        if backend.remaining_jobs_count() == 0:
            continue

        # TODO: Is the required entanglement available?

        qpus[i] = backend.status().pending_jobs

    sorted_qpus = sorted(qpus.items(), key=lambda item: item[1])
    return [backends[qpuinfo[0]] for qpuinfo in sorted_qpus]


def _run(backend: IBMQBackend, circuit: QuantumCircuit) -> Result:
    qobj = assemble(transpile(circuit, backend=backend), backend=backend)
    # TODO: configure amount of steps
    job = backend.run(qobj)
    return backend.retrieve_job(job.job_id()).result()


# TODO: Convert to async function
def run(circuit: QuantumCircuit, api_key: str = None, steps: int = 1) -> Result:
    # TODO: Think about moving the api_key to __init__ after converting this to a class
    # Use stored or supplied token
    try:
        IBMQ.disable_account()
    except IBMQAccountCredentialsNotFound:
        pass

    if api_key is None:
        provider = IBMQ.load_account()
    else:
        provider = IBMQ.enable_account(api_key)

    # TODO: fetch backends in __init__ (add refresh timer)
    # Fetch backends and find available qpu with enough qubits and least load
    backends = provider.backends()
    # Fetch qpus with least load and try it
    candidates = _get_qpu_candidates(backends, circuit)

    if len(candidates) == 0:
        raise RuntimeError('No matching qpu found (either no jobs available or unmappable circuit)')

    for backend in _get_qpu_candidates(backends, circuit):
        try:
            # Create qobj and run it on qpu
            result = _run(backend, circuit)
            break
        except Exception:
            # Something failed, try the next qpu
            continue

        # no qpu found that works :(
        raise RuntimeError('No qpu available that can handle the circuit')

    # Disable account
    IBMQ.disable_account()
    return result


def getCircuitAscii(circuit: QuantumCircuit) -> str:
    # Draw the circuit
    return circuit.draw()


def getResult(circuit: QuantumCircuit, result: Result) -> Dict[str, int]:
    return result.get_counts(circuit)


def plotResult(circuit: QuantumCircuit, result: Result) -> None:
    plot_histogram(result.get_counts(circuit), bar_labels=False).show()
