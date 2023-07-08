import argparse
import os

from pylint.lint import Run

parser = argparse.ArgumentParser(prog="LINT")

parser.add_argument(
    "-p",
    "--path",
    help="path to directory you want to run pylint | "
    "Default: %(default)s | "
    "Type: %(type)s ",
    default="./src",
    type=str,
)

parser.add_argument(
    "-t",
    "--threshold",
    help="score threshold to fail pylint runner | "
    "Default: %(default)s | "
    "Type: %(type)s ",
    default=7,
    type=float,
)

args = parser.parse_args()
path = str(args.path)
threshold = float(args.threshold)

print("PyLint Starting | " "Path: {} | " "Threshold: {} ".format(path, threshold))

script_dir = os.path.dirname(os.path.realpath(__file__))
module_path = os.path.join(script_dir, "..", path)

init_hook = '--init-hook=import os, sys; sys.path.append("' + module_path + '")'
print(init_hook)
ignore_paths = "--ignore-paths=" + path + "/k"

results = Run([init_hook, ignore_paths, path], do_exit=False)
# results = Run(["--disable=all", path], do_exit=False)

# print (results.linter.stats)

for info in ("error", "fatal"):
    for k, v in results.linter.stats.by_module.items():
        if v[info] > 0:
            message = f"Module:{k} Type:{info} #:{v[info]}"
            print(message)
            failed = True
            # raise Exception(message)

# print (results.linter.stats.by_module)
# print (json.dumps(results.linter.stats.by_module, indent=2))

final_score = results.linter.stats.global_note

if final_score < threshold:
    message = (
        "PyLint Failed | "
        "Score: {} | "
        "Threshold: {} ".format(final_score, threshold)
    )

    print(message)
    raise Exception(message)

else:
    message = (
        "PyLint Passed | "
        "Score: {} | "
        "Threshold: {} ".format(final_score, threshold)
    )

    print(message)

    exit(0)
