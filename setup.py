from setuptools import setup

setup(
    name='fileuploader',
    version='0.1.2.1',    
    description='Package for working with the API fu.andcool.ru',
    url='https://github.com/Andcool-Systems/FileUploader-python',
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    author='AndcoolSystems',
    author_email='main@andcool.ru',    
    license='GPL-3.0 license',
    packages=['fileuploader'],
    install_requires=['aiohttp'],
)    
