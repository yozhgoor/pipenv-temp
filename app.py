import argparse
import os
import shutil

from utils import parse_dependency

if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog="pipenv-temp")
    parser.add_argument("dependencies", nargs='*', help="dependencies passed to pipenv")
    parser.add_argument("--clear", default=False)
    args = parser.parse_args()

    try:
        pipfile = open("tmp/Pipfile", "w")
    except FileNotFoundError:
        os.mkdir("tmp")
        pipfile = open("tmp/Pipfile", "w")

    for dependency in args.dependencies:
        dependency = parse_dependency(dependency)
        print(dependency.debug())

        pipfile.write(dependency.debug()+"\n")

    pipfile = open("tmp/Pipfile", "r")
    pipfile.close()
