"""
Main file to be executed
"""
import os
import subprocess
import shutil
import logging
import argparse
import sys

# list is supported files that will be placed/written
# it follows this structure: 'filename.extension': 'path it is/will be placed'
FILES_PATH_LIST: dict[str, str] = {
    'extensions.json': os.path.join(os.path.expanduser('~'),
                                    '.vscode-oss', 'extensions'),
    'settings.json': os.path.join(os.path.expanduser('~'),
                                  '.config', 'VSCodium', 'User'),
    '.gitconfig': os.path.expanduser('~'),
    '.zshrc': os.path.expanduser('~'),
    '.bashrc': os.path.expanduser('~')
}


def write_remote_into_local(remote_file_path: str, local_file_path: str) -> None:
    """Receive the path for both the downloaded file and the local file then
    replace the content of the local file for the content of the remote file.
    If the local file does not exists it will be created

    Args:
        remote_file_path (str): Path for the Github Repo downloaded file
        local_file_path (str): Path for the local file or where it must be created
    """
    with open(remote_file_path, 'r', encoding='UTF-8') as remote_file:
        with open(local_file_path, 'w', encoding='UTF-8') as local_file:

            remote_file_content = remote_file.read()
            local_file.write(remote_file_content)
            local_file.close()

        remote_file.close()


if __name__ == '__main__':

    logger = logging.getLogger(__name__)
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s')

    parser = argparse.ArgumentParser(
        description="Script that adds 3 numbers from CMD"
    )

    parser.add_argument("--repo", required=True, type=str)
    args = parser.parse_args()

    # must be github repo with their config files
    git_repo = args.repo

    if git_repo == '' or git_repo is None:
        logger.warning("Not a git repository")
        sys.exit()

    # If not a git repo then it should not be executed
    if '.git' not in git_repo:
        logger.warning('Repo need to be a non empty string')
        sys.exit()

    try:
        # Getting download location from git repo url
        download_folder: str = git_repo.split(
            '.git', maxsplit=1)[0].split('/')[-1]

        # cloning git repo using the system`s bash
        subprocess.run(
            ['git', 'clone', git_repo], check=True)

        # iterating files
        for key, value in FILES_PATH_LIST.items():

            write_remote_into_local(
                remote_file_path=os.path.join(
                    os.getcwd(), download_folder, key),
                local_file_path=os.path.join(value, key)
            )

    except Exception as e:
        logger.warning(e.args)
    finally:
        # cleaning download folder
        if os.path.isdir(download_folder):
            shutil.rmtree(download_folder)
