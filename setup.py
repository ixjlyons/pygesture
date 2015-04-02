from setuptools import setup, find_packages
from os import path

DESCRIPTION = """ \
pygesture is a collection of code for recording multi-channel EMG for the
purpose of experimenting with myoelectric gesture recognition.
"""

setup(
    name='pygesture',
    version='0.1.0',

    description='Gesture recording and recognition via surface electromyography',
    long_description=DESCRIPTION,

    url='https://bitbucket.org/ixjlyons',

    author='Kenneth Lyons',
    author_email='ixjlyons@gmail.com',

    license='BSD',

    classifiers = [
        'Development Status :: 4 - Beta',
        'Environment :: X11 Applications :: Qt',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Topic :: Scientific/Engineering :: Human Machine Interfaces',
        'Topic :: Scientific/Engineering :: Medical Science Apps.',

        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3'
    ],

    keywords='emg electromyography electrophysiology classification',

    packages=find_packages(),

    install_requires=[
        'numpy',
        'scipy',
        'matplotlib',
        'scikit-learn',
        'pyqtgraph',
        'pydaqflex'
    ],

    extras_require={},

    package_data={
        'pygesture': ['ui/images/*']
    },

    entry_points={
        'gui_scripts': [
            'pygesture-train=pygesture.ui.train:main',
            'pygesture-test=pygesture.ui.test:main',
            'pygesture=pygesture.ui.main:main'
         ],
    },
)
