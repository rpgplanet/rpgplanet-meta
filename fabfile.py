from fabric.api import *

env.project_docroots = project_docroots = {
    "rpgplanet" : "/srv/rpgplanet.cz/www_root/www/htdocs",
    "rpgscheduler" : "/srv/rpgplanet.cz/www_root/akce/htdocs",
    # sub for subdomains
    "rpghrac" : "/srv/rpghrac.cz/www_root/htdocs/sub",
    # sub for subdomains
    "metaplayer" : "/srv/rpghrac.cz/www_root/htdocs/meta",
}

# this might be read from mypage-all/runcommand.py to have things on one place
# however, considering deployments of new projects, it might make sense to have
# devel versions in -all already, but not in deployment files.
# Anyways, YAGNI, it's no such PITA to script this out. Reconsider when we are
# going to have more than 10 sites deployed.

env.services = ['rpgplanet.cz', 'rpghrac.cz', 'akce.rpgplanet.cz']

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
    put("%(dist_dir)s/*" % env, "%(applicationpath)s" % env)
    for package in env.packages:
        env.package = package
        # destory version suffix
        run('cd %(applicationpath)s && tar xvzpf %(package)s-* && rm %(package)s-*.tar.* && mv %(package)s-* %(package)s' % env )

def install_requirements():
    """Install the required packages using pip"""
    for package in env.packages:
        env.package = package
        # paver is special because it is required for some egg_infos
        run('cd %(applicationpath)s && ./bin/pip install -E . paver' % env)
        run('cd %(applicationpath)s && ./bin/pip install -E . -r ./%(package)s/requirements.txt' % env)
        run('cd %(applicationpath)s && cd %(package)s && ./../bin/python setup.py develop' % env )

def deploy_to_server():
    setup()
    upload_packages()
    install_requirements()
    resymlink_media()
    migrate_database()
    resymlink_release()
    restart_services()
    

def deploy(meta_version, dist_dir, rpgplanet_version, rpghrac_version, rpgcommon_version, metaplayer_version, rpgscheduler_version):
    """Deploy the latest version of the site to the production server and """
    
    env.meta_version = meta_version
    env.dist_dir = dist_dir
    env.project_versions = {
        'rpgplanet' : rpgplanet_version,
        'rpghrac' : rpghrac_version,
	'rpgscheduler' : rpgscheduler_version,
        'rpgcommon' : rpgcommon_version,
        'metaplayer' : metaplayer_version,
    }

    env.applicationpath = '/srv/applications/w-almad/rpgplanet/%s' % env.meta_version
    env.user = 'w-almad'

    deploy_to_server()

def resymlink_media():
    # TODO: static media are now on same server, this may be not so in the future
    for package in env.packages:
        if package in project_docroots:
	    env.docroot = project_docroots[package]
	    env.package = package
            env.project_version = env.project_versions[package]
            run('cd %(applicationpath)s && if [ ! -e %(docroot)s/%(project_version)s ]; then ln -sf `pwd`/%(package)s/%(package)s/static/ %(docroot)s/%(project_version)s; fi;' % env)

def resymlink_release():
    """Symlink our current release, uploads and settings file"""
    run('cd %(applicationpath)s && cd .. && if [ -e `pwd`/current ]; then rm `pwd`/current; fi && ln -sf %(applicationpath)s `pwd`/current' % env)

def migrate_database():
    """Run our migrations"""
    for package in env.packages:
        env.package = package
        run('cd %(applicationpath)s; cd %(package)s/%(package)s; ./../../bin/python manage.py syncdb --noinput --migrate' % env )

def restart_services():
    """Restart all project lighties"""
    for service in env.services:
        run('sudo svc -t /service/%s' % service)
    
    # give services a sec or five to start up
    from time import sleep
    sleep(5)

    for service in env.services:
        # this sucks and shall be handled by startup/service; when some oracle will answer
        # http://stackoverflow.com/questions/3431029/socket-permissions-when-running-django-with-fastcgi
        # we'll get rid of it
        run('sudo chmod 0770 /var/www/fastcgi/sockets/w-almad/%s.socket' % service)

def downgrade_release():
    raise NotImplementedError()
    #TODO: Got to old release (probably given?), resymlink back, run migrations
    
