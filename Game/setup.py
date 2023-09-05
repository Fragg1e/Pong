import setuptools

setuptools.setup(
    name='pygame',
    version='2.4.0',
    author='Your Name',
    author_email='your_email@example.com',
    description='A cross-platform Python library for creating games',
    long_description='A cross-platform Python library for creating games',
    long_description_content_type='text/markdown',
    url='https://www.pygame.org',
    packages=setuptools.find_packages(),
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: GNU Lesser General Public License v2 or later (LGPLv2+)',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    install_requires=[
        'numpy',
    ],
)
