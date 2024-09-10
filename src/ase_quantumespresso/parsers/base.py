import logging
from .utils import Node
from aiida.engine import ExitCode
import os
from aiida_quantumespresso.parsers.base import BaseParser as AiidaBaseParser
from aiida.common import AttributeDict
from typing import Tuple

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class BaseParser(AiidaBaseParser):
    """`Parser` implementation"""

    def __init__(self, directory, output_filename=None):
        """Initialize the instance of `PwParser`."""
        self.directory = directory
        self.node = Node(output_filename=output_filename)
        self._exit_codes = None
        self.results = {}
        self.logger = logger

    @property
    def logger(self):
        return self._logger

    @logger.setter
    def logger(self, value):
        self._logger = value

    @property
    def node(self):
        return self._node

    @node.setter
    def node(self, value):
        self._node = value

    @property
    def exit_codes(self):
        """"""
        return self._exit_codes

    @exit_codes.setter
    def exit_codes(self, value):
        self._exit_codes = value

    def out(self, key, value):
        self.results[key] = value

    def exit(self, exit_code=None, logs=None):
        if exit_code is not None:
            pass
        elif self.node.exit_status is not None:
            exit_code = ExitCode(self.node.exit_status, self.node.exit_message)
        else:
            exit_code = ExitCode(0)

        return exit_code

    def parse(self, **kwargs):
        raise NotImplementedError

    def parse_stdout_from_retrieved(
        self, logs: AttributeDict
    ) -> Tuple[str, dict, AttributeDict]:
        """Read and parse the ``stdout`` content of a Quantum ESPRESSO calculation.

        :param logs: Logging container that will be updated during parsing.
        :returns: size 3 tuple: (``stdout`` content, parsed data, updated logs).
        """
        filename_stdout = self.node.get_option("output_filename")
        filepath_stdout = self.directory / filename_stdout

        if not os.path.exists(filepath_stdout):
            logs.error.append("ERROR_OUTPUT_STDOUT_MISSING")
            return "", {}, logs

        try:
            with open(filepath_stdout, "r") as handle:
                stdout = handle.read()
        except OSError as exception:
            logs.error.append("ERROR_OUTPUT_STDOUT_READ")
            logs.error.append(exception)
            return "", {}, logs

        try:
            parsed_data, logs = self._parse_stdout_base(stdout, logs)
        except Exception as exception:
            logs.error.append("ERROR_OUTPUT_STDOUT_PARSE")
            logs.error.append(exception)
            return stdout, {}, logs

        return stdout, parsed_data, logs
