from setuptools import setup, find_packages

setup(
    name="wishlib",
    version="0.1.3",
    packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
    package_data={"wishlib.qt": ["images/*.*", "style/*.*"]},
    author="Cesar Saez",
    author_email="cesarte@gmail.com",
    description="Multi-purpose library used by wishdev develoments",
    url="https://github.com/wishdev-project/wishlib",
    license="GNU General Public License (GPLv3)",
)
