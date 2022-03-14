import re

class Dependency:
    def __init__(self, name, version):
        self.name = name
        self.version = version

    def __eq__(self, other):
        return ((self.name, self.version) == (other.name, other.version))

    def debug(self):
        return f"Dependency {{ name: {self.name}, version: {self.version} }}"

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
            dep_name = url_end

        return Repository(name, url, branch, rev)
    else:
        if name:
            dep_name = name
        else:
            dep_name = version
            version = None

        return Dependency(dep_name, version)
