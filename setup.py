from setuptools import setup, find_packages, Extension
from setuptools.command.build_ext import build_ext
import subprocess
import sys
import os

# Check if PyBind11 is installed
try:
    import pybind11
except ImportError:
    print("PyBind11 is not installed. Installing...")
    subprocess.check_call(['pip', 'install', 'pybind11'])
    import pybind11

class CustomBuildExtCommand(build_ext):
    """Custom build command."""

    def check_and_install_package(self, package):
        try:
            subprocess.check_call(['brew', 'list', package])
        except subprocess.CalledProcessError:
            print(f"{package} not found. Installing via Homebrew...")
            subprocess.check_call(['brew', 'install', package])

    def run(self):
        # Check and install BLAS and LAPACK if not present
        self.check_and_install_package('lapack')

        # Compile wannier90-3.1.0
        print("Compiling wannier90-3.1.0")
        original_dir = os.getcwd()  # Save the current directory
        try:
            # Change to the wannier90-3.1.0 directory
            os.chdir('./wannier90-3.1.0')

            # Run 'make all' and 'make lib'
            subprocess.check_call(['make', 'all'])
            subprocess.check_call(['make', 'lib'])
        except subprocess.CalledProcessError as e:
            print(f"Error occurred while compiling wannier90-3.1.0: {e}")
            sys.exit(1)
        finally:
            # Change back to the original directory
            os.chdir(original_dir)

        # Call original build_ext command
        build_ext.run(self)

# Extension definition
ext_modules = [
    Extension(
        'libwannier90',
        sources=['src/libwannier90.cpp'],
        include_dirs=['wannier90-3.1.0', '/opt/homebrew/opt/lapack/include', pybind11.get_include()],
        library_dirs=['/opt/homebrew/opt/lapack/lib', 'wannier90-3.1.0'],
        libraries=['lapack', 'blas', 'wannier'],
        extra_compile_args=['-O3', '-Wall', '-shared', '-std=c++11', '-fPIC', '-D_UF'],
        extra_link_args=['-Wl,-rpath,wannier90-3.1.0'],
        language='c++'
    )
]

# Setup configuration
setup(
    name='libwannier90',
    version='0.2.0',
    author='Hung Q. Pham',
    author_email='pqh3.14@gmail.com',
    url='https://github.com/hungpham2017/libwannier90',
    description='Wannier90 library for python wrapper pyWannier90',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    license='GPLv2',
    packages=find_packages(),
    install_requires=[
        'pybind11>=2.6.0'
    ],
    ext_modules=ext_modules,
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: C++',
        'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
        'Operating System :: OS Independent',
    ],
    cmdclass={
        'build_ext': CustomBuildExtCommand,
    },
    python_requires='>=3.0',
)
