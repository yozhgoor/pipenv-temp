import argparse
import os
import shutil

from dependency import parse_dependency

if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog="pipenv-temp")
    parser.add_argument("dependencies", nargs='*', help="dependencies passed to pipenv")
    args = parser.parse_args()

    if os.path.isdir("tmp"):
        pipfile = open("tmp/Pipfile", "w")
    else:
        os.mkdir("tmp")
        pipfile = open("tmp/Pipfile", "w")

    pipfile.write("[packages]\n")

    for dependency in args.dependencies:
        dependency = parse_dependency(dependency)
        print(dependency.debug())

        pipfile.write(dependency.fmt()+"\n")

    pipfile.close()

    appfile = open("tmp/app.py", "w")
    appfile.write('''import requests

request = requests.get("https://github.com/yozhgoor")
print(request.status_code)
    ''')
    appfile.close()
