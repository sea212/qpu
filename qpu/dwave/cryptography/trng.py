from collections import OrderedDict
from typing import Dict

from dimod import BinaryQuadraticModel
from dimod.sampleset import SampleSet
from neal import SimulatedAnnealingSampler


def generate(bits: int = 3) -> BinaryQuadraticModel:
    # Create "TRNG" BQM
    return BinaryQuadraticModel({'b{}'.format(i): 0.0 for i in range(bits)}, {}, 'BINARY')


def simulate(model: BinaryQuadraticModel, steps: int = 8000) -> SampleSet:
    # Use simulated annealing sampler
    simulator = SimulatedAnnealingSampler()

    # Execute the BQM on the simulated annealing sampler
    return simulator.sample(model, num_reads=steps)


def run(model: BinaryQuadraticModel, steps: int = 8000, api_key: str = None) -> SampleSet:
    raise NotImplementedError()


'''
def getCircuitAscii(circuit: QuantumCircuit) -> str:
    # Draw the circuit
    return circuit.draw()
'''


def getResult(result: SampleSet) -> Dict[str, int]:
    newres = {}

    for res in result:
        # Create binary representation from result dictionary
        res = ''.join([str(i) for i in list(res.values())])

        # Add or count up occurences of a specific result
        if res in newres:
            newres[res] += 1
        else:
            newres[res] = 1

    return OrderedDict(sorted(newres.items()))


def plotResult(model: BinaryQuadraticModel, result: SampleSet) -> None:
    raise NotImplementedError()
