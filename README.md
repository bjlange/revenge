Revenge of the Nerds v0.1
-------------------------------

My crack at using statistical inference, the value-based drafting
principle, maybe some simulation in conjunction with some fun custom
web interfaces to crush everyone in my fantasy draft this year. In
other words, [data science](http://datasco.pe)!

More here once there's something to talk about. This project is
configured with Vagrant and Fabric, read more about how to get it running below.


Setting up the dev environment
---------------

### NOTE: not sure if this is even gonna be necessary. But, it's here.

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
