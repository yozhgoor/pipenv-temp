import argparse

from utils import parse_dependency

if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog="pipenv-temp")
    parser.add_argument("dependencies", nargs='*', help="dependencies passed to pipenv")
    args = parser.parse_args()

    for dependency in args.dependencies:
        parsed = parse_dependency(dependency)
        print(parsed.debug())
