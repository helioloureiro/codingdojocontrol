codingdojocontrol
=================

* A simple tool to use during coding dojos

The project target was to create an easy tool
to join two different needs for a coding dojo:

1) countdown timer

2) lighter about code status

After a quick search in Google, no tool could
attend my requirements, so I moved on and 
created this.

Graphical interfaces were created using 
qt4-designer.

TODO:
 * improve configuration
 * create notification GUIs?
 * play a sound once time reaches zero
 * change display collor in the last 10 seconds?
 * world domination

Requirements
============
 * python-qt4 

Usage
=====
Just clone this repo:
 git clone https://github.com/helioloureiro/codingdojocontrol.git codingdojo

Into this directory, codingdojo, it will run any .py script and check output result
for 0 (ok) or not.

So create your challenge, the create a script.  Before the pilot start to code,
press button "Start".  It will countdown till zero.

If for some reason you need to start over the counter, just press "Reset".

"Configure" button allows you to select other directory to place your coding 
dojo's code, and change the default time from 5 minutes (300 seconds).

