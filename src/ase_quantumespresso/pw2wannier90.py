from .namelist import NamelistTemplate


class Pw2wannier90Template(NamelistTemplate):
    _label = "pw2wannier90"

    def __init__(self):
        super().__init__(
            [
                "pw2wannier90",
            ]
        )

    def read_results(self, directory):
        return {"pw2wannier90": None}
