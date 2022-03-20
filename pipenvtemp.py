import argparse
import os
import shutil
import appdirs
import tempfile
import subprocess
import re

class Dependency:
    def __init__(self, name, version):
        self.name = name
        self.version = version

    def __eq__(self, other):
        return ((self.name, self.version) == (other.name, other.version))

    def debug(self):
        return f"Dependency {{ name: {self.name}, version: {self.version} }}"

    def fmt(self):
        if self.version:
            return f"{self.name} = \"{self.version}\""
        else:
            return f"{self.name} = \"*\""

class Repository:
    def __init__(self, name, url, branch, rev):
        self.name = name
        self.url = url
        self.branch = branch
        self.rev = rev

    def __eq__(self, other):
        return ((self.name, self.url, self.branch, self.rev) == (other.name, other.url, other.branch, other.rev))

    def debug(self):
        return f"Repository {{ name: {self.name}, url: {self.url}, branch: {self.branch}, rev: {self.rev} }}"

    def fmt(self):
        if self.branch:
            ref = self.branch
        elif self.rev:
            ref = self.rev
        else:
            ref = "main"

        return f"{self.name} = {{ editable = true, ref = \"{ref}\", git = \"{self.url}\"}}"


def parse_dependency(dependency):
    prog = re.compile(r"^((?P<name>[^+=/]+)=)?(?P<version>((?P<url>\w+://([^:@]+(:[^@]+)?@)?[^#+]*?(?P<url_end>/[^#+/]+)?)(#branch=(?P<branch>[^+]+)|#rev=(?P<rev>[^+]+))?)|[^+]+)?$")
    result = prog.match(dependency)

    name = result.group("name")
    version = result.group("version")
    url = result.group("url")
    url_end = result.group("url_end")
    branch = result.group("branch")
    rev = result.group("rev")

    if url:
        if name:
            dep_name = name
        else:
            dep_name = url_end.replace("/", "", 1)

        return Repository(dep_name, url, branch, rev)
    else:
        if name:
            dep_name = name
        else:
            dep_name = version
            version = None

        return Dependency(dep_name, version)

class TestDependencyParsing:
    def test_dependency(self):
        assert Dependency("requests", None) == parse_dependency("requests")

    def test_dependency_with_version(self):
        assert Dependency("requests", "2.27") \
            == parse_dependency("requests=2.27")

    def test_dependency_with_exact_version(self):
        assert Dependency("requests", "=2.27.1") \
            == parse_dependency("requests==2.27.1")

    def test_dependency_with_maximal_version(self):
        assert Dependency("requests", "<2.25.1") \
            == parse_dependency("requests=<2.25.1")

    def test_repository_with_http_url(self):
        assert Repository("matplotlib", "https://github.com/matplotlib/matplotlib", None, None) \
            == parse_dependency("matplotlib=https://github.com/matplotlib/matplotlib")

    def test_repository_with_http_url_and_no_extension(self):
        assert Repository("matplotlib", "https://github.com/matplotlib/matplotlib", None, None) \
            == parse_dependency("https://github.com/matplotlib/matplotlib")

    def test_repository_with_http_url_and_branch(self):
        assert Repository("matplotlib", "https://github.com/matplotlib/matplotlib.git", "old_master", None) \
            == parse_dependency("matplotlib=https://github.com/matplotlib/matplotlib.git#branch=old_master")

    def test_repository_with_http_url_and_rev(self):
        assert Repository("matplotlib", "https://github.com/matplotlib/matplotlib.git", None, "f6e0ee4") \
            == parse_dependency("matplotlib=https://github.com/matplotlib/matplotlib.git#rev=f6e0ee4")

    def test_repository_with_ssh_url(self):
        assert Repository("pygame","ssh://git@github.com:pygame/pygame.git", None, None) \
            == parse_dependency("pygame=ssh://git@github.com:pygame/pygame.git")

    def test_repository_with_ssh_url_and_no_extension(self):
        assert Repository("pygame","ssh://git@github.com:pygame/pygame", None, None) \
            == parse_dependency("ssh://git@github.com:pygame/pygame")

    def test_repository_with_ssh_url_and_branch(self):
        assert Repository("pygame","ssh://git@github.com:pygame/pygame.git", "android", None) \
            == parse_dependency("pygame=ssh://git@github.com:pygame/pygame.git#branch=android")

    def test_repository_with_ssh_url_and_rev(self):
        assert Repository("pygame", "ssh://git@github.com:pygame/pygame.git", None, "c1afa68") \
            == parse_dependency("pygame=ssh://git@github.com:pygame/pygame.git#rev=c1afa68")

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
