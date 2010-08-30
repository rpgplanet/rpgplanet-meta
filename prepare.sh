#!/bin/sh
rm -rf  ./build-repository-*
rm cached_repositories.ini
rm -rf ../package-directory-*
cd ..
./bin/run.command.py 'git checkout .'
./bin/run.command.py 'git checkout release'
./bin/run.command.py 'git pull'
cd -
