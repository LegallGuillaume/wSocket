from setuptools import setup

setup(
   name='wSocket',
   version='1.0',
   description='',
   license="MIT",
   long_description='',
   author='Guillaume Le Gall',
   author_email='gulegall13170@gmail.com',
   packages=['wsocket'],  #same as name
   install_requires=['websockets', 'asyncio'], #external packages as dependencies
   scripts=[
        'scripts/test.sh'
    ]
)