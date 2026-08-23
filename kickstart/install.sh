#!/bin/sh

VM_NAME=""
ISO_FILE="/data/libvirt/default/boot/Rocky-10.2-x86_64-dvd1.iso"
GENERIC_QCOW_FILE="/data/libvirt/default/images/Rocky-10-GenericCloud-Base.latest.x86_64.qcow2"
DISK_SIZE="20"
KICKSTART_SERVER="192.168.1.20"
ROOT_PASSWORD=""

usage() {
    echo "Usage: ./install.sh -n <vmname> -s <size> -p <password>"
    echo "Example: ./install.sh -n web-server -s 20 -p secret"
}

validate() {
    error=0

    if [ "${VM_NAME}" = "" ]; then
        echo "Missing -n <VM name>"
        error=1
    fi

    if [ "${SIZE}" = "" ]; then
        echo "Missing -s <size>"
        error=1
    fi

    if [ "${ROOT_PASSWORD}" = "" ]; then
        echo "Missing -p <root password>"
        error=1
    fi

    if [ "$error" -eq 1 ]; then
        usage
        exit
    fi
    
}

while getopts ":hn:s:p:" option; do
    case $option in
        h)
            usage
            exit;;
        n)
            VM_NAME="${OPTARG}"
            ;;
        s)
            SIZE="${OPTARG}"
            ;;
        p)
            ROOT_PASSWORD="${OPTARG}"
            ;;
        \?)
            echo "Invalid option: ${OPTARG}"
            usage
            exit;;

   esac
done

shift $((OPTIND -1))

validate

echo "Creating VM..."

sudo virsh destroy ${VM_NAME} 2> /dev/null
sudo virsh undefine ${VM_NAME} 2> /dev/null

sudo rm -f /data/libvirt/default/images/${VM_NAME}.qcow2

sudo cp -f $GENERIC_QCOW_FILE /data/libvirt/default/images/${VM_NAME}.qcow2

cp anaconda-ks-template.cfg anaconda-ks.cfg
sed -i "s|{{ password }}|${ROOT_PASSWORD}|g" anaconda-ks.cfg

sudo qemu-img resize /data/libvirt/default/images/${VM_NAME}.qcow2 ${SIZE}G

sudo virt-install \
  --virt-type=kvm \
  --name ${VM_NAME} \
  --ram  4096 \
  --vcpus=4 \
  --os-variant=rocky10 \
  --location=$ISO_FILE \
  --network=bridge=br0,model=virtio \
  --disk path=/data/libvirt/default/images/${VM_NAME}.qcow2,size=${DISK_SIZE},bus=virtio,format=qcow2 \
  --extra-args="inst.ks=http://${KICKSTART_SERVER}:8000/anaconda-ks.cfg console=ttyS0" \
  --disk path=$ISO_FILE,device=cdrom \
  --graphics none \
  --wait=-1
