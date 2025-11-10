# Caldera for OT plugin: Snap7
A Caldera for OT plugin supplying Caldera with the Siemens S7 protocol TTPs. This is part of a series of plugins that provide added threat emulation capability for Operational Technology (OT) environments.
The plugin uses the open-source [Snap7 library](https://github.com/davenardella/snap7)

# Installation
To install the snap7 plugin:
- Copy the snap7 plugin in Caldera's plugin directory: `caldera/plugins`
- Enable the snap7 plugin by adding `- snap7` to the list of enabled plugins in `conf/local.yml` or `conf/default.yml` (if running Caldera in insecure mode)

# Payload compiling
In order to use thisd plugin, you need to have the snap7_cli executable file for the agent architecure.
A compiled version is provided for x64 linux and Windows.
To compile it yourself, you'll need to install the snap7 library as well as the [python-snap7](https://github.com/gijzelaerr/python-snap7) Python wrappers.

# Features
The abilities available in the snap7 plugin are:
- Gathering data from PLC
- read Data Block
- write Data Block
- fuzz Data Block
- read/write other data types

# Limitations
As the plugin is based on snap7, compatibility is the same as the library:
 - Only global DBs can be accessed.
 - The optimized block access must be turned off.
 - The access level must be “full” and the “connection mechanism” must allow GET/PUT.
More information can be found on [Snap7 website](https://snap7.sourceforge.net/) by naviagting to "Snap7 communications" -> "Snap7 client" -> "Target compatibility"

