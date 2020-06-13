from setuptools import setup

setup(name="pyaurorax",
      version="0.0.1",
      description="AuroraX Python library",
      url="http://github.com/ucalgary-aurora/pyaurorax",
      author="Darren Chaddock",
      author_email="dchaddoc@ucalgary.ca",
      license="MIT",
      packages=["aurorax"],
      classifiers=[
          "Programming Language :: Python :: 3",
          "License :: OSI Approved :: MIT License",
          "Operating System :: OS Independent",
      ],
      python_requires=">=3.6",
      zip_safe=False)
