import argparse
import os
import shutil
import appdirs
import tempfile

from dependency import parse_dependency


if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog="pipenv-temp")
    parser.add_argument("dependencies", nargs='*', help="dependencies passed to pipenv")
    args = parser.parse_args()

    cache_dir = appdirs.user_cache_dir(appname='pipenv-temp')

    if not os.path.isdir(cache_dir):
        os.mkdir(cache_dir)

    tmp_dir = tempfile.mkdtemp(dir=cache_dir)
    print(f"Generating project at {tmp_dir}")

    pipfile = open(os.path.join(tmp_dir, "Pipfile"), "w")
    pipfile.write("[packages]\n")

    for dependency in args.dependencies:
        dependency = parse_dependency(dependency)
        print(dependency.debug())

        pipfile.write(dependency.fmt()+"\n")

    pipfile.close()
    print("Pipfile generated")

    appfile = open(os.path.join(tmp_dir, "app.py"), "w")
    appfile.write('''import requests

request = requests.get("https://github.com/yozhgoor")
print(request.status_code)
    ''')
    appfile.close()
    print("app.py generated")
