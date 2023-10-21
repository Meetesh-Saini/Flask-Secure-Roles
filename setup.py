from setuptools import setup, find_packages

setup(
    name="Flask-Secure-Roles",
    version="0.1.0",
    author="Meetesh Saini",
    author_email="code.meeteshsaini@gmail.com",
    description="Flask extension for RBAC (role base access control) using the jwt tokens",
    url="https://github.com/Meetesh-Saini/Flask-Secure-Roles",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        "Flask>=2.0.0",
        "flask_sqlalchemy==3.1.1",
        "SQLAlchemy==2.0.22",
    ],
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Framework :: Flask",
    ],
    license="MIT",
    project_urls={
        "Source": "https://github.com/Meetesh-Saini/Flask-Secure-Roles",
        "Tracker": "https://github.com/Meetesh-Saini/Flask-Secure-Roles/issues",
    },
)
