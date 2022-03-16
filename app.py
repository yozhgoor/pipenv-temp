import argparse
import os
import shutil
import appdirs
import tempfile
import subprocess

from dependency import parse_dependency

if __name__ == '__main__':
    # Initiate the CLI
    parser = argparse.ArgumentParser(prog="pipenv-temp")
    parser.add_argument("dependencies", nargs='*', help="dependencies passed to pipenv")

    # Parse CLI args
    args = parser.parse_args()

    # Get the user cache directory
    cache_dir = appdirs.user_cache_dir(appname='pipenv-temp')
    if not os.path.isdir(cache_dir):
        os.mkdir(cache_dir)

    # Create the temporary directory
    tmp_dir = tempfile.mkdtemp(dir=cache_dir)
    print(f"Generating project at {tmp_dir}")

    # Create the `Pipfile` of the project
    pipfile = open(os.path.join(tmp_dir, "Pipfile"), "w")
    pipfile.write("[packages]\n")

    # Add dependencies to the `Pipfile`
    for dependency in args.dependencies:
        dependency = parse_dependency(dependency)
        print(dependency.debug())

        pipfile.write(dependency.fmt()+"\n")

    pipfile.close()
    print("Pipfile generated")

    # Create a basic `app.py` file
    app_file = open(os.path.join(tmp_dir, "app.py"), "w")
    app_file.write('''import requests

request = requests.get("https://github.com/yozhgoor")
print(request.status_code)
    ''')
    app_file.close()
    print("app.py generated")

    # Create the TO_DELETE file
    to_delete_file = open(os.path.join(tmp_dir, "TO_DELETE"), "x")
    to_delete_file.close()

    # Install dependencies with pipenv
    subprocess.run(["pipenv", "install"], cwd = tmp_dir)

    # Start a shell
    subprocess.run(["pipenv", "shell"], cwd = tmp_dir)

    # Clean up when exiting the shell
    if os.path.isfile(os.path.join(tmp_dir, "TO_DELETE")):
        subprocess.run(["pipenv", "--rm"], cwd = tmp_dir)
        shutil.rmtree(tmp_dir)
        print(f"Project deleted")
    else:
        print(f"Project preserved at {tmp_dir}")
