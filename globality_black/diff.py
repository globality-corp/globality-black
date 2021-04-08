import tempfile
import subprocess


def git_diff(input_path, output_code):
    temp = tempfile.NamedTemporaryFile(mode='w+t')
    temp.writelines(output_code)
    temp.seek(0)
    subprocess.run(["git", "diff", "--no-index", input_path, temp.name])
    temp.close()
#path = Path("/Users/davidcohen/globality-black/globality_black/tests/fixtures/comprehensions_input.txt")
#expected_output = Path("/Users/davidcohen/globality-black/globality_black/tests/fixtures/comprehensions_output.txt").read_text()

#black_mode = get_black_mode(path)
#output = reformat_text(path.read_text(), black_mode)
#print(path.read_text())
#print()
#print(output)
#delta = color_diff(unified_diff(path.read_text(),output))
#delta = unified_diff(path.read_text(),output)
#delta = HtmlDiff().make_file(path.read_text(),output)
#with open("delta.html", "w") as f:
#f.write(delta)
#import os
#os.system("vim delta.html")
#diff = show_diff(path.read_text(),output)  # noqa
#sys.stdout.writelines(delta)
#result = subprocess.run(["git", "diff", "--no-index", "/Users/davidcohen/globality-black/globality_black/tests/fixtures/comprehensions_input.txt", 
#temp.name])
#result = subprocess.run(["git", "diff", "--no-index", "/Users/davidcohen/globality-black/globality_black/tests/fixtures/comprehensions_input.txt", 
#"/Users/davidcohen/globality-black/globality_black/tests/fixtures/comprehensions_input.txt"])
#result = subprocess.run([" echo {}".format(output)])
#print(delta)
#temp.close()
if __name__ == "__main__":
    from pathlib import Path
    from globality_black.black_handler import get_black_mode
    from globality_black.reformat_text import reformat_text
    path = Path("/Users/davidcohen/globality-black/globality_black/tests/fixtures/comprehensions_input.txt")
    black_mode = get_black_mode(path)
    output = reformat_text(path.read_text(), black_mode)
    git_diff(path, output)
