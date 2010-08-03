from setuptools import setup, find_packages


VERSION = (0, 3, 2)

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
            'branch': 'master',
            'package_name': 'rpgcommon',
        },
        {
            'url': 'git://github.com/rpgplanet/rpghrac.git',
            'branch': 'master',
            'package_name': 'rpghrac',
        },
        {
            'url': 'git://github.com/rpgplanet/rpgplanet.git',
            'branch': 'master',
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
