#!/usr/bin/python3
"""Deploy archive!"""
from fabric.api import env, put, run
import os

env.hosts = ['<IP web-01>', '<IP web-02>']
env.user = '<username>'
env.key_filename = '/path/to/your/private/key'


def do_deploy(archive_path):
    if not os.path.exists(archive_path):
        return False

    file_name = archive_path.split('/')[-1]
    folder_name = file_name.split('.')[0]

    put(archive_path, '/tmp/')
    run('mkdir -p /data/web_static/releases/{}/'.format(folder_name))
    run('tar -xzf /tmp/{} -C /data/web_static/releases/{}/'.format(file_name, folder_name))
    run('rm /tmp/{}'.format(file_name))
    run('mv /data/web_static/releases/{}/web_static/* /data/web_static/releases/{}/'.format(folder_name, folder_name))
    run('rm -rf /data/web_static/releases/{}/web_static'.format(folder_name))
    run('rm -rf /data/web_static/current')
    run('ln -s /data/web_static/releases/{}/ /data/web_static/current'.format(folder_name))

    return True
