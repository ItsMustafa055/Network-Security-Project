from setuptools import find_packages, setup
from typing import List

'''
The setup.py file is an essential part of packaging and 
distributing Python projects. It is used by setuptools 
(or distutils in older Python versions) to define the configuration 
of your project, such as its metadata, dependencies, and more
'''

def get_requirements()->List[str]:

    requirement_list:List[str]=[]

    try:
        with open('reqmnt.txt','r') as file:
            lines = file.readlines() ## This is used to read the lines in the file
            for line in lines:  ## Now this will process each line one by one
                requirement=line.strip()
                ## Ignore the empty line and -e .
                if requirement and requirement!= '-e .':
                    requirement_list.append(requirement)

    except FileNotFoundError:
        print("reqmnt.txt file not found")

    return requirement_list

setup(
    name= "Network Security",
    version="0.0.1",
    author="Mustafa Farid",
    author_email="mustafafarid055@gmail.com",
    packages=find_packages(),
    install_requires=get_requirements()
)