from collections import OrderedDict
from typing import Dict

import matplotlib.pyplot as plt
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
