import subprocess
import shutil
import os
import logging

DEFAULT_USER = "dchapp"
DEFAULT_EMAIL = "dylanchapp@gmail.com"

def cmd_exists(cmd):
    return shutil.which(cmd) is not None


def default_brew_packages():
    return (
        "cmake",
        "ninja",
        "bazel",
        "python@3.10",
        "rust",
        "jupyter",
        "ripgrep",
        "coreutils",
        "llvm",
        "gcc",
    )

def default_brew_cask_packages():
    return (
        "visual-studio-code",
        "spotify",
        "discord",
        "iterm2",
        "vlc",
        "signal",
    )

def default_python_tools():
    return (
        "mypy",
    )

def install_brew_packages(install_cask_packages=True):
    base_brew_install_cmd = ("brew", "install")
    base_brew_install_cask_cmd = ("brew", "install", "--cask")
    for pkg in default_brew_packages():
        cmd = (*base_brew_install_cmd, pkg)
        subprocess.run(cmd)
    if install_cask_packages:
        for pkg in default_brew_cask_packages():
            cmd = (*base_brew_install_cmd, pkg)
            subprocess.run(cmd)


def install_python_tools():
    base_cmd = ("python3", "-m", "pip", "install")
    for pkg in default_python_tools():
        cmd = (*base_cmd, pkg)
        subprocess.run(cmd)


def setup_brew():
    """
    Install homebrew if not already present
    """
    if not cmd_exists("brew"):
        install_brew_cmd = ("/bin/bash", "-c", "\"$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)\"")
        subprocess.run(install_brew_cmd)

def setup_git():
    """
    Set basic git configs
    """
    branch_name = "master"
    user_name = DEFAULT_USER
    user_email = DEFAULT_EMAIL
    base_git_config_cmds = (
            ("git", "config", "--global", "init.defaultBranch", branch_name),
            ("git", "config", "--global", "user.name", user_name),
            ("git", "config", "--global", "user.email", user_email),
            )
    for cmd in base_git_config_cmds:
        subprocess.run(cmd)

def setup_vim():
    """
    - Get pathogen
    - Get solarized colors
    - Copy default vimrc
    """
    # Setup pathogen
    pathogen_dirs = ("~/.vim/autoload", "~/.vim/bundle")
    for d in pathogen_dirs:
        os.makedirs(os.path.expanduser(d), exist_ok=True)
    pathogen_curl_cmd = ("curl", "-LSso", os.path.expanduser("~/.vim/autoload/pathogen.vim"), "https://tpo.pe/pathogen.vim")
    subprocess.run(pathogen_curl_cmd)
    # Get solarized color scheme
    clone_solarized_cmd = ("git", "clone", "git://github.com/altercation/vim-colors-solarized.git")
    pathogen_bundle_dir = os.path.expanduser("~/.vim/bundle")
    subprocess.run(clone_solarized_cmd, cwd=pathogen_bundle_dir)
    # Copy vimrc
    vimrc_src_path = os.path.join(os.getcwd(), "vimrc")
    vimrc_dst_path = os.path.expanduser("~/.vimrc")
    shutil.copyfile(vimrc_src_path, vimrc_dst_path)

def setup_shell():
    """"
    For right now, just copies a default zshrc to ~/.zshrc
    """
    zshrc_src_path = os.path.join(os.getcwd(), "zshrc")
    zshrc_dst_path = os.path.expanduser("~/.zshrc")
    shutil.copyfile(zshrc_src_path, zshrc_dst_path)
    
def make_ssh_keypair():
    cmd = ("ssh-keygen", "-t", "ed25519", "-C", DEFAULT_EMAIL, "-N", "", "-f", os.path.expanduser("~/.ssh/id_ed25519"),)
    subprocess.run(cmd)


def set_desktop_background():
    background_pic = os.path.abspath(os.path.join(os.getcwd(), "img", "flat_black.jpg"))
    osascript_cmd = f"tell application \"Finder\" to set desktop picture to POSIX file \"{background_pic}\""
    cmd = ("osascript", "-e", osascript_cmd)
    subprocess.run(cmd)


def main():
    setup_shell()
    setup_vim()
    setup_brew()
    make_ssh_keypair()
    set_desktop_background()

if __name__ == "__main__":
	main()
