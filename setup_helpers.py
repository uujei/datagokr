import os

REPOS = ["git+", "svn+", "hg+"]


def _get_requirements(requirements):
    if not os.path.exists(requirements):
        return []
    try:
        with open("requirements.txt") as f:
            requirements = f.read().splitlines()
    except Exception as ex:
        with open("DecoraterBotUtils.egg-info\requires.txt") as f:
            requirements = f.read().splitlines()
    return [_ for _ in requirements if not _.startswith("#")]


def get_requirements(requirements, remove_links=False):
    """
    lists the requirements to install.
    """
    requirements = _get_requirements(requirements=requirements)

    if remove_links:
        for _repo in REPOS:
            requirements = [_ for _ in requirements if not _.startswith(_repo)]

    return requirements


def get_links(requirements):
    """
    gets URL Dependency links.
    """
    links = []
    requirements = _get_requirements(requirements=requirements)

    for _repo in REPOS:
        links += [_ for _ in requirements if _.startswith(_repo)]

    return links
