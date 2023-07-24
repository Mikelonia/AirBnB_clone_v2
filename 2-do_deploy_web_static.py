#!/usr/bin/python3
# Fabfile to distribute an archive to a web server. By Okpako Michael
import os.path
from fabric.api import env
from fabric.api import put
from fabric.api import run

env.hosts = ['<54.236.47.105>', '<100.25.167.77>']

def do_deploy(archive_path):
    """Distributes an archive to a web server.

    Args:
        archive_path (str): The path of the archive to distribute.
    Returns:
        If the file doesn't exist at archive_path or an error occurs - False.
        Otherwise - True.
    """
    if os.path.isfile(archive_path) is False:
        return False

    # Upload the archive to the /tmp/ directory on the web servers
    file = archive_path.split("/")[-1]
    if put(archive_path, "/tmp/{}".format(file)).failed is True:
        return False

    # Uncompress the archive to the folder /data/web_static/releases/<archive filename without extension> on the web servers
    name = file.split(".")[0]
    if run("mkdir -p /data/web_static/releases/{}/".format(name)).failed is True:
        return False
    if run("tar -xzf /tmp/{} -C /data/web_static/releases/{}/".format(file, name)).failed is True:
        return False
    if run("rm /tmp/{}".format(file)).failed is True:
        return False

    # Delete the symbolic link /data/web_static/current from the web servers
    if run("rm -rf /data/web_static/current").failed is True:
        return False

    # Create a new symbolic link /data/web_static/current on the web servers, linked to the new version of your code (/data/web_static/releases/<archive filename without extension>)
    if run("ln -s /data/web_static/releases/{}/ /data/web_static/current".format(name)).failed is True:
        return False

    return True


