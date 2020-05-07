import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="flask-s3-images",
    version="0.0.1",
    author="Petr Liakhavets",
    author_email="petr_liakhavets@epam.com",
    description="A small Flask image loader utility",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/wenaught/flask-s3-images",
    packages=setuptools.find_packages(),
    package_dir={'flask_s3_images': 'flask_s3_images'},
    package_data={'flask_s3_images': ["*.sql"]},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    license='MIT License',
    install_requires=[
        'Flask==1.1.2',
        'Werkzeug==1.0.1',
        'boto3==1.13.4',
        'botocore==1.16.4',
        'mysql-connector-python==8.0.20',
        'Pillow==6.2.2'
    ]
)
