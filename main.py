"""
Main file to be executed
"""
import os
import subprocess
import shutil
import logging
import argparse
import sys
import enum


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


def write_remote_into_local(remote_folder: str) -> None:
    """Receive the path for both the downloaded file and the local file then
    replace the content of the local file for the content of the remote file.
    If the local file does not exists it will be created

    Args:
        remote_folder (str): Path for the Github Repo downloaded files
    """

    for key, value in FILES_PATH_LIST.items():

        remote_file_path = os.path.join(os.getcwd(), remote_folder, key),
        local_file_path = os.path.join(value, key)

        with open(remote_file_path, 'r', encoding='UTF-8') as remote_file:
            with open(local_file_path, 'w', encoding='UTF-8') as local_file:

                remote_file_content = remote_file.read()
                local_file.write(remote_file_content)

                local_file.close()

            remote_file.close()


def write_local_into_remote_then_push(remote_folder: str):
    """_summary_

    Args:
        remote_folder (str): Path for the Github Repo downloaded files
    """

    root_dir = os.getcwd()
    os.chdir(os.path.join(root_dir, remote_folder))

    for key, value in FILES_PATH_LIST.items():

        remote_file_path = os.path.join(root_dir, remote_folder, key)
        local_file_path = os.path.join(value, key)

        with open(remote_file_path, 'w', encoding='UTF-8') as remote_file:
            with open(local_file_path, 'r', encoding='UTF-8') as local_file:

                local_file_content = local_file.read()
                remote_file.write(local_file_content)

                local_file.close()

            remote_file.close()

        subprocess.run(
            ['git', 'add', key], check=True, stdout=False, stdin=False)

    subprocess.run(
        ['git', 'commit', '-m', 'update'], check=True, stdout=False, stdin=False)

    # pushing changes to remote git repository
    subprocess.run(
        ['git', 'push'], check=True, stdout=False, stdin=False)

    os.chdir(root_dir)


class TypesOfExecution(enum.Enum):
    """Enum class created to manage the possible ways in which the app can be executed. 
    Decided by command line and validated using this class 
    """
    DOWNLOAD_AND_REPLACE_LOCAL = 'download'
    UPLOAD_LOCAL_TO_GITHUB = 'upload'

    @staticmethod
    def return_types_as_list() -> list:
        '''Returns all the defined types as list to be used as choices in CLI parser'''
        return [t.value for t in TypesOfExecution]


if __name__ == '__main__':

    logger = logging.getLogger(__name__)
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s')

    parser = argparse.ArgumentParser(
        description='Arg to specify the Github repository used to manipulate the config files'
    )

    parser.add_argument('--repo', required=True, type=str)
    parser.add_argument('--type', required=False,
                        choices=TypesOfExecution.return_types_as_list(), default='download')

    args = parser.parse_args()

    # must be github repo with their config files
    git_repo = args.repo
    selected_type_of_execution = args.type

    if git_repo == '' or git_repo is None:
        logger.warning("Not a git repository")
        sys.exit()

    # If not a git repo then it should not be executed
    if '.git' not in git_repo:
        logger.warning('Repo need to be a non empty string')
        sys.exit()

    # Getting download location from git repo url
    download_folder: str = git_repo.split(
        '.git', maxsplit=1)[0].split('/')[-1]

    # cloning git repo using the system`s bash
    subprocess.run(
        ['git', 'clone', git_repo], check=True, stdout=False, stdin=False)

    try:

        if selected_type_of_execution == TypesOfExecution.DOWNLOAD_AND_REPLACE_LOCAL.value:
            write_remote_into_local(download_folder)

        elif selected_type_of_execution == TypesOfExecution.UPLOAD_LOCAL_TO_GITHUB.value:
            write_local_into_remote_then_push(download_folder)

        else:
            logger.info("Option not available")

    except Exception as e:
        logger.warning(e.args)

    finally:
        # cleaning download folder
        if os.path.isdir(download_folder):
            shutil.rmtree(download_folder)
