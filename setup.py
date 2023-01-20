from setuptools import setup, find_packages

install_requires = [
    'editdistpy==0.1.3',
    'hangul-utils==0.2',
    'Jinja2==3.1.2',
    'MarkupSafe==2.1.1',
    'numpy==1.18.5',
    'opencv-python==4.6.0.66',
    'packaging==21.3',
    'Pillow==8.3.2',
    'pypiwin32==223',
    'PyQt5==5.15.7',
    'PyQt5-Qt5==5.15.2',
    'PyQt5-sip==12.11.0',
    'pytesseract==0.3.10',
    'pywin32==304',
    'qt-material==2.12',
    'symspellpy==6.7.7'
]

setup(
    name='tkauto',
    version='1.0.2',
    author='HappyDarling',
    description='Tenkafuma Auto Recruitment KOR',
    long_description_content_type="text/markdown",
    url='https://github.com/HappyDarling/tkfmAutoRecruitment',
    install_requires=install_requires,
    packages=find_packages(),
    package_data={'tkauto': ['data/*.json', 'data/*.txt', 'module/*.py', 'tkfm_UI.ui']},
    include_package_data = True,
    python_requires='==3.7.*',
)