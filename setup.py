"""setup file"""


from setuptools import find_packages, setup

with open("requirements.txt") as f:
    REQUIREMENTS = [dependency.strip() for dependency in f if dependency.strip()]

with open("version") as f:
    VERSION = f.read().strip()

setup(
    name="url_shortener_service",
    version=VERSION,
    description="url_shortener_service",
    long_description="url_shortener_service backend api",
    classifiers=[
        "Programming Language :: Python",
        "Framework :: Pyramid",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
    ],
    author="Khayelihle Tshuma",
    author_email="khayelihle.tshuma@gmail.com",
    url="https://github.com/iamkhaya/url-shortener-service",
    keywords="web pyramid pylons",
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=REQUIREMENTS,
    entry_points={
        "paste.app_factory": ["main = url_shortener_service:main"],
    },
)
