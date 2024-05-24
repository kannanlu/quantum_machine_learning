import sys
import cudaq
import timeit
from cudaq import spin


@cudaq.kernel
def ghz_ciruit_m(n: int) -> None:
    """generate the Greenberger-Horne-Zeilinger state

    Args:
        n (int): the number qubits.
    """
    # allocate n qubits
    qstate = cudaq.qvector(n)
    # place the first qubit in superposition state
    h(qstate[0])
    # loop over all qubit and apply CNOT between successive two
    for jj in range(n - 1):
        x.ctrl(qstate[jj], qstate[jj + 1])
    #measure z of the qubits
    mz(qstate)
    return


@cudaq.kernel
def ghz_ciruit():
    """generate the Greenberger-Horne-Zeilinger state

    Args:
        n (int): the number qubits.
    """
    # allocate n qubits
    n = 2
    qstate = cudaq.qvector(n)
    # place the first qubit in superposition state
    h(qstate[0])
    # loop over all qubit and apply CNOT between successive two
    for jj in range(n - 1):
        x.ctrl(qstate[jj], qstate[jj + 1])


@cudaq.kernel
def param_gate(theta: float):
    """circuit with parametrized gate

    Args:
        theta (float): parametrized Ry gate
    """
    q = cudaq.qvector(2)
    x(q[0])
    ry(theta, q[1])
    x.ctrl(q[1], q[0])


@cudaq.kernel
def param_q(n: int):
    q = cudaq.qvector(n)
    h(q[0])
    for jj in range(n - 1):
        x.ctrl(q[jj], q[jj + 1])


#############################
if __name__ == "__main__":
    operator = 5.907 - 2.1433 * spin.x(0) * spin.x(1) - 2.1433 * spin.y(
        0) * spin.y(1) + 0.21829 * spin.z(0) - 6.0125 * spin.z(1)
    energy = cudaq.observe(param_q, operator, 2).expectation()
    print(energy)
