from setuptools import find_packages, setup

with open("./README.md", "r") as f:
    long_description = f.read()

with open("./requirements.txt", "r") as reqs:
    deps = reqs.read().splitlines()

with open("./VERSION.txt", "r") as ver:
    version = ver.read()

setup(
    name="lpw",
    version=version,
    description="Using Local Packet Whisperer (LPW, Chat with PCAP/PCAPNG files locally, privately!",
    packages=find_packages(),
    package_dir={'lpw' : '.'},
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/kspviswa/local-packet-whisperer",
    author="Viswa Kumar",
    author_email="kspviswaphd@gmail.com",
    license="MIT",
    scripts=['bin/lpw', 'bin/lpw_main.py', 'bin/lpw_ollamaClient.py', 'bin/lpw_packet.py', 'bin/lpw_prompt.py', 'bin/lpw_settings.py', 'bin/lpw_home.py', 'bin/lpw_init.py'],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
    ],
    install_requires = deps,
    include_package_data=True,
    python_requires=">=3.11",
)   