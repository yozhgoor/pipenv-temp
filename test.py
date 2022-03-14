import unittest

from utils import Dependency
from utils import Repository
from utils import parse_dependency

def assert_eq(test_name, left, right):
    if left == right:
        print(f"{test_name}: Ok")
    else:
        print(f"{test_name}: Error")
        print("    Left: {0}, Right: {1}".format(left.debug(), right.debug()))

class TestDependencyParsing:

    def dependency():
        dependency = Dependency("anyhow", None)
        parsed = parse_dependency("anyhow")

        assert_eq("dependency", parsed, dependency)

    def dependency_with_version():
        dependency = Dependency("anyhow", "0.1")
        parsed = parse_dependency("anyhow=0.1")

        assert_eq("dependency_with_version", parsed, dependency)

    def dependency_with_exact_version():
        dependency = Dependency("anyhow", "=0.1")
        parsed = parse_dependency("anyhow==0.1")

        assert_eq("dependency_with_exact_version", parsed, dependency)

    def dependency_with_maximal_version():
        dependency = Dependency("anyhow", "<1.0.2")
        parsed = parse_dependency("anyhow=<1.0.2")

        assert_eq("dependency_with_maximal_version", parsed, dependency)

    def repository_with_http_url():
        repository = Repository("tokio", "https://github.com/tokio-rs/tokio.git", None, None)
        parsed = parse_dependency("tokio=https://github.com/tokio-rs/tokio.git")

        assert_eq("repository_with_http_url", parsed, repository)

    def repository_with_http_url_and_no_extension():
        repository = Repository("tokio", "https://github.com/tokio-rs/tokio", None, None)
        parsed = parse_dependency("tokio=https://github.com/tokio-rs/tokio")

        assert_eq("repository_with_http_url", parsed, repository)

    def repository_with_http_url_and_branch():
        repository = Repository("tokio", "https://github.com/tokio-rs/tokio.git", "compat", None)
        parsed = parse_dependency("tokio=https://github.com/tokio-rs/tokio.git#branch=compat")

        assert_eq("repository_with_http_url_and_branch", parsed, repository)

    def repository_with_http_url_and_rev():
        repository = Repository("tokio", "https://github.com/tokio-rs/tokio.git", None, "75c0777")
        parsed = parse_dependency("tokio=https://github.com/tokio-rs/tokio.git#rev=75c0777")

        assert_eq("repository_with_http_url_and_rev", parsed, repository)

    def repository_with_ssh_url():
        repository = Repository("serde","ssh://git@github.com/serde-rs/serde.git", None, None)
        parsed = parse_dependency("serde=ssh://git@github.com/serde-rs/serde.git")

        assert_eq("repository_with_ssh_url", parsed, repository)

    def repository_with_ssh_url_and_no_extension():
        repository = Repository("serde","ssh://git@github.com/serde-rs/serde", None, None)
        parsed = parse_dependency("serde=ssh://git@github.com/serde-rs/serde")

        assert_eq("repository_with_ssh_url_and_no_extension", parsed, repository)

    def repository_with_ssh_url_and_branch():
        repository = Repository("serde","ssh://git@github.com/serde-rs/serde.git", None, None)
        parsed = parse_dependency("serde=ssh://git@github.com/serde-rs/serde.git")

        assert_eq("repository_with_ssh_url", parsed, repository)

    def repository_with_ssh_url_and_rev():
        repository = Repository("serde", "ssh://git@github.com/serde-rs/serde.git", None, "5b140361a")
        parsed = parse_dependency("serde=ssh://git@github.com/serde-rs/serde.git#rev=5b140361a")

        assert_eq("repository_with_ssh_url_and_rev", parsed, repository)

TestDependencyParsing.dependency()
TestDependencyParsing.dependency_with_version()
TestDependencyParsing.dependency_with_exact_version()
TestDependencyParsing.dependency_with_maximal_version()

TestDependencyParsing.repository_with_http_url()
TestDependencyParsing.repository_with_http_url_and_no_extension()
TestDependencyParsing.repository_with_http_url_and_branch()
TestDependencyParsing.repository_with_http_url_and_rev()

TestDependencyParsing.repository_with_ssh_url()
TestDependencyParsing.repository_with_ssh_url_and_no_extension()
TestDependencyParsing.repository_with_ssh_url_and_branch()
TestDependencyParsing.repository_with_ssh_url_and_rev()
