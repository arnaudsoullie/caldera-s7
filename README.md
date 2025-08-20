# Caldera for OT plugin: Snap7
A Caldera for OT plugin supplying Caldera with snap7 protocol TTPs. This is part of a series of plugins that provide added threat emulation capability for Operational Technology (OT) environments.

Full snap7 plugin documentation can be viewed as part of fieldmanual, once the Caldera server is running.

# Installation
To run Caldera along with snap7 plugin:

- Download Caldera as detailed in the Installation Guide
- Install the snap7 plugin in Caldera's plugin directory: `caldera/plugins`
- Enable the snap7 plugin by adding `- snap7` to the list of enabled plugins in `conf/local.yml` or `conf/default.yml` (if running Caldera in insecure mode)
Version

# Description

abilities available in the snap7 plugin:
- Gathering data from PLC
- read Data Block
- write Data Block
- fuzz Data Block
- read/write other data types




