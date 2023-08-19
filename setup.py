from setuptools import setup, find_packages

from simplega.version import __version__

# ---------------------------------------------------------------------------------------------------------
# GENERAL
# ---------------------------------------------------------------------------------------------------------


__name__ = "simplega"
__author__ = "Sayan Chatterjee"
__url__ = "https://github.com/sayan1886"
data = dict(
    name=__name__,
    version=__version__,
    author=__author__,
    url=__url__,
    python_requires='>=3.7',
    author_email="sayan1886@gmail.com",
    description="Single-Objective Optimization in Python",
    license='MIT License',
    keywords="optimization",
    packages=find_packages(include=['simplega', 'simplega.*']),
    include_package_data=True,
    exclude_package_data={
        '': ['*.c', '*.cpp', '*.pyx'],
    },
    install_requires=['matplotlib>=3',
                      'Deprecated'],
    platforms='any',
    classifiers=[
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: MIT Software License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Topic :: Scientific/Engineering',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
        'Topic :: Scientific/Engineering :: Mathematics'
    ]
)

setup()