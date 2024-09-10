# -*- coding: utf-8 -*-
"""`Parser` implementation for the `dos.x` code of Quantum ESPRESSO.

Modified from aiida-quantumespresso.parsers.dos.DosParser.
"""

from aiida_quantumespresso.utils.mapping import get_logging_container
from .exit_code import DosExitCodes
from .base import BaseParser


class DosParser(BaseParser):
    """`Parser` implementation for the `dos.x` calculation, modified from aiida-quantumespresso."""

    dos_filename = "pwscf.dos"

    def __init__(self, directory, outputname):
        """Initialize the instance of `PwParser`."""
        super().__init__(directory, output_filename=outputname)
        self.outputname = outputname
        self.exit_codes = DosExitCodes()

    def parse(self, **kwargs):
        """Parse the retrieved files of a ``DosCalculation`` into output nodes."""
        from aiida_quantumespresso.parsers.dos import parse_raw_dos

        logs = get_logging_container()

        _, parsed_stdout, logs = self.parse_stdout_from_retrieved(logs)

        base_exit_code = self.check_base_errors(logs)
        if base_exit_code:
            return self.exit(base_exit_code, logs)

        self.out("output_parameters", parsed_stdout)

        if "ERROR_OUTPUT_STDOUT_INCOMPLETE" in logs.error:
            return self.exit(self.exit_codes.ERROR_OUTPUT_STDOUT_INCOMPLETE, logs)

        # Parse the DOS
        filepath_dos = self.directory / self.dos_filename
        try:
            with open(filepath_dos, "r") as handle:
                dos_file = handle.readlines()
        except OSError:
            return self.exit(self.exit_codes.ERROR_READING_DOS_FILE, logs)

        array_names = [[], []]
        array_units = [[], []]
        array_names[0] = [
            "dos_energy",
            "dos",
            "integrated_dos",
        ]  # When spin is not displayed
        array_names[1] = [
            "dos_energy",
            "dos_spin_up",
            "dos_spin_down",
            "integrated_dos",
        ]  # When spin is displayed
        array_units[0] = ["eV", "states/eV", "states"]  # When spin is not displayed
        array_units[1] = [
            "eV",
            "states/eV",
            "states/eV",
            "states",
        ]  # When spin is displayed

        # grabs parsed data from aiida.dos
        # TODO: should I catch any QEOutputParsingError from parse_raw_dos,
        #       log an error and return an exit code?
        array_data, spin = parse_raw_dos(dos_file, array_names, array_units)

        energy_units = "eV"
        # dos_units = "states/eV"
        # int_dos_units = "states"
        xy_data = {}
        xy_data["x"] = {
            "array": array_data["dos_energy"],
            "labels": "dos_energy",
            "units": energy_units,
        }
        y_arrays = []
        y_names = []
        y_units = []
        y_arrays += [array_data["integrated_dos"]]
        y_names += ["integrated_dos"]
        y_units += ["states"]
        if spin:
            y_arrays += [array_data["dos_spin_up"]]
            y_arrays += [array_data["dos_spin_down"]]
            y_names += ["dos_spin_up"]
            y_names += ["dos_spin_down"]
            y_units += ["states/eV"] * 2
        else:
            y_arrays += [array_data["dos"]]
            y_names += ["dos"]
            y_units += ["states/eV"]
        xy_data["y"] = {"arrays": y_arrays, "labels": y_names, "units": y_units}

        self.out("dos", xy_data)

        return self.exit(logs=logs)
