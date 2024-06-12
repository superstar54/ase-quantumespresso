# ASE-QuantumESPRESSO
[![PyPI version](https://badge.fury.io/py/ase-quantumespresso.svg)](https://badge.fury.io/py/ase-quantumespresso)
[![Unit test](https://github.com/superstar54/ase-quantumespresso/actions/workflows/ci.yaml/badge.svg)](https://github.com/superstar54/ase-quantumespresso/actions/workflows/ci.yaml)
[![codecov](https://codecov.io/gh/superstar54/ase-quantumespresso/branch/main/graph/badge.svg)](https://codecov.io/gh/superstar54/ase-quantumespresso)
[![Docs status](https://readthedocs.org/projects/ase-quantumespresso/badge)](http://ase-quantumespresso.readthedocs.io/)

Extends the functionality of ASE espresso module by providing additional calculators for Quantum ESPRESSO binaries, including `pw.x`, `dos.x`, `pp.x`, and others.

## Installation

To install the ASE-QuantumESPRESSO package, you can use pip:
```bash
pip install ase-quantumespresso
```


## Workflows using `ase-quantumespresso`

Please see the [ase-quantumespresso](https://workgraph-collections.readthedocs.io/en/latest/ase/espresso/index.html)


## Usage

### DFT+U

```python
atoms.info['hubbard_u'] = 'HUBBARD (ortho-atomic)', 'U Mn-3d 5.0', 'U Ni-3d 6.0'
```
