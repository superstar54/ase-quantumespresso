from .namelist import NamelistTemplate


class ProjwfcTemplate(NamelistTemplate):
    _label = "projwfc"

    def __init__(self):
        super().__init__(
            [
                "projections",
                "dos",
                "bands",
            ]
        )

    def read_results(self, directory):
        from .parsers.projwfc import ProjwfcParser

        parser = ProjwfcParser(directory, self.outputname)
        exit_code = parser.parse()
        results = parser.results
        results["exit_code"] = exit_code
        print("results: ", results.keys())
        return results
