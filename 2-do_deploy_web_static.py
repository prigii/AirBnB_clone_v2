#!/usr/bin/python3
"""Deploy archive!"""
from fabric.api import env, put, run
import os

env.hosts = ['<IP web-01>', '<IP web-02>']
env.user = '<username>'
env.key_filename = '/path/to/ssh/key'


def do_deploy(archive_path):
    if not os.path.exists(archive_path):
        return False

    archive_name = os.path.basename(archive_path)
    archive_root, _ = os.path.splitext(archive_name)

    try:
        put(archive_path, '/tmp/')
        run('mkdir -p /data/web_static/releases/{}/'.format(archive_root))
        run('tar -xzf /tmp/{} -C /data/web_static/releases/{}/'.format(
            archive_name, archive_root))
        run('rm /tmp/{}'.format(archive_name))
        run('mv /data/web_static/releases/{}/web_static/* \
            /data/web_static/releases/{}/'.format(
                archive_root, archive_root))
        run('rm -rf /data/web_static/releases/{}/web_static'.format(
            archive_root))
        run('rm -rf /data/web_static/current')
        run('ln -s /data/web_static/releases/{}/ \
            /data/web_static/current'.format(archive_root))
    except Exception as e:
        print(e)
        return None
