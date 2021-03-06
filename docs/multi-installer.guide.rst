Multi Installer Guide
=====================

Pre-requisites
^^^^^^^^^^^^^^

Multi-Installer has been tested on Ubuntu Server, which is the recommended OS for the cloud installer.

Add the OpenStack installer ppa to your system.

.. code::

   $ sudo apt-add-repository ppa:juju/stable
   $ sudo apt-add-repository ppa:maas-maintainers/stable
   $ sudo apt-add-repository ppa:cloud-installer/testing
   $ sudo apt-get update

.. note::

   Adding the ppa is only necessary until an official release to the
   archives has been announced.

For a proper installation the system must have an available network interface that can be managed by MAAS
and respond to DNS/DHCP requests. The private network can then be configured to forward traffic out via public
network interface.

An example of a system with 2 network interfaces **eth0 (public)** and **eth1 (private, bridged)**

.. code::

   # The loopback network interface
   auto lo
   iface lo inet loopback
     dns-nameservers 127.0.0.1
     pre-up iptables-restore < /etc/network/iptables.rules

   auto eth0
   iface eth0 inet dhcp

   auto eth1
   iface eth1 inet manual

   auto br0
   iface br0 inet static
     address 172.16.0.1
     netmask 255.255.255.0
     bridge_ports eth1

Below sets up the NAT for those interfaces, save to **/etc/network/iptables.rules**:

.. code::

   *nat
   :PREROUTING ACCEPT [0:0]
   :INPUT ACCEPT [0:0]
   :OUTPUT ACCEPT [0:0]
   :POSTROUTING ACCEPT [0:0]
   -A POSTROUTING -s 172.16.0.1/24 ! -d 172.16.0.1/24 -j MASQUERADE
   COMMIT

Finally, enable IP Forwarding:

.. code::

   $ echo 1 > /proc/sys/net/ipv4/ip_forward

.. note::

   To make IP Forwarding persists, set the value in **/etc/sysctl.conf**


Installation
^^^^^^^^^^^^

Install OpenStack installer via `apt-get`

.. code::

   $ sudo apt-get install openstack

Start the installation
^^^^^^^^^^^^^^^^^^^^^^

To start the installation run the following command

.. code::

   $ sudo openstack-install

.. note::

   The installer should be run as a non-root user.

An initial dialog box will appear asking you to select which type of
install, choose **Multi-system**.

Setting a password
^^^^^^^^^^^^^^^^^^

When asked to set the openstack password it should be noted that this password is
used throughout all openstack related services (ie Horizon login password). The only
service that does not use this password is **juju-gui**.

Next Steps
^^^^^^^^^^

The installer will run through a series of steps starting with making
sure the necessary bits are available for a multi system installation
and ending with a `juju` bootstrapped system.

Accessing the OpenStack environment
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

See :doc:`Using Juju in OpenStack Guide <using-juju-in-openstack.guide>`

Tips
^^^^

Juju will arbitrarily pick a machine to install its state server to, however,
if a machine exists that is better suited you can tell the OpenStack installer
to use that machine instead:

.. code::

   $ JUJU_BOOTSTRAP_TO=openstack-vm-bootstrap.maas sudo -E openstack-install

.. note::

   **sudo -E** is necessary for the current environment to be preserved.

Troubleshooting
^^^^^^^^^^^^^^^

The installer keeps its own logs in **$HOME/.cloud-install/commands.log**.

Uninstalling
^^^^^^^^^^^^

To uninstall and cleanup your system run the following

.. code::

    $ sudo openstack -u
