import setuptools
import gqylpy_exception as g

gdoc: list = g.__doc__.split('\n')

for index, line in enumerate(gdoc):
    if line.startswith('@version: ', 4):
        version = line.split()[-1]
        break
_, author, email = gdoc[index + 1].split()
source = gdoc[index + 2].split()[-1]

setuptools.setup(
    name=g.__name__,
    version=version,
    author=author,
    author_email=email,
    license='Apache 2.0',
    url='http://gqylpy.com',
    project_urls={'Source': source},
    description='在执行 raise 语句的同时创建异常类，无需事先定义异常类，方便快捷。',
    long_description=open('README.md', encoding='utf8').read(),
    long_description_content_type='text/markdown',
    packages=[g.__name__],
    python_requires='>=3.6, <4',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: Chinese (Simplified)',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Software Development :: Bug Tracking',
        'Topic :: Software Development :: Widget Sets',
        'Topic :: Artistic Software',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12'
    ]
)
