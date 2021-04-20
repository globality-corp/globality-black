import tempfile
from pathlib import Path

import pexpect


def git_diff(input_path: Path, output_code: str) -> str:
    with tempfile.NamedTemporaryFile(mode="w+t") as temp_file:
        temp_file.writelines(output_code)
        temp_file.seek(0)
        output = pexpect.run(
            "git --no-pager diff --no-index {} {}".format(input_path, temp_file.name)
        )
        temp_file.close()
        return output.decode()
