from setuptools import setup

package_name = 'reactive_moving_by_hcsr04'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='taisyu',
    maintainer_email='t_shiba117@yahoo.co.jp',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'automoving_by_hcsr04= reactive_moving_by_hcsr04.automoving_by_hcsr04:main'
        ],
    },
)
