from .namelist import NamelistTemplate


class DosTemplate(NamelistTemplate):
    _label = "dos"
    outputname = "dos.doso"

    def __init__(self):
        super().__init__(
            [
                "dos",
            ]
        )

    def read_results(self, directory):
        from .parsers.dos import DosParser

        parser = DosParser(directory, self.outputname)
        exit_code = parser.parse()
        results = parser.results
        results["exit_code"] = exit_code
        return results
