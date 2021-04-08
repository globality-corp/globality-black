import tempfile
import subprocess


def git_diff(input_path, output_code):
    temp = tempfile.NamedTemporaryFile(mode='w+t')
    temp.writelines(output_code)
    temp.seek(0)
    subprocess.run(["git", "diff", "--no-index", input_path, temp.name])
    temp.close()


if __name__ == "__main__":
    from pathlib import Path
    from globality_black.black_handler import get_black_mode
    from globality_black.reformat_text import reformat_text
    path = Path("/Users/davidcohen/globality-black/globality_black/tests/fixtures/comprehensions_input.txt")
    black_mode = get_black_mode(path)
    output = reformat_text(path.read_text(), black_mode)
    git_diff(path, output)
