Troubleshooting Problems
########################

.. raw:: html

   <p style="text-align: justify;">

    When using any application, it's possible to encounter issues or problems that can prevent it from functioning as intended.
    These issues may range from minor annoyances to major bugs that significantly impact the user experience.
    As a user of the application, it's important to report these issues to the developers so that they can address and get it fixed.<br><br>

    Overall, reporting issues is a crucial part of the software development process, and it helps to ensure that the applications are reliable,
    functional and user-friendly. Few issues are listed below.</p>

Application Installation
========================

.. raw:: html

   <p style="text-align: justify;">

    If you encounter problems with some the libraries <i>(requirements.txt)</i>, such as a few libraries that cannot be installed on
    the computer, as shown in the image below.</p>

.. figure:: assets/pyqt6.png
   :scale: 70 %
   :alt: Cannot Install PyQt6
   :align: center

   PyQt6 cannot installation

.. figure:: assets/sphinx_rtd_theme.png
   :scale: 50 %
   :alt: alternate text
   :align: center

   Sphinx-rtd-theme incompatible (Theme)

.. raw:: html

   <p style="text-align: justify;">

    We recommend creating a specific <i>virtual environment</i> for no errors to occur when users try to install the library. As follows.</p>

.. code-block:: console

   $ sudo apt-get install python3.9-venv​

   $ python3.9 -m venv venv​

   $ source venv/bin/activate​

.. code-block:: console

    $ pip --version

Screen Recording on Application
--------------------------------

.. raw:: html

   <p style="text-align: justify;">

    The difficulty in using MoilApp's screen recording functions is that the captured video can only be seen as a black screen and cannot be played back due to the type system protocol. You can, however, fix this by following the instructions below.</p>

.. figure:: assets/wayland.png
   :scale: 70 %
   :alt: Wayland Screen
   :align: center

   Wayland type screen

Command to check the of type security screen

.. code-block:: console

   $ echo $XDG_SESSION_TYPE

.. figure:: assets/custom_config.png
   :scale: 70 %
   :alt: Open Config
   :align: center

   open configuration

Command to open custom configuration

.. code-block:: console

   $ sudo nano /etc/gdm3/custom.config

.. figure:: assets/change_type.png
   :scale: 70 %
   :alt: Change to Waylang enable while being False
   :align: center

   Change to waylandEnable=False

.. figure:: assets/restart.png
   :scale: 70 %
   :alt: Restarting your computer
   :align: center

   Restart your computer

Command for restart your computer

.. code-block:: console

   $ sudo systemctl restart gdm3

.. raw:: html

   <p style="text-align: justify;">

    The last way is if the condition has been on <i>x11</i> type, however, the program still cannot be running, may you should be
    typing command on your terminal to fix it.

.. code-block:: console

   $ sudo apt install libxcb-cursor0

Python.h Missing on Python-dev
-------------------------------

.. raw:: html

   <p style="text-align: justify;">

    If you encounter installation problem with <i>pybind</i> while using MoilCV, you can install <i>python-dev</i> that is compatible
    with your Python version to resolve the issue. The steps to take are the instructions provided below.</p>

.. code-block:: console

   $ sudo apt-get install python3.8-dev

or

.. code-block:: console

   $ sudo apt-get install python3.9-dev

.. figure:: assets/python_dev.png
   :scale: 70 %
   :alt: Python Dev Installation
   :align: center

   Python-dev installed based on version

Sphinx Documentation for PDF
-----------------------------

.. raw:: html

   <p style="text-align: justify;">

    Difficulty in accessing the <i>MoilApp documentation</i> in PDF format is a common issue encountered by users. This is often
    caused by errors that occur during the initial conversion of the documentation to HTML. To resolve this issue. Please
    endure that you follow the instructions carefully.</p>

.. figure:: assets/sphinx_PDF.png
   :scale: 70 %
   :alt: Converting RST to HTML file
   :align: center

   Convert rst file to html file

If the following error occurs, we advise installing an additional library so that it can be converted properly.

Command for install library

.. code-block:: console

   $ sudo apt install latexmk

   $ sudo apt install textlive-latex-extra

The command below can be typed in the terminal to access the documentation.

Command for generate file

.. code-block:: console

   $ make html

   $ make latexpdf

.. raw:: html

   <p style="text-align: justify;">

    This command is employed for deleting a documentation file, and it is also beneficial when updating a modified file.
    If the previous file is not deleted, the documentation will still show the outdated file instead of the updated version.</p>

.. code-block:: console

   $ make clean

Application running
--------------------

.. raw:: html

   <p style="text-align: justify;">

    You cannot update the application when an update notification is present when you establish a new branch and add some functions, or alter the source code, you will encounter an error and a dump if you try this.</p>


.. figure:: assets/change_branch.png
   :scale: 70 %
   :alt: alternate text
   :align: center

   check for update on local branch

.. raw:: html

   <p style="text-align: justify;">

    To update your branch, you can use this command in case you encounter an error. This command will ensure that
    any changes made are saved locally.</p>

.. code-block:: console

   $ git stash save "Save comment in local computer"

And then, try do change another branch again.

.. code-block:: console

   $ git checkout "develop/main"

Adjustment of name your branch want to change

References
===========

    - `Specific python | How to install pip for Python 3.9 <https://stackoverflow.com/questions/65644782/how-to-install-pip-for-python-3-9-on-ubuntu-20-04>`_

    - `Python.h missing on | with python-dev installed <https://stackoverflow.com/questions/65743603/python-h-missing-on-ubuntu-18-with-python-dev-installed>`_

    - `Ubuntu > 20.04, | XCB type screen display <https://intellij-support.jetbrains.com/hc/en-us/community/posts/11003640644242-Ubuntu-20-04-xcb?page=1#community_comment_11048699939346>`_
