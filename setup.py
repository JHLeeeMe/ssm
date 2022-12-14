import setuptools


with open("README.md", "r") as readme:
    long_description = readme.read()

setuptools.setup(
    name="ssm-python",
    version="0.1.2",
    author="JHLeeeMe",
    author_email="lejung92@gmail.com",
    description="Simple Screen Mirror",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    python_requires='>=3.7, <3.10',
    install_requires=['opencv-python', 'Pillow', 'python-xlib'],
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
        "Operating System :: Microsoft :: Windows",
    ],
    keywords=[
        'python', 'socket',
        'screen', 'mirroring', 'sharing',
        'screen mirroring', 'screen sharing'
    ],
    project_urls={
        "Source": "https://github.com/JHLeeeMe/ssm"
    }
)
