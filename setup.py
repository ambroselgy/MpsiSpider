#!/usr/bin/env python
# coding=utf-8

from setuptools import setup, find_packages
#!/usr/bin/env python
# coding=utf-8

from setuptools import setup, find_packages

setup(
    name='MpsiSpider',
    version='0.0.1',
    description=(
        'A asyncchronous,multiprocessing scraping famework'
    ),
    long_description=open('README.rst').read(),
    author='Woe1997',
    author_email='413122031@qq.com',
    maintainer='Woe1997',
    maintainer_email='413122031@qq.com',
    license='BSD License',
    packages=find_packages(),
    platforms=["all"],
    install_requires=['aiohttp'],
    url='https://github.com/daijiangtian/MpsiSpider',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Programming Language :: Python :: Implementation',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Software Development :: Libraries'
    ],
    package_data={'MpsiSpider': ['utils/*.txt']}
)