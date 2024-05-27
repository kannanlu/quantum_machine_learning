import cudaq
import random
from typing import List


def random_bits(length: int):
    bit_string = []
    for _ in range(length):
        bit_string.append(random.randint(0, 1))
    return bit_string


@cudaq.kernel
def oracle(register: cudaq.qview, auxillary_qubit: cudaq.qubit,
           hidden_bits: List[int]):
    for index, bit in enumerate(hidden_bits):
        if bit == 1:
            x.ctrl(register[index], auxillary_qubit)


@cudaq.kernel
def bv_decode(hidden_bits: List[int]):
    # allocate the qubits
    qubits = cudaq.qvector(len(hidden_bits))
    # allocate an extra auxillary qubit
    auxillary_qubit = cudaq.qubit()

    #prepare the auxillary qubit
    h(auxillary_qubit)
    z(auxillary_qubit)

    #put the other qubit in superposition
    h(qubits)

    #query the oracle
    oracle(qubits, auxillary_qubit, hidden_bits)

    # de-superposition
    h(qubits)

    #measure the qubits
    mz(qubits)


#############################
if __name__ == "__main__":
    qubit_count = 25
    hidden_bits = random_bits(qubit_count)
    cudaq.set_target("nvidia")
    print(cudaq.draw(bv_decode, hidden_bits))
    result = cudaq.sample(bv_decode, hidden_bits)
    print(f"encoded bit string = {hidden_bits}")
    print(f"measured bit string = {result.most_probable()}")
    print(
        f"successful? {''.join([str(i) for i in hidden_bits]) == result.most_probable()}"
    )
