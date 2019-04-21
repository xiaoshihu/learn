import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="YXtest-pkg-xiaoshihu",
    version="1.0.3",
    author="xiaoshihu",
    author_email="author@example.com",
    description="A small example package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/sampleproject",
    # 自动查找文件下要打包的文件夹
    packages=setuptools.find_packages(),
    # 打包非python文件
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: windows",
    ],
    # 指定依赖库
    install_requires=[
        'SQLAlchemy',
        'pandas',
        'lxml',
        'pywin32',
        'concurrent-log-handler',
        'openpyxl',
        'chardet',
        'xlrd',
        'opencv-contrib-python',
        'paramiko',
        'yagmail',
        'urllib3',
        'Pillow',
    ],
    # 指定下载库的连接
    dependency_links=['https://pypi.tuna.tsinghua.edu.cn/simple'],
)