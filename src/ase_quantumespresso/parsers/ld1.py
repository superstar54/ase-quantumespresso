# -*- coding: utf-8 -*-
"""`Parser` implementation for the `ld1.x` code of Quantum ESPRESSO.

"""

from aiida_quantumespresso.utils.mapping import get_logging_container
from .exit_code import NamelistsExitCodes
from .base import BaseParser
import re


class Ld1Parser(BaseParser):
    """`Parser` implementation for the `dos.x` calculation, modified from aiida-quantumespresso."""

    success_string = "End of pseudopotential test"

    def __init__(self, directory, outputname):
        """Initialize the instance of `PwParser`."""
        super().__init__(directory, output_filename=outputname)
        self.outputname = outputname
        self.exit_codes = NamelistsExitCodes()

    def parse(self, **kwargs):
        """Parse the retrieved files of a ``DosCalculation`` into output nodes."""

        logs = get_logging_container()

        _, parsed_stdout, logs = self.parse_stdout_from_retrieved(logs)

        base_exit_code = self.check_base_errors(logs)
        if base_exit_code:
            return self.exit(base_exit_code, logs)

        self.out("output_parameters", parsed_stdout)

        if "ERROR_OUTPUT_STDOUT_INCOMPLETE" in logs.error:
            return self.exit(self.exit_codes.ERROR_OUTPUT_STDOUT_INCOMPLETE, logs)

        # Parse the Energy
        filepath_dos = self.directory / self.outputname
        try:
            with open(filepath_dos, "r") as handle:
                text = handle.read()
                energy_data = parse_energy_totals(text)
                self.out("ld1", energy_data)
        except OSError:
            return self.exit(self.exit_codes.ERROR_READING_DOS_FILE, logs)

        return self.exit(logs=logs)


def parse_energy_totals(text):
    # Pattern to find Etot and Etotps lines and capture relevant parts
    etot_pattern = r"Etot\s+=\s+([-\d\.]+)\s+Ry,\s+([-\d\.]+)\s+Ha,\s+([-\d\.]+)\s+eV"
    etotps_pattern = (
        r"Etotps\s+=\s+([-\d\.]+)\s+Ry,\s+([-\d\.]+)\s+Ha,\s+([-\d\.]+)\s+eV"
    )

    # Search for patterns and extract values
    etot_match = re.search(etot_pattern, text)
    etotps_match = re.search(etotps_pattern, text)

    # Structured data
    energy_data = {}

    if etot_match:
        energy_data["Etot"] = {
            "Ry": float(etot_match.group(1)),
            "Ha": float(etot_match.group(2)),
            "eV": float(etot_match.group(3)),
        }

    if etotps_match:
        energy_data["Etotps"] = {
            "Ry": float(etotps_match.group(1)),
            "Ha": float(etotps_match.group(2)),
            "eV": float(etotps_match.group(3)),
        }

    return energy_data
