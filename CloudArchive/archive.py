import os
import logging

from CloudArchive import config
from CloudArchive import log_config

log = logging.getLogger("cloud_archive")


class Repo(object):
    origin = None
    config = None
    name = None

    def __init__(self, path):
        self.path = path

        self._get_name_from_path()
        self.get_existing_remotes()

        drive, root_project, remaining_path = self.path.split(os.path.sep, 2)
        self.project_cloud_folder = os.path.join(drive + os.path.sep, root_project, "cloud")  # not sure why I need to add os.path.sep to the drive letter, but I dooo.

    def _get_name_from_path(self):
        self.name = os.path.split(os.path.split(self.path)[0])[1]

    def get_existing_remotes(self):
        """
            So, one goal here is that we make sure that we back up any Git repositories we have. But also, maybe we don't
            duplicate the data too much. To start with, let's figure out the remote origins of each git repository that's
            already on disk. At some point, we might want to also check how far behind the origin this repository is,
            and if it's more than a handful of commits behind (how many, I don't know right now), then we clone a copy
            to the backup location anyway.
        :return:
        """

        log.debug("Getting remote origin for {}".format(self.name))
        self.config = os.path.join(self.path, "config")
        with open(self.config, 'r') as config_file:
            config_lines = config_file.readlines()

        for i, line in enumerate(config_lines):
            if line.strip() == "[remote \"origin\"]":
                self.origin = config_lines[i+1].split("=")[1].strip()


def find_git_repos(root_folder=config.root_search_folder):
    """
        Just a simple function to find any Git repository under the root folder provided. Searches the tree
        for any folder named .git and returns a list of Repo objects with the paths populated
    :param root_folder:
    :return:
    """
    git_repos = []

    log.info("Searching for Git repositories in subfolders of {}. This may take a long time".format(root_folder))

    for dirpath, dirnames, filenames in os.walk(root_folder):
        if ".git" in dirnames:
            git_repos.append(Repo(path=os.path.join(dirpath, ".git")))

    return git_repos


def main(base_folder="X:\\"):
    """
        Find all existing repositories, finds all repositories marked as associated with projects, and establishes a
        backup of repositories that don't already exist.
    :return:
    """
