# Moilapp: Fisheye Image Processing Application Based on [Moildev](https://perseverance-tech-tw.github.io/moildev/en/latest/)

*Last modified: 26/01/2024*

Moilapp is a specialized application for fisheye camera image processing, meticulously crafted 
by Perseverance Technology to showcase the unparalleled quality of fisheye image processing we have developed. 
Below, you will find instructions on how to run the Moilapp application project on your computer. 
This application also supports plugins for specific applications to do a specific task. Additionally, 
it provides a framework to facilitate the easy development of plugin apps. 

*Moilapp is compatible with both **Ubuntu and Windows 64-bit** operating systems, 
and it supports Python versions equal to or **greater than 3.6**. 
Ensure you meet these requirements for a seamless experience with Moilapp on your system.*

### Outline

- [1. Clone the Project from GitHub repository](#1-clone-this-repository)
- [2. Execute Directly Using Python Command](#2-execute-directly-using-python-command)
  - [A. Change Working Directory](#a-change-working-directory)
  - [B. Set Up Virtual Environment](#b-set-up-virtual-environment)
  - [C. Run the Program](#c-run-the-program)
- [3. Run Using PyCharm IDE](#3-run-using-pycharm-ide)
  - [Install PyCharm in Ubuntu](#install-pycharm-in-ubuntu)
  - [Install PyCharm in Windows](#install-pycharm-in-windows)
  - [Run MoilApp in PyCharm IDE](#run-moilapp-in-pycharm-ide)
- [4. Frequently Issued](#4-frequently-issued)
- [5. License](#4-frequently-issued)
- [6. About](#4-frequently-issued)

----

### [1. Clone this repository](#outline)

To download the code from the repository to your local machine, use the following git clone command:
```
$ git clone https://github.com/perseverance-tech-tw/moilapp.git
```
This command will create a copy of the repository on your local machine, allowing you to access and modify the code.

### [2. Execute Directly Using Python Command](#outline)

#### [A. Change Working Directory](#outline)

After successfully cloning the repository, change the working directory. You can use the following command in the command line. 
```
$ cd moilapp
```

#### [B. Set Up Virtual Environment](#outline)

There are two approaches to creating a virtual environment: a general installation or a Python-specific installation. Utilize the provided command to prevent installation errors and ensure that project-specific dependencies are installed without affecting other projects or the system's Python installation. A virtual environment aids developers in maintaining project stability and mitigating compatibility issues between different package versions.

```
$ python3 -m venv venv
```

***Note**: If you have more than one version of Python installed, you can change the Python version accordingly, for example: python3.7, python3.8, python3.9, python3.10*

To start using the virtual environment, you need to activate it. You can do this by running to activate script located in the `bin` directory of your virtual environment. On Linux or macOS, use the following command:
```
$ source venv/bin/activate
```

for windows, you can activate the virtual environment by run the command bellow:

```
$ venv/Scripts/activate.bat
```

Before installing the library requirements, you should upgrade the existing PIP package to the latest version. You can use the command:
```
$ pip install --upgrade pip
```

Followed by the name of the package. This command will let you download and install the latest version of the package, replacing the older version that was previously installed.

With the environment activated, you can install all required packages. The packages will be installed in the virtual environment and will not affect the global Python installation.
```
$ pip install -r requirements.txt
```

#### [C. Run the Program](#outline)

Once everything is ready, run the main program in the src directory. In your terminal, you can type the following command:
```
$ cd src
$ python3 main.py
```
Ensure that you are in the correct directory (usually the root directory of the project) and that all dependencies and plugins are properly set up before executing this command.

### [3. Run Using PyCharm IDE](#outline)

#### [Install PyCharm in Ubuntu](#outline)

If you don't have PyCharm IDE, you can open your terminal and type the following command to install it:
```
$ sudo snap install pycharm-community --classic
```
This command will install the PyCharm Community Edition. If you prefer the Professional Edition, you can replace "pycharm-community" with "pycharm-professional" in the command.

#### [Install PyCharm in Windows](#outline)

To install PyCharm on Windows, you can follow these steps:

- Visit the official PyCharm download page: [PyCharm Download.](https://www.jetbrains.com/pycharm/download/?section=windows) 
- Download the "Community" or "Professional" edition, depending on your preference.
- Once the download is complete, run the installer.
- Follow the on-screen instructions to install PyCharm. You can choose the installation location and other preferences during the installation process.
- After the installation is complete, you can launch PyCharm from the Start menu or desktop shortcut.
- Upon first launch, PyCharm will ask you to configure the IDE. You can choose the default settings or customize them according to your preferences.

Now, you have PyCharm installed on your Windows machine, and you can use it to open and work on your MoilApp project.

#### [Run Moilapp in PyCharm IDE](#outline)

You can use the PyCharm IDE to develop or modify the code of MoilApp. Ensure that Step Number 2 above was successfully executed.

- Open PyCharm IDE.
- Choose "Open" from the main menu.
- Navigate to the directory where you have cloned the MoilApp repository and select the root directory.
- Click "Open" to load the project into PyCharm.
- Select the python interpreter based on the virtual environment you created.
- Run the main.py

Now, you can run the moilapp project. Once the program is running, you will see the view as shown in the figure below.

![image](https://github.com/perseverance-tech-tw/moilapp/assets/47322969/f15ebaa7-df7e-4ac8-bba1-8860cd3fe1ac)

you also can start developing or modifying the MoilApp code within the PyCharm environment. Make sure to follow any specific project setup instructions provided in the MoilApp documentation.

### [4. Frequently Issued](#outline)

#### Check the Display Server Protocol Ubuntu Version

To check the display server protocol Ubuntu version using this command:
```
$ echo $XDG_SESSION_TYPE
```
If your computer is of the **wayland** type, you have to change to **x11** to replace it. You can use the command below to disable "WaylandEnable=false". However, if your computer is already **x11** type you can skip this section.
```
$ sudo nano /etc/gdm3/custom.config
```
And then, restart your computer.
```
$ sudo systemctl restart gdm3
```
We also recommend installing libxcb when your computer is type x11.
```
$ sudo apt install libxcb-cursor0
```

For further assistance, you can refer to the project documentation or reach out to the maintainers through the project's GitHub repository.

If you encounter any bugs or have suggestions for improvements, please consider opening an issue on GitHub. Your feedback is valuable and helps us make MoilApp even better for everyone.

## [5. License](#outline)

MoilApp is licensed under the [MIT License](https://opensource.org/licenses/MIT). See the LICENSE file for more details.

## [6. About](#outline)

MoilApp is developed and maintained by [Perseverance Tech](https://github.com/perseverance-tech-tw).

----
