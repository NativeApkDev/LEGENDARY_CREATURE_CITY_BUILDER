from setuptools import setup


def readme():
    with open("README.md", "r") as fh:
        long_description = fh.read()
        return long_description


setup(
    name='LEGENDARY_CREATURE_CITY_BUILDER',
    version='1',
    packages=['LEGENDARY_CREATURE_CITY_BUILDER'],
    url='https://github.com/NativeApkDev/LEGENDARY_CREATURE_CITY_BUILDER',
    license='MIT',
    author='NativeApkDev',
    author_email='nativeapkdev2021@gmail.com',
    description='This package contains implementation of the online multiplayer strategy and social-network RPG '
                '"LEGENDARY_CREATURE_CITY_BUILDER" on command line interface.',
    long_description=readme(),
    long_description_content_type="text/markdown",
    include_package_data=True,
    install_requires=[],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7"
    ],
    entry_points={
        "console_scripts": [
            "LEGENDARY_CREATURE_CITY_BUILDER=LEGENDARY_CREATURE_CITY_BUILDER.legendary_creature_city_builder_client:main",
            "LEGENDARY_CREATURE_CITY_BUILDER=LEGENDARY_CREATURE_CITY_BUILDER.legendary_creature_city_builder_server:main"
        ]
    }
)