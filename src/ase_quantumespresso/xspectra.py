from .namelist import NamelistTemplate


class XspectraTemplate(NamelistTemplate):
    _label = "xspectra"

    def __init__(self):
        super().__init__(
            [
                "xspectra",
            ]
        )

    def write_input(self, profile, directory, atoms, parameters, properties):
        
        kpts_string = " ".join(map(str, parameters.pop("kpts"))) + " "
        koffset = parameters.pop("koffset") or [0, 0, 0]
        kpts_string += " ".join(map(str, koffset))
        additional_cards = [kpts_string]
        parameters["additional_cards"] = additional_cards
        super().write_input(profile, directory, atoms, parameters, properties)

    def read_results(self, directory):
        return {"xspectra": None}
