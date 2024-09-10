import pytest
from ase.build import bulk
import os


@pytest.fixture
def pseudopotentials():
    return {"Si": "Si.pbe-nl-rrkjus_psl.1.0.0.UPF"}


@pytest.fixture
def pseudo_dir():
    """Path to the directory containing pseudopotentials."""
    # located in the tests/datas/pseudos
    return os.path.join(os.path.dirname(__file__), "datas", "pseudos")


@pytest.fixture
def bulk_si():
    return bulk("Si")


@pytest.fixture
def pw_input_data():
    return {
        "control": {"calculation": "scf"},
        "system": {
            "ecutwfc": 30,
            "ecutrho": 200,
            "occupations": "smearing",
            "degauss": 0.01,
        },
    }


@pytest.fixture
def dos_input_data():
    return {}


@pytest.fixture
def projwfc_input_data():
    return {}
