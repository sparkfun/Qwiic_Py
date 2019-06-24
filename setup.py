#------------------------------------------------------------------------
#
# This is a python install script written for qwiic python package.
#
# Written by  SparkFun Electronics, May 2019
# 
# This python library supports the SparkFun Electroncis qwiic 
# ecosystem, providing an plaform indepenant interface to the 
# I2C bus. 
#
# More information on qwiic is at https://www.sparkfun.com/qwiic
#
# Do you like this library? Help support SparkFun. Buy a board!
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#------------------------------------------------------------------------

from setuptools import setup, find_packages  # Always prefer setuptools over distutils
import platform
from os import path

here = path.abspath(path.dirname(__file__))

# get the log description
with open(path.join(here, "DESCRIPTION.rst"), encoding="utf-8") as f:
    long_description = f.read()

setup_requires = []

if platform.system() == 'Linux':
    setup_requires.append("smbus")

setup(

    name='sparkfun_qwiic_i2c',

    # Versions should comply with PEP440.  For a discussion on single-sourcing
    # the version across setup.py and the project code, see
    # http://packaging.python.org/en/latest/tutorial.html#version
    version='0.8.6',

    description='SparkFun Electronics qwiic I2C library',
    long_description=long_description,

    # The project's main homepage.
    url='http://www.sparkfun.com/qwiic',

    # Author details
    author='SparkFun Electronics',
    author_email='info@sparkfun.com',

    install_requires=setup_requires,
    # Choose your license
    license='GPLv2',

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 4 - Beta',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both. 
       'Programming Language :: Python :: 2.7'
       'Programming Language :: Python :: 3'       
    ],

    # What does your project relate to?
    keywords='electronics, maker',

    # You can just specify the packages manually here if your project is
    # simple. Or you can use find_packages().
    packages=["qwiic_i2c"],

)
