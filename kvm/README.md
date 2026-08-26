# KVM

## Introduction

KVM is a hypervisor that runs natively on Linux. This example contains scripts to install Linux using the graphical installer.

## Pre-requisites

KVM must be configured for your Linux system.

## Install Rocky

First download the ISO for RockyLinux 10 from the cloest mirror at https://rockylinux.org/download and copy it to /var/lib/libvirt/boot.

Next, copy the QCOW2 file for RockyLinux 10 and copy it to KVM storage pool. The script defaults this location to /data/libvirt/default/images.

The latest version of RockyLinux 10 as of this writing is 10.2. If a newer version is available, please update install.sh.

Next, run the install script:

```sh
sh ./install_rocky.sh -n web-server -s 30
Creating VM...

Domain 'web-server' has been undefined

Image resized.

Starting install...
Creating domain...                                          |         00:00     
Running graphical console command: virt-viewer --connect qemu:///system --wait web-server
```

The graphical installer will be displayed in a separate window.

<img src="rocky_linux_kvm_install_screen.png" />

## Install Ubuntu

Download the latest Ubuntu ISO image from https://ubuntu.com/download/server and copy it to /var/lib/libvirt/boot. 

Next, download the latest Ubuntu qcow2 image from https://cloud-images.ubuntu.com/resolute/current/ and copy it to /data/libvirt/default/images.

Next, run the install script:

```sh
sh ./install_ubuntu.sh -n ubuntu-server -s 20
```

The graphical installer will be displayed in a separate window.

<img src="ubuntu_install_screen.png" />