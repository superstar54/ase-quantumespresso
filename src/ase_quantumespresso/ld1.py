from .namelist import NamelistTemplate


class Ld1Template(NamelistTemplate):
    _label = "ld1"
    outputname = "ld1.ld1o"

    def __init__(self):
        super().__init__(
            [
                "ld1",
            ]
        )

    def write_input(self, profile, directory, atoms, parameters, properties):
        from ase.io.espresso_namelist.keys import ld1_keys

        # I removed the "test" key from ld1_keys, because it was causing the following error:
        # Error: reading number of pseudo wavefunctions (nwfs)
        ld1_keys.pop("test")
        pseudo_potential_test_cards = parameters.pop("pseudo_potential_test_cards")
        additional_cards = [pseudo_potential_test_cards]
        parameters["additional_cards"] = additional_cards
        super().write_input(profile, directory, atoms, parameters, properties)

    def read_results(self, directory):
        from .parsers.ld1 import Ld1Parser

        parser = Ld1Parser(directory, self.outputname)
        exit_code = parser.parse()
        results = parser.results
        results["exit_code"] = exit_code
        print("results", results)
        return results
