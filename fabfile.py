from fabric.api import *

project_docroots = {
    "rpgplanet" : "/srv/www/rpgplanet.cz/www_root/www/htdocs",
    # sub for subdomains
    "rpghrac" : "/srv/www/rpghrac.cz/www_root/htdocs/sub/",
}

# this might be read from mypage-all/runcommand.py to have things on one place
# however, considering deployments of new projects, it might make sense to have
# devel versions in -all already, but not in deployment files.
# Anyways, YAGNI, it's no such PITA to script this out. Reconsider when we are
# going to have more than 10 sites deployed.

env.services = project_docroots.keys()

env.projects = projects = (
    "rpgcommon",
) + tuple(project_docroots.keys())

libraries = (
)

env.packages = projects + libraries

def setup():
    """
    Setup a fresh virtualenv and install everything we need so it's ready to
    deploy to
    """
    run('mkdir -p $(applicationpath); cd $(applicationpath); virtualenv .; easy_install pip')

def install_requirements():
    """Install the required packages using pip"""
    for package in env.packages:
        run('cd $(applicationpath) && pip install -E . -r ./%s/freezed-requirements.txt' % package)
        run('cd $(applicationpath) && cd %s && ./../bin/python setup.py develop' % package)

def deploy_to_server():
    setup()
    install_requirements()
    resymlink_media()
    migrate_database()
    resymlink_release()
    restart_services()
    

def deploy_preproduction(meta_version, dist_dir):
    """Deploy the latest version of the site to the production server and """

    env.hosts = ['melissar']

    env.release = 'current'

    env.meta_version = meta_version
    env.dist_dir = dist_dir

    env.applicationpath = '/srv/applications/w-rpgplanet-cz/rpgplanet/%s' % env.meta_version


    deploy_to_server()


def deploy(meta_version, dist_dir):
    """Deploy the latest version of the site to the production server and """

    env.hosts = ['kenshin:2222']

    env.applicationpath = '/srv/applications/w-rpgplanet-cz/rpgplanet/%s' % env.version
    env.user = 'w-rpgplanet-cz'

    env.meta_version = meta_version
    env.dist_dir = dist_dir

    deploy_to_server()

def resymlink_media():
    raise NotImplementedError()
    for package in env.packages:
        if package in project_docroots:
            run('cd %s; ln -sf' % project_docroots[package])

def resymlink_release():
    """Symlink our current release, uploads and settings file"""
    raise NotImplementedError()
#    run('cd $(path); rm project; ln -s releases/current project; rm releases/current; ln -s $(release) releases/current')
#    run('cd $(path)/releases/current/; ln -s settings_$(settings).py settings.py', fail='ignore')
#    run('cd $(path)/releases/current/media/; ln -s ../../../shared/uploads/ .', fail='ignore')

def migrate_database():
    """Run our migrations"""
    for package in env.packages:
        run('cd $(applicationpath); cd %s; ./../bin/python manage.py syncdb --noinput --migrate' % package)

def restart_services():
    """Restart all project lighties"""
    for service in env.services:
        sudo('svc -t /etc/service/%s' % service)

