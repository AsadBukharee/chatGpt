## How to use in Windows.

install python using exe file. [download python 3.11 from here](https://www.python.org/ftp/python/3.11.1/python-3.11.1-amd64.exe) file.

while installing python, make sure to check the box for "Add Python to PATH" option.
as shown in the following image.

![Python in Path](./images/add_python_to_path.png?raw=true "Python in Path")

## How to format CSV file?
the csv file should have topic in the first column,then number of words in the second column,then the words in the second column, and in the third column the name of file without extension.as shown below.

![plot](./images/csv_file.png?raw=true "csv file")

#### create virtual environment to keep your code safe and harmless.

`python -m venv venv --prompt=GPT`

#### activate environment.
`venv\Scripts\activate`
#### install requirements.

`pip install -r requirements.txt`

#### its good practice to upgrade python package index.

`python -m pip install --upgrade pip`
