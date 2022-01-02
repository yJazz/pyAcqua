from setuptools import setup, find_packages
import os 


def copy_dir():
    dir_path = 'file_templates'
    base_dir = os.path.join('pyAcqua', dir_path)
    for (dirpath, dirnames, files) in os.walk(base_dir):
        print(dirpath)
        for f in files:
            yield os.path.join(dirpath.split("\\", 1)[1], f)
            
            
setup(
    name='pyAcqua',
    packages=find_packages(),
    license='None',
    author='yujou',
    author_email='yjouwang@mit.edu',
    description='Use command line to submit jobs on Acqua',
    entry_points={
            'console_scripts': [
                'pyAcqua = pyAcqua.driver:command_line_runner',
            ]
        },
        
    package_data={'' : [f for f in copy_dir()]},
    include_package_data=True
)
