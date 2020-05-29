from collections import OrderedDict
from os import environ
from typing import Dict

import matplotlib.pyplot as plt
from dimod import BINARY, BinaryQuadraticModel
from dimod.sampleset import SampleSet
from dwave.system import DWaveSampler
from neal import SimulatedAnnealingSampler

API_KEY_ENV_NAME = 'DWAVE_API_TOKEN'


def generate(bits: int = 32) -> BinaryQuadraticModel:
    # Create TRNG BQM
    return BinaryQuadraticModel({i: 0 for i in range(bits)}, {}, vartype=BINARY)


def simulate(model: BinaryQuadraticModel, steps: int = 8000) -> SampleSet:
    # Use simulated annealing sampler
    simulator = SimulatedAnnealingSampler()

    # Execute the BQM on the simulated annealing sampler
    return simulator.sample(model, num_reads=steps)


def run(model: BinaryQuadraticModel, api_key: str = None,
        config_path: str = None, steps: int = 1) -> SampleSet:
    if api_key is None and config_path is None and API_KEY_ENV_NAME not in environ:
        raise RuntimeError('No API key specified, no config specified, no API key found in env')

    args = {}

    if api_key is not None:
        args['token'] = api_key
    if config_path is not None:
        args['config_file'] = config_path

    # Get a qpu with enought qubits. Since we have no edges, the entanglements are irrelevant
    sampler = DWaveSampler(**args)
    return sampler.sample(model, num_reads=steps)


'''
def getCircuitAscii(circuit: QuantumCircuit) -> str:
    # Draw the circuit
    return circuit.draw()
'''


def getResult(result: SampleSet) -> Dict[str, int]:
    final_result = {}

    for res in result.data():
        # Create binary representation from result dictionary
        number = ''.join([str(i) for i in list(res.sample.values())])

        # Add or count up occurences of a specific result
        final_result[number] = res.num_occurrences

    return OrderedDict(sorted(final_result.items()))


def plotResult(result: SampleSet) -> None:
    ores = getResult(result)
    occurences = ores.values()
    totalocc = sum(occurences)
    occurences = [num/totalocc for num in occurences]
    fig, ax = plt.subplots()
    ax.bar(ores.keys(), occurences, width=0.4, label='Number')
    ax.set_ylabel('Probability')
    ax.set_title('Probability distribution of quantum number generator')
    ax.legend()

    plt.show()
