from fabric.api import *

env.project_docroots = project_docroots = {
    "rpgplanet" : "/srv/www/rpgplanet.cz/www_root/www/htdocs",
    # sub for subdomains
    "rpghrac" : "/srv/www/rpghrac.cz/www_root/htdocs/sub",
    # sub for subdomains
    "hrac" : "/srv/www/rpghrac.cz/www_root/htdocs",
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
    require('applicationpath')
    run('mkdir -p %(applicationpath)s && cd %(applicationpath)s && virtualenv . && ./bin/easy_install pip' % env)

def upload_packages():
    """ Upload packages from package directory to virtual environment """
    put("%(distdir)s/* %(applicationpath)s" % env)
    for package in env.packages:
        env.package = package
        # destory version suffix
        run('cd %(applicationpath)s && tar xvzpf %(package)s-* && mv %(package)s-* %(package)s' % env )

def install_requirements():
    """Install the required packages using pip"""
    for package in env.packages:
        env.package = package
        run('cd %(applicationpath)s && ./bin/pip install -E . -r ./%(package)s/freezed-requirements.txt' % env)
        run('cd %(applicationpath)s && cd %(package)s && ./../bin/python setup.py develop' % env )

def deploy_to_server():
    setup()
    upload_packages()
    install_requirements()
    resymlink_media()
    migrate_database()
    resymlink_release()
    restart_services()
    

def deploy_preproduction(meta_version, dist_dir):
    """Deploy the latest version of the site to the production server and """
    env.release = 'current'

    env.meta_version = meta_version
    env.dist_dir = dist_dir

    env.applicationpath = '/srv/applications/w-rpgplanet-cz/rpgplanet/%s' % env.meta_version

    deploy_to_server()


def deploy(meta_version, dist_dir):
    """Deploy the latest version of the site to the production server and """
    env.applicationpath = '/srv/applications/w-rpgplanet-cz/rpgplanet/%s' % env.version
    env.user = 'w-rpgplanet-cz'

    env.meta_version = meta_version
    env.dist_dir = dist_dir

    deploy_to_server()
    restart_services()

def resymlink_media():
    # TODO: static media are now on same server, this may be not so in the future
    for package in env.packages:
        if package in project_docroots:
            run(('cd %(applicationpath)s; ln -sf `pwd`/%(package)s/static/ %(docroot)s/%(meta_version)s/' % {
                'docroot' : project_docroots[package],
                'package' : package,
                'meta_version' : env.meta_version,
            }) % env)

def resymlink_release():
    """Symlink our current release, uploads and settings file"""
    run('cd %(applicationpath)s && cd .. && ln -sf %(applicationpath)s `pwd`/current' % env)

def migrate_database():
    """Run our migrations"""
    for package in env.packages:
        run(('cd %(applicationpath)s; cd %s; ./../bin/python manage.py syncdb --noinput --migrate' % package) % env )

def restart_services():
    """Restart all project lighties"""
    for service in env.services:
        sudo('svc -t /etc/service/%s' % service)

def downgrade_release():
    raise NotImplementedError()
    #TODO: Got to old release (probably given?), resymlink back, run migrations
    
