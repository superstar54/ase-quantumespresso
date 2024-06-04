# ASE-QuantumESPRESSO
Extends the functionality of ASE espresso module by providing additional calculators for Quantum ESPRESSO binaries, including `pw.x`, `dos.x`, `pp.x`, and others.

## Installation

To install the ASE-QuantumESPRESSO package, you can use pip:
```bash
pip install ase-quantumespresso
```


## Workflows using `ase-quantumespresso`

Please see the [aiida-workgraph](https://workgraph-collections.readthedocs.io/en/latest/ase/espresso/index.html)


## Usage

### DFT+U

```python
atoms.info['hubbard_u'] = 'HUBBARD (ortho-atomic)', 'U Mn-3d 5.0', 'U Ni-3d 6.0'
```