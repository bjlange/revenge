Revenge of the Nerds v0.1
-------------------------------

My crack at using statistical inference and simulation in conjunction
with some fun custom web interfaces to crush everyone in my fantasy
league this year. In other words, [data science](datasco.pe)!

More here once there's something to talk about. This project is configured with Vagrant and Fabric,


Setting up your dev environment
---------------

Big ups to @gabegaster for the easy, breezy, beautiful
[FabTools Start Kit](https://github.com/gabegaster/FabTools_StartKit)

* Install [Vagrant](http://vagrantup.com),
  [Fabric](http://fabric.readthedocs.org/en/latest/installation.html),
  and [fabtools](http://fabtools.readthedocs.org/en/latest/).

* From the command line, run `fab dev vagrant.up provision`. This will
  create a virtual machine with all the necessary packages.

* SSH to the virtual machine with `vagrant ssh`.

* Put in any python or other unix tools you want in REQUIREMENTS or
  REQUIREMENTS-DEB, and use `fab dev provision` to install them onto
  your machine.
