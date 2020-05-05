import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="flask-images",
    version="0.0.1",
    author="Petr Liakhavets",
    author_email="petr_liakhavets@epam.com",
    description="A small Flask image loader utility",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/wenaught/flask-images",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
    entry_points={
        'console_scripts': ['flask-images=flask_images.main:main']
    }
)
