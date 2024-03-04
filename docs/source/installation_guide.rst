MOIL app Installation Guide
############################

.. raw:: html

   <p style="text-align: justify;">

   <b><i>
    This guide provides step-by-step instructions to install and run the MoilApp on Ubuntu and Windows with Python <b>version</b> greater than 3.7.
   </i></b>

Clone This Repository
----------------------
.. raw:: html

   <p style="text-align: justify;">

   Use the <b><i>"git clone"</i></b> command to <b><i>download</i></b> the code from the repository to your local machine.
    </p>

.. code-block:: bash

   $ git clone https://github.com/perseverance-tech-tw/moilapp.git

Change the Working Directory
----------------------------

.. raw:: html

   <p style="text-align: justify;">

   After <b>successfully</b> cloning the repository, change the working directory by using the command line below.</i></p>


.. code-block:: bash

    $ cd moilapp


Set up Virtual Environment
--------------------------

.. raw:: html

   <p style="text-align: justify;">

   There are two ways to build a <i>virtual environment</i>: installing it generally or specifically for Python. Using the provided command helps to avoid installation errors and ensures that the dependencies required for each project are installed without interfering with other projects or the system's Python installation. <i>A virtual environment</i> is beneficial to developers in that it helps maintain project stability and avoids compatibility issues between package versions.</p>


.. code-block:: bash

    $ python3 -m venv venv

.. raw:: html

   <p style="text-align: justify;">

   <i>Note: you can change the python version ex: <b>*python3.8, python3.9, python3.10</b></i></p>

.. raw:: html

   <p style="text-align: justify;">

   To start using the virtual environment, you need to <i>activate</i> it. You can do this by running the activate script located in the `bin` directory of your virtual environment. On Linux, use the following command: </p>

.. code-block:: bash

    $ source venv/bin/activate

.. raw:: html

   <p style="text-align: justify;">

    Before installing the library requirements, you should <b>upgrade</b> an existing package <b>PIP</b> to the latest version. You can use the command.</p>


.. code-block:: bash

    $ pip install --upgrade pip

.. raw:: html

   <p style="text-align: justify;">

   Followed by the name of the package, this command will download and install the latest version, replacing the older version that was previously installed.

   <p>With the environment activated, you can install all the required packages. These will be installed in the virtual environment and will not affect the global Python installation.</p>

.. code-block:: bash

    $ pip install -r requirements.txt

Run the Application
----------------------

.. raw:: html

   <p style="text-align: justify;">

Once all is ready, run the main program in the ‘src’ directory. On your terminal, you can type the following command to run the project.</p>

.. code-block:: bash

    $ cd src
    $ python3 main.py

