from pipenvtemp import Dependency
from pipenvtemp import Repository
from pipenvtemp import parse_dependency

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
