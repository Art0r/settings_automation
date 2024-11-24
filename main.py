'''
main code
'''
import os
import subprocess
import shutil
from functools import wraps


DOWNLOAD_LOCATION = "dotfiles"
GIT_REPO = str(input("Especifique o endereço do repositório no Github: ")).strip()

def download_remote_configs() -> None:
    '''main.py'''
    subprocess.run(
        ['git', 'clone', GIT_REPO], check=True)


def remove_remote_configs() -> None:
    '''main.py'''
    shutil.rmtree(DOWNLOAD_LOCATION)


def read_remote_content(filename: str) -> str:
    '''main.py'''
    return open(
        os.path.join(DOWNLOAD_LOCATION, filename), 'r', encoding='UTF-8').read()


def write_remote_settings_to_local() -> None:
    '''main.py'''
    vscode_config_path = os.path.join(
        os.path.expanduser('~'), '.config', 'VSCodium')

    vscode_config_user_path = os.path.join(vscode_config_path, 'User')

    vscode_settings_json_path = os.path.join(
        vscode_config_user_path, 'settings.json')

    with open(vscode_settings_json_path, 'w', encoding='UTF-8') as file:
        content = read_remote_content('settings.json')
        file.write(content)
        file.close()


def write_remote_extensions_to_local() -> None:
    '''main.py'''
    vscode_path = os.path.join(os.path.expanduser('~'), '.vscode-oss')

    vscode_extensions_path = os.path.join(vscode_path, 'extensions')

    vscode_extensions_json_path = os.path.join(
        vscode_extensions_path, 'extensions.json')

    with open(vscode_extensions_json_path, 'w', encoding='UTF-8') as file:
        content = read_remote_content('extensions.json')
        file.write(content)
        file.close()


def handle(func) -> None:
    '''main.py'''
    wraps(func)

    def wrapper(*args, **kwargs):

        download_remote_configs()
        func(*args, **kwargs)
        remove_remote_configs()

    return wrapper


@handle
def main():
    '''main.py'''
    write_remote_extensions_to_local()
    write_remote_settings_to_local()


if __name__ == '__main__':
    main()
