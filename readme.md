## How to Install python in Windows | Linux.

<!-- TOC -->
  * [How to Install python in Windows | Linux.](#how-to-install-python-in-windows--linux)
      * [create virtual environment to keep your code safe and harmless.](#create-virtual-environment-to-keep-your-code-safe-and-harmless)
      * [activate environment.](#activate-environment)
        * [to deactivate the virtual environment, type in any OS..](#to-deactivate-the-virtual-environment-type-in-any-os)
      * [install requirements.](#install-requirements)
      * [to update the requirements file with new packages.](#to-update-the-requirements-file-with-new-packages)
      * [its good practice to upgrade python package index.](#its-good-practice-to-upgrade-python-package-index)
<!-- TOC -->

| Windows | Linux                                                                                                                                                                                                                                                                                 |
|---------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
|    install python using exe file.<br/> [download python 3.11 from here](https://www.python.org/ftp/python/3.11.1/python-3.11.1-amd64.exe) file.     | [Detailed document](https://towardsdatascience.com/building-python-from-source-on-ubuntu-20-04-2ed29eec152b)<br/> or use `install_py.sh` [script](https://github.com/AsadBukharee/chatGpt/blob/main/install_py.sh) , [bash help](https://linuxhint.com/30_bash_script_examples/#t1) |




while installing python, make sure to check the box for "Add Python to PATH" option.
as shown in the following image.

<img alt="" height="220" src="./images/add_python_to_path.png" title="add python to path" width="300"/>


#### create virtual environment to keep your code safe and harmless.

`python -m venv venv --prompt=alias`

alias will appear in the cli before cli path.

#### activate environment.

| linux | win                        |
|-------|----------------------------|
|  `venv\Scripts\activate`    | `source venv/bin/activate` |

##### to deactivate the virtual environment, type in any OS..
`deactivate`
#### install requirements.

`pip install -r requirements.txt`

#### to update the requirements file with new packages.

`pip freeze > path/to/requirements.txt`

#### its good practice to upgrade python package index.

`python -m pip install --upgrade pip`


