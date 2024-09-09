from dataclasses import dataclass
from aiida.engine import ExitCode


@dataclass(frozen=True)
class PWExitCodes:
    ERROR_NO_RETRIEVED_TEMPORARY_FOLDER: ExitCode = ExitCode(
        301, "The retrieved temporary folder could not be accessed."
    )
    ERROR_OUTPUT_XML_MISSING: ExitCode = ExitCode(
        303, "The retrieved folder did not contain the required XML file."
    )
    ERROR_OUTPUT_XML_MULTIPLE: ExitCode = ExitCode(
        304, "The retrieved folder contained multiple XML files."
    )
    ERROR_OUTPUT_FILES: ExitCode = ExitCode(
        305, "Both the stdout and XML output files could not be read or parsed."
    )
    ERROR_OUTPUT_XML_READ: ExitCode = ExitCode(
        320, "The XML output file could not be read."
    )
    ERROR_OUTPUT_XML_PARSE: ExitCode = ExitCode(
        321, "The XML output file could not be parsed."
    )
    ERROR_OUTPUT_XML_FORMAT: ExitCode = ExitCode(
        322, "The XML output file has an unsupported format."
    )
    ERROR_OUT_OF_WALLTIME_INTERRUPTED: ExitCode = ExitCode(
        340,
        "The calculation stopped prematurely because it ran out of walltime but the \
job was killed by the scheduler before the files were safely written to disk for a potential restart.",
    )
    ERROR_UNEXPECTED_PARSER_EXCEPTION: ExitCode = ExitCode(
        350, "The parser raised an unexpected exception."
    )
    ERROR_G_PAR: ExitCode = ExitCode(
        360, "The code failed in finding a valid reciprocal lattice vector."
    )
    ERROR_ELECTRONIC_CONVERGENCE_NOT_REACHED: ExitCode = ExitCode(
        410, "The electronic minimization cycle did not reach self-consistency."
    )
    ERROR_DEXX_IS_NEGATIVE: ExitCode = ExitCode(
        461, "The code failed with negative dexx in the exchange calculation."
    )
    ERROR_COMPUTING_CHOLESKY: ExitCode = ExitCode(
        462, "The code failed during the cholesky factorization."
    )
    ERROR_DIAGONALIZATION_TOO_MANY_BANDS_NOT_CONVERGED: ExitCode = ExitCode(
        463, "Too many bands failed to converge during the diagonalization."
    )
    ERROR_S_MATRIX_NOT_POSITIVE_DEFINITE: ExitCode = ExitCode(
        464, "The S matrix was found to be not positive definite."
    )
    ERROR_ZHEGVD_FAILED: ExitCode = ExitCode(
        465, "The `zhegvd` failed in the PPCG diagonalization."
    )
    ERROR_QR_FAILED: ExitCode = ExitCode(
        466, "The `[Q, R] = qr(X, 0)` failed in the PPCG diagonalization."
    )
    ERROR_EIGENVECTOR_CONVERGENCE: ExitCode = ExitCode(
        467, "The eigenvector failed to converge."
    )
    ERROR_BROYDEN_FACTORIZATION: ExitCode = ExitCode(
        468, "The factorization in the Broyden routine failed."
    )
    ERROR_NPOOLS_TOO_HIGH: ExitCode = ExitCode(
        481,
        'The k-point parallelization "npools" is too high, some nodes have no k-points.',
    )
    ERROR_IONIC_CONVERGENCE_NOT_REACHED: ExitCode = ExitCode(
        500, "The ionic minimization cycle did not converge for the given thresholds."
    )
    ERROR_IONIC_CONVERGENCE_REACHED_EXCEPT_IN_FINAL_SCF: ExitCode = ExitCode(
        501,
        "Then ionic minimization cycle converged but the thresholds are exceeded in the final SCF.",
    )
    ERROR_IONIC_CYCLE_EXCEEDED_NSTEP: ExitCode = ExitCode(
        502,
        "The ionic minimization cycle did not converge after the maximum number of steps.",
    )
    ERROR_IONIC_INTERRUPTED_PARTIAL_TRAJECTORY: ExitCode = ExitCode(
        503,
        "The ionic minimization cycle did not finish because the calculation was interrupted \
but a partial trajectory and output structure was successfully parsed which can be used for a restart.",
    )
    ERROR_IONIC_CYCLE_ELECTRONIC_CONVERGENCE_NOT_REACHED: ExitCode = ExitCode(
        510,
        "The electronic minimization cycle failed during an ionic minimization cycle.",
    )
    ERROR_IONIC_CONVERGENCE_REACHED_FINAL_SCF_FAILED: ExitCode = ExitCode(
        511,
        "The ionic minimization cycle converged, but electronic convergence was not reached in the final SCF.",
    )
    ERROR_IONIC_CYCLE_BFGS_HISTORY_FAILURE: ExitCode = ExitCode(
        520,
        "The ionic minimization cycle terminated prematurely because of two consecutive \
failures in the BFGS algorithm.",
    )
    ERROR_IONIC_CYCLE_BFGS_HISTORY_AND_FINAL_SCF_FAILURE: ExitCode = ExitCode(
        521,
        "The ionic minimization cycle terminated prematurely because of two consecutive \
failures in the BFGS algorithm and electronic convergence failed in the final SCF.",
    )
    ERROR_CHARGE_IS_WRONG: ExitCode = ExitCode(
        531, "The electronic minimization cycle did not reach self-consistency."
    )
    ERROR_SYMMETRY_NON_ORTHOGONAL_OPERATION: ExitCode = ExitCode(
        541, "The variable cell optimization broke the symmetry of the k-points."
    )
    ERROR_RADIAL_FFT_SIGNIFICANT_VOLUME_CONTRACTION: ExitCode = ExitCode(
        542,
        "The cell relaxation caused a significant volume contraction and there is not enough \
space allocated for radial FFT.",
    )
    WARNING_ELECTRONIC_CONVERGENCE_NOT_REACHED: ExitCode = ExitCode(
        710,
        "The electronic minimization cycle did not reach self-consistency, but `scf_must_converge` \
is `False` and/or `electron_maxstep` is 0.",
    )
