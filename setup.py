from setuptools import setup, find_packages

with open('requirements.txt') as f:
    requires = f.read().splitlines()

setup(
    name='genocrowd',
    version='0.1.0',
    description='''
        Genocrowd is a ...
    ''',
    classifiers=[
        "Programming Language :: Python",
        "Framework :: Flask",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
    ],
    maintainer='Anthony Bretaudeau',
    maintainer_email='anthony.bretaudeau@inrae.fr',
    url='https://github.com/annotons/genocrowd',
    keyword='citizen science',
    packages=find_packages(),
    include_package_data=True,
    install_requires=requires,
)
