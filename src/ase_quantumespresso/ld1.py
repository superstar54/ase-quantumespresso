from .namelist import NamelistTemplate
import re

class Ld1Template(NamelistTemplate):
    _label = "ld1"

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
        path = directory / "ld1.ld1o"
        with open(path, "r") as f:
            energy_data = parse_energy_totals(f.read())
        
        return {"ld1": energy_data}



def parse_energy_totals(text):
    # Pattern to find Etot and Etotps lines and capture relevant parts
    etot_pattern = r"Etot\s+=\s+([-\d\.]+)\s+Ry,\s+([-\d\.]+)\s+Ha,\s+([-\d\.]+)\s+eV"
    etotps_pattern = r"Etotps\s+=\s+([-\d\.]+)\s+Ry,\s+([-\d\.]+)\s+Ha,\s+([-\d\.]+)\s+eV"
    
    # Search for patterns and extract values
    etot_match = re.search(etot_pattern, text)
    etotps_match = re.search(etotps_pattern, text)
    
    # Structured data
    energy_data = {}
    
    if etot_match:
        energy_data['Etot'] = {
            'Ry': float(etot_match.group(1)),
            'Ha': float(etot_match.group(2)),
            'eV': float(etot_match.group(3))
        }
    
    if etotps_match:
        energy_data['Etotps'] = {
            'Ry': float(etotps_match.group(1)),
            'Ha': float(etotps_match.group(2)),
            'eV': float(etotps_match.group(3))
        }
    
    return energy_data