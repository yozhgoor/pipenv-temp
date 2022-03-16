import unittest

from dependency import Dependency
from dependency import Repository
from dependency import parse_dependency

class TestFailed(Exception):
    pass

def assert_eq(test_name, left, right):
    if left == right:
        print(f"{test_name}: Ok")
        return True
    else:
        print(f"{test_name}: Error")
        print("    Left: {0}, Right: {1}".format(left.debug(), right.debug()))
        return False

class TestDependencyParsing:

    def dependency():
        dependency = Dependency("anyhow", None)
        parsed = parse_dependency("anyhow")

        return assert_eq("dependency", parsed, dependency)

    def dependency_with_version():
        dependency = Dependency("anyhow", "0.1")
        parsed = parse_dependency("anyhow=0.1")

        return assert_eq("dependency_with_version", parsed, dependency)

    def dependency_with_exact_version():
        dependency = Dependency("anyhow", "=0.1")
        parsed = parse_dependency("anyhow==0.1")

        return assert_eq("dependency_with_exact_version", parsed, dependency)

    def dependency_with_maximal_version():
        dependency = Dependency("anyhow", "<1.2.2")
        parsed = parse_dependency("anyhow=<1.0.2")

        return assert_eq("dependency_with_maximal_version", parsed, dependency)

    def repository_with_http_url():
        repository = Repository("tokio", "https://github.com/tokio-rs/tokio.git", None, None)
        parsed = parse_dependency("tokio=https://github.com/tokio-rs/tokio.git")

        return assert_eq("repository_with_http_url", parsed, repository)

    def repository_with_http_url_and_no_extension():
        repository = Repository("tokio", "https://github.com/tokio-rs/tokio", None, None)
        parsed = parse_dependency("tokio=https://github.com/tokio-rs/tokio")

        return assert_eq("repository_with_http_url", parsed, repository)

    def repository_with_http_url_and_branch():
        repository = Repository("tokio", "https://github.com/tokio-rs/tokio.git", "compat", None)
        parsed = parse_dependency("tokio=https://github.com/tokio-rs/tokio.git#branch=compat")

        return assert_eq("repository_with_http_url_and_branch", parsed, repository)

    def repository_with_http_url_and_rev():
        repository = Repository("tokio", "https://github.com/tokio-rs/tokio.git", None, "75c0777")
        parsed = parse_dependency("tokio=https://github.com/tokio-rs/tokio.git#rev=75c0777")

        return assert_eq("repository_with_http_url_and_rev", parsed, repository)

    def repository_with_ssh_url():
        repository = Repository("serde","ssh://git@github.com/serde-rs/serde.git", None, None)
        parsed = parse_dependency("serde=ssh://git@github.com/serde-rs/serde.git")

        return assert_eq("repository_with_ssh_url", parsed, repository)

    def repository_with_ssh_url_and_no_extension():
        repository = Repository("serde","ssh://git@github.com/serde-rs/serde", None, None)
        parsed = parse_dependency("serde=ssh://git@github.com/serde-rs/serde")

        return assert_eq("repository_with_ssh_url_and_no_extension", parsed, repository)

    def repository_with_ssh_url_and_branch():
        repository = Repository("serde","ssh://git@github.com/serde-rs/serde.git", None, None)
        parsed = parse_dependency("serde=ssh://git@github.com/serde-rs/serde.git")

        return assert_eq("repository_with_ssh_url", parsed, repository)

    def repository_with_ssh_url_and_rev():
        repository = Repository("serde", "ssh://git@github.com/serde-rs/serde.git", None, "5b140361a")
        parsed = parse_dependency("serde=ssh://git@github.com/serde-rs/serde.git#rev=5b140361a")

        return assert_eq("repository_with_ssh_url_and_rev", parsed, repository)

status = True

if not TestDependencyParsing.dependency():
    status = False
if not TestDependencyParsing.dependency_with_version():
    status = False

if not TestDependencyParsing.dependency_with_exact_version():
    status = False
if not TestDependencyParsing.dependency_with_maximal_version():
    status = False

if not TestDependencyParsing.repository_with_http_url():
    status = False
if not TestDependencyParsing.repository_with_http_url_and_no_extension():
    status = False
if not TestDependencyParsing.repository_with_http_url_and_branch():
    status = False
if not TestDependencyParsing.repository_with_http_url_and_rev():
    status = False

if not TestDependencyParsing.repository_with_ssh_url():
    status = False
if not TestDependencyParsing.repository_with_ssh_url_and_no_extension():
    status = False
if not TestDependencyParsing.repository_with_ssh_url_and_branch():
    status = False
if not TestDependencyParsing.repository_with_ssh_url_and_rev():
    status = False

if status:
    print("Test passing")
else:
    raise TestFailed
