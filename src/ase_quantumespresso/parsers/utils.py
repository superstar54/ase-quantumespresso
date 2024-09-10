import dataclasses
from ase import Atoms
import re


@dataclasses.dataclass
class Node:
    exit_status: str = None
    exit_message: str = None
    output_filename: str = None

    def __getitem__(self, key):
        return getattr(self, key)

    def get_option(self, name):
        return getattr(self, name)


@dataclasses.dataclass
class XyData:
    x: list = None
    y: list = None


def convert_qe_to_atoms(output_dict: dict, input_atoms: Atoms = None) -> Atoms:
    """Convert the dictionary parsed from the Quantum ESPRESSO output into ``Atoms``."""

    cell_dict = output_dict["cell"]

    # Without an input structure, try to recreate the structure from the output
    if not input_atoms:

        symbols = []
        positions = []
        for kind_name, position in output_dict["atoms"]:
            symbols.append(re.sub(r"\d+", "", kind_name))
            positions.append(position)
        atoms = Atoms(
            cell=cell_dict["lattice_vectors"],
            symbols=[atom[0] for atom in output_dict["atoms"]],
            positions=[atom[1] for atom in output_dict["atoms"]],
        )

    else:
        atoms = input_atoms.copy()
        atoms.set_cell(cell_dict["lattice_vectors"])
        new_pos = [i[1] for i in cell_dict["atoms"]]
        atoms.set_positions(new_pos)
    return atoms


def convert_qe_to_kpoints(xml_dict, structure):
    """Build the output kpoints from the raw parsed data.

    :param parsed_parameters: the raw parsed data
    :return: a `KpointsData` or None
    """
    from ase.dft.kpoints import BandPath

    k_points_list = xml_dict.get("k_points", None)
    k_points_units = xml_dict.get("k_points_units", None)
    k_points_weights_list = xml_dict.get("k_points_weights", None)

    if k_points_list is None or k_points_weights_list is None:
        return None

    if k_points_units != "1 / angstrom":
        raise ValueError(
            "k-points are not expressed in reciprocal cartesian coordinates"
        )

    kpoints = BandPath(cell=structure.cell, kpts=k_points_list)
    # kpoints.set_cell_from_structure(structure)
    # kpoints.set_kpoints(k_points_list, cartesian=True, weights=k_points_weights_list)

    return kpoints
