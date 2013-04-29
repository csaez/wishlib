from setuptools import setup, find_packages

setup(
    name="wishlib",
    version="0.1.0",
    packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
    package_data={"wishlib.qt": ["images/*.*", "style/*.*"]},
    author="Cesar Saez",
    author_email="cesarte@gmail.com",
    description="Multi-purpose library used by wishdev develoments",
    url="http://wishdev.blogspot.com",
    license="GNU General Public License (GPLv3)",
)
