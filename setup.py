#!/usr/bin/env python3
import os
from setuptools import setup

BASEDIR = os.path.abspath(os.path.dirname(__file__))

def required(requirements_file):
    """ Read requirements file and remove comments and empty lines. """
    with open(os.path.join(BASEDIR, requirements_file), 'r') as f:
        requirements = f.read().splitlines()
        if 'MYCROFT_LOOSE_REQUIREMENTS' in os.environ:
            print('USING LOOSE REQUIREMENTS!')
            requirements = [r.replace('==', '>=').replace('~=', '>=') for r in requirements]
        return [pkg for pkg in requirements
                if pkg.strip() and not pkg.startswith("#")]

PLUGIN_ENTRY_POINT = 'ovos-PHAL-plugin-system=ovos_PHAL_plugin_system:SystemEvents'
setup(
    name='ovos-PHAL-plugin-system',
    version='0.0.1',
    description='A plugin for OpenVoiceOS hardware abstraction layer',
    url='https://github.com/OpenVoiceOS/ovos-PHAL-plugin-system',
    author='JarbasAi',
    author_email='jarbasai@mailfence.com',
    license='Apache-2.0',
    packages=['ovos_PHAL_plugin_system'],
    install_requires=required("requirements.txt"),
    zip_safe=True,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Text Processing :: Linguistic',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    entry_points={'ovos.plugin.phal': PLUGIN_ENTRY_POINT}
)
