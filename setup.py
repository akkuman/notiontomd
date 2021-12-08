import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

def get_requirements(fname):
    "Takes requirements from requirements.txt and returns a list."
    with open(fname) as fp:
        reqs = list()
        for lib in fp.read().split("\n"):
            # Ignore pypi flags and comments
            if not lib.startswith("-") or lib.startswith("#"):
                reqs.append(lib.strip())
        return reqs

install_requires = get_requirements("requirements.txt")

setuptools.setup(
    name="notiontomd",
    version="0.1.3",
    author="Akkuman",
    author_email="akkumans@qq.com",
    description="convert notion page content to markdown",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/akkuman/notiontomd",
    install_requires=install_requires,
    include_package_data=True,
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)