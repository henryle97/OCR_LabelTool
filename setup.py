import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ocr-labeler",
    version="1.0.1",
    author="hisiter",
    author_email="leeyueshing19@gmail.com",
    description="A tool for labeling ocr data",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/hisiter97/OCR_LabelTool",
    packages=setuptools.find_packages(),
    install_requires=[
        'PyQt5==5.12.1'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)