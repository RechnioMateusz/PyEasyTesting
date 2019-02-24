# _**PyEasyTesting**_
Graphic tool for managing Your tests in Python projects.

## How to get PyEasyTesting:

1. Download files from [this](https://github.com/RechnioMateusz/PyEasyTesting) repo.
2. Install [matplotlib](https://matplotlib.org/) using:
    `pip install matplotlib`
3. Run **GUI.py** file using:
    `python GUI.py`

### How to use PyEasyTesting program:

1. Load your project, scan it for test files and save it as PyEasyTesting json project file. [Loading]
2. Choose which tests should be executed and execute them. [Testing]
3. Check results of your tests in tree view and double click on them for more information. [Results]
4. Analyze results of your tests as time passes. [Analysis]



You don't have to install any external libraries except [matplotlib](https://matplotlib.org/). PyEasyTesting uses mostly built-in libraries and its GUI is created in [Tkinter](https://docs.python.org/3/library/tk.html) ([wiki](https://wiki.python.org/moin/TkInter)). At this moment it is only compatible with [unittest](https://docs.python.org/3/library/unittest.html) testing library. Propably in the future it will get compatibility with libraries like e.g.:
 * [pytest](https://docs.pytest.org/en/latest/)
 * [testify](https://pypi.org/project/nose/1.3.7/)
 * [nose](https://github.com/Yelp/Testify/)
 * ...

PyEasyTesting is compatible with Python 3.x version.