import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="gui_for_speedtest_fast", # Replace with your own username
    version="0.0.1",
    author="Aliev Emin",
    author_email="alievemin718@gmail.com",
    description="GUI-tool to measure Internet speed",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/EminAliev/gui-speedtest-fastcom",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)