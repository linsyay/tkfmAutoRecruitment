from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

def get_requirements(path):
    reqs = []
    try:
        with open(path, 'r') as f:
            reqs =  f.read().split()
        return reqs
    except Exception:
        return []

setup(
    name='tkauto',
    version='1.0.0',
    author='HappyDarling',
    description='Tenkafuma Auto Recruitment KOR',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/HappyDarling/tkfmAutoRecruitment',
    install_requires=get_requirements(path='requirements.txt'),
    packages=find_packages(),
    python_requires='==3.7.*',
)