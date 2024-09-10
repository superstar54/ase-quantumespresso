import os
import warnings
from ase.calculators.genericfileio import GenericFileIOCalculator
from ase.calculators.espresso import EspressoTemplate, EspressoProfile
from ase.io import write
from ase.io.espresso import Namelist

compatibility_msg = (
    "Espresso calculator is being restructured.  Please use e.g. "
    "Espresso(profile=EspressoProfile(argv=['mpiexec', 'pw.x'])) "
    "to customize command-line arguments."
)

__all__ = ["Espresso", "PwTemplate", "EspressoProfile"]


class PwTemplate(EspressoTemplate):
    def execute(self, directory, profile):
        """Do not raise an exception if the calculation fails."""
        try:
            profile.run(
                directory, self.inputname, self.outputname, errorfile=self.errorname
            )
        except Exception as e:
            print(
                f"The calculation failed with the following error: {e}. The results can not be trusted."
            )

    def write_input(self, profile, directory, atoms, parameters, properties):
        """Override the write_input method to support:
        - DFT+U
        """
        self.directory = directory
        self.atoms = atoms
        self.parameters = parameters
        self.properties = properties

        dst = directory / self.inputname

        input_data = Namelist(parameters.pop("input_data", None))
        input_data.to_nested("pw")
        input_data["control"].setdefault("pseudo_dir", str(profile.pseudo_dir))
        parameters["input_data"] = input_data
        # handle DFT+U
        additional_cards = parameters.pop("additional_cards", [])
        if "hubbard_u" in atoms.info:
            additional_cards.append(atoms.info["hubbard_u"])

        write(
            dst,
            atoms,
            format="espresso-in",
            properties=properties,
            additional_cards=additional_cards,
            **parameters,
        )

    def read_results(self, directory):
        """Override to set energy to None if not present."""
        from .parsers import PwParser

        parser = PwParser(self.directory, self.outputname, self.atoms, self.parameters)
        exit_code = parser.parse()

        results = parser.results
        results["exit_code"] = exit_code
        results.setdefault("energy", results["output_parameters"].get("energy", None))
        results["atoms"] = results.get("output_structure", None)
        return results


class Espresso(GenericFileIOCalculator):
    def __init__(
        self,
        *,
        profile=None,
        command=GenericFileIOCalculator._deprecated,
        label=GenericFileIOCalculator._deprecated,
        directory=".",
        template=PwTemplate(),
        **kwargs,
    ):
        """
        All options for pw.x are copied verbatim to the input file, and put
        into the correct section. Use ``input_data`` for parameters that are
        already in a dict.

        input_data: dict
            A flat or nested dictionary with input parameters for pw.x
        pseudopotentials: dict
            A filename for each atomic species, e.g.
            ``{'O': 'O.pbe-rrkjus.UPF', 'H': 'H.pbe-rrkjus.UPF'}``.
            A dummy name will be used if none are given.
        kspacing: float
            Generate a grid of k-points with this as the minimum distance,
            in A^-1 between them in reciprocal space. If set to None, kpts
            will be used instead.
        kpts: (int, int, int), dict, or BandPath
            If kpts is a tuple (or list) of 3 integers, it is interpreted
            as the dimensions of a Monkhorst-Pack grid.
            If ``kpts`` is set to ``None``, only the Γ-point will be included
            and QE will use routines optimized for Γ-point-only calculations.
            Compared to Γ-point-only calculations without this optimization
            (i.e. with ``kpts=(1, 1, 1)``), the memory and CPU requirements
            are typically reduced by half.
            If kpts is a dict, it will either be interpreted as a path
            in the Brillouin zone (*) if it contains the 'path' keyword,
            otherwise it is converted to a Monkhorst-Pack grid (**).
            (*) see ase.dft.kpoints.bandpath
            (**) see ase.calculators.calculator.kpts2sizeandoffsets
        koffset: (int, int, int)
            Offset of kpoints in each direction. Must be 0 (no offset) or
            1 (half grid offset). Setting to True is equivalent to (1, 1, 1).

        """

        if command is not self._deprecated:
            raise RuntimeError(compatibility_msg)

        if label is not self._deprecated:
            warnings.warn("Ignoring label, please use directory instead", FutureWarning)

        if "ASE_ESPRESSO_COMMAND" in os.environ and profile is None:
            warnings.warn(compatibility_msg, FutureWarning)

        super().__init__(
            profile=profile,
            template=template,
            directory=directory,
            parameters=kwargs,
        )

    def get_property(self, name, atoms=None, **kwargs):
        from ase import Atoms

        if atoms is None:
            atoms = Atoms()
        return super().get_property(name, atoms=atoms, **kwargs)
