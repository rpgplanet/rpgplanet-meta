import os
from os.path import join, pardir, abspath, dirname, split
import sys
from tempfile import mkdtemp

from setuptools import find_packages

from paver.easy import *
from paver.setuputils import setup, Bunch


VERSION = (0, 1)

__version__ = VERSION
__versionstr__ = '.'.join(map(str, VERSION))

setup(
    name = 'rpgplanet_meta',
    version = __versionstr__,
    description = 'RPG Planet meta package',
    long_description = '\n'.join((
        'RPG Planet Meta Package',
        '',
        '',
    )),
    author = 'Almad',
    author_email='bugs@almad.net',
    license = 'BSD',                                                                                                                                                                                                                                                    
    url='http://github.com/rpgplanet/rpgplanet-meta',

    dependencies_git_repositories = [
        {
            'url': 'git://github.com/rpgplanet/rpgcommon.git',
            'package_name': 'rpgcommon',
        },
        {
            'url': 'git://github.com/rpgplanet/rpghrac.git',
            'package_name': 'rpghrac',
        },
        {
            'url': 'git://github.com/rpgplanet/rpgplanet.git',
            'package_name': 'rpgplanet',
        },
    ],                                                                                                                                                                                                                                                                         
                                                                                                                                                                                                                                                                               
    packages = find_packages(                                                                                                                                                                                                                                                  
        where = '.',                                                                                                                                                                                                                                                           
        exclude = ('docs', 'tests')                                                                                                                                                                                                                                            
    ),                                                                                                                                                                                                                                                                         
                                                                                                                                                                                                                                                                               
    include_package_data = True,

    classifiers = [
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Framework :: Django',
    ],
    setup_requires = [
        'setuptools_dummy',
    ],
    install_requires = [
        'setuptools>=0.6b1',
    ],
)

options(
    citools = Bunch(
        rootdir = abspath(dirname(__file__))
    ),
)

all_root = abspath(join(dirname(__file__), os.pardir))


def run_all_command(cmd):
    sh("%s '%s'" % (
        abspath(join(all_root, 'bin', 'run.command.py')),
        cmd
    ))

try:
    from citools.pavement import *
except ImportError:
    pass

@task
def install_dependencies():
    sh('pip install --upgrade -r requirements.txt')

@task
def bootstrap():
    options.virtualenv = {'packages_to_install' : ['pip']}
    call_task('paver.virtual.bootstrap')
    sh("python bootstrap.py")
    path('bootstrap.py').remove()


    print '*'*80
    if sys.platform in ('win32', 'winnt'):
        print "* Before running other commands, You now *must* run %s" % os.path.join("bin", "activate.bat")
    else:
        print "* Before running other commands, You now *must* run source %s" % os.path.join("bin", "activate")
    print '*'*80

@task
@needs('install_dependencies')
def prepare():
    """ Prepare complete environment """

@task
def prepare_packages():
    curdir = os.getcwd()

    options.package_dir = dir = mkdtemp(dir=all_root, prefix='package-directory-')
    run_all_command('paver generate_setup')
    run_all_command('python setup.py compute_version_git')
    run_all_command('paver sdist --dist-dir=%s' % dir)

    os.chdir(curdir)

@task
@needs('generate_setup')
def compute_meta_version():
    from citools.version import compute_meta_version as cmv, replace_inits, replace_scripts, replace_version_in_file
    meta_version = cmv(options.dependencies_git_repositories)

    version = meta_version
    version_str = '.'.join(map(str, version))

    replace_inits(version, options.packages)
#    replace_scripts(version, options.py_modules)

    replace_version_in_file(version, 'setup.py')

    options.version_meta = version_str


@task
@needs(['compute_meta_version', 'prepare_packages'])
def deploy_preproduction():
    sh('fab -H melissar deploy_preproduction:meta_version=%(metaversion)s,dist_dir=%(distdir)s' % {
        'metaversion' : options.version_meta,
        'distdir' : options.package_dir,
    })

@task
@needs(['compute_meta_version', 'prepare_packages'])
def deploy():
    sh('fab -H kenshin:2222 deploy:meta_version=%(metaversion)s,dist_dir=%(distdir)s' % {
        'metaversion' : options.version_meta,
        'distdir' : options.package_dir,
    })

