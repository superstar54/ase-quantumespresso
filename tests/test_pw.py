from ase_quantumespresso.espresso import Espresso, EspressoProfile


def test_pw(bulk_si, pseudopotentials, pseudo_dir, pw_input_data):
    profile = EspressoProfile(command="pw.x", pseudo_dir=pseudo_dir)
    calc = Espresso(
        directory="calculatioin",
        profile=profile,
        pseudopotentials=pseudopotentials,
        input_data=pw_input_data,
        kpts=[1, 1, 1],
    )
    bulk_si.calc = calc
    bulk_si.get_potential_energy()
    assert calc.results["exit_code"].status == 0
