#!/bin/bash
mask='/24'
base_octets='172.16.'
gateway_octet='1'

declare -A wan=([dev]='enp0s4'
                [bridge]='br0'
                [octet]='0'
                [octets]=${base_octets}'0.'
                [gateway]=${base_octets}'0.1')

path='/var/lib/lxc/'
lxc_template='/usr/share/lxc/templates/lxc-archlinux'

set_bridge_up() { echo "DEBUG: ${LINENO}" >&2
  eval "declare -A neu="${1#*=}

  # Special cases
  case "${neu[bridge]}" in
    br0) ip link add ${neu[bridge]} type bridge
         ip link set ${neu[bridge]} up
         ip addr add ${neu[gateway]}${mask} dev ${neu[bridge]}
         ;;
  esac
}

prepare_lxc() { echo "DEBUG: ${LINENO}" >&2
  lxc_id=$1
  lxc_name='lxc'${lxc_id}
  config=${path}${lxc_name}'/config'
  autodev=${path}${lxc_name}'/autodev'

  lxc-create -n ${lxc_name} -t ${lxc_template}
  init_config
  add_veth "$(declare -p wan)" 
  set_gateway ${wan[gateway]}
  complete_config_w_autdev

  #install dependencies
  lxc-start -n ${lxc_name}
}
init_config() { echo "DEBUG: ${LINENO}" >&2
cat > ${config} << EOL
# Template used to create this container: /usr/share/lxc/templates/lxc-archlinux
# Parameters passed to the template:
# For additional config options, please look at lxc.container.conf(5)
## Default values
lxc.rootfs = /var/lib/lxc/${lxc_name}/rootfs
lxc.utsname = ${lxc_name}
lxc.arch = x86_64
lxc.include = /usr/share/lxc/config/archlinux.common.conf
#
## Capabilities
#lxc.cap.drop = mac_admin
#lxc.cap.drop = mac_override
#lxc.cap.drop = sys_admin
#lxc.cap.drop = sys_module
#lxc.cap.drop = mknod
#lxc.cap.drop = setuid
#lxc.cap.drop = net_raw
#
## UID Mappings
#lxc.id_map = u 0 100000 10000
#lxc.id_map = g 0 100000 10000
#
## Cgroups
#lxc.cgroup.cpuset.cpus = 0,1
#lxc.cgroup.cpu.shares = 256
#lxc.cgroup.devices.deny = a
#lxc.cgroup.devices.allow = c 1:3 rw
#lxc.cgroup.devices.allow = b 8:0 rw
#
## Network
EOL
}
set_gateway() { echo "DEBUG: ${LINENO}" >&2
cat >> ${config} << EOL
lxc.network.ipv4.gateway = $1
#
EOL
}
add_veth() { echo "DEBUG: ${LINENO}" >&2
  eval "declare -A veth="${1#*=}
  
  veth[lxc]='v'${veth[octet]}'p'${lxc_id} 
  veth[host]='v'${veth[octet]}'b'${lxc_id}
  ip link add ${veth[host]} type veth peer name ${veth[lxc]}
  ip link set ${veth[host]} up
  ip link set ${veth[host]} master ${veth[bridge]}

  set_network_config "$(declare -p veth)"
}
set_network_config() { echo "DEBUG: ${LINENO}" >&2
eval "declare -A cveth="${1#*=}
cat >> ${config} << EOL
lxc.network.type = phys
lxc.network.link = ${cveth[lxc]}
lxc.network.flags = up
lxc.network.ipv4 = ${cveth[octets]}${lxc_id}${mask}
lxc.network.name = eth${cveth[octet]}
EOL
}
complete_config_w_autdev() { echo "DEBUG: ${LINENO}" >&2
autodev_content='#!/bin/bash 
cd ${LXC_ROOTFS_MOUNT}/dev 
mkdir net 
mknod net/tun c 10 200 
chmod 0666 net/tun'
echo "$autodev_content" > ${autodev}
chmod +x /var/lib/lxc/${lxc_name}/autodev

cat >> ${config} << EOL
## mounts
## specify shared filesystem paths in the format below
## make sure that the mount point exists on the lxc
#lxc.mount.entry = /mnt/data/share mnt/data none bind 0 0
#
## for xorg
## fix overmounting see: https://github.com/lxc/lxc/issues/434
lxc.mount.entry = tmpfs tmp tmpfs defaults
lxc.mount.entry = /dev/dri dev/dri none bind,optional,create=dir
lxc.mount.entry = /dev/snd dev/snd none bind,optional,create=dir
lxc.mount.entry = /tmp/.X11-unix tmp/.X11-unix none bind,optional,create=dir
lxc.mount.entry = /dev/video0 dev/video0 none bind,optional,create=file
#
# if running the same Arch linux on the same architecture it may be
# adventitious to share the package cache directory
#lxc.mount.entry = /var/cache/pacman/pkg var/cache/pacman/pkg none bind 0 0
#
## systemd within the lxc
lxc.autodev = 1
lxc.pts = 1024
lxc.kmsg = 0
lxc.hook.autodev=/var/lib/lxc/${lxc_name}/autodev
#
EOL
}

chroot_exec() { echo "DEBUG: ${LINENO}" >&2
  rootpath=${path}"$1"'/rootfs/'
  chroot ${rootpath} ln -s /dev/null /etc/systemd/system/systemd-udevd.service &\
                     ln -s /dev/null /etc/systemd/system/systemd-udevd-control.socket &\
                     ln -s /dev/null /etc/systemd/system/systemd-udevd-kernel.socket &\
                     ln -s /dev/null /etc/systemd/system/proc-sys-fs-binfmt_misc.automount
}

set_iptables_flush() {
  table_cmd="iptables "
  ns_prefix="ip netns exec"

  ns=""
  device=""
  bridge=""

  if [ ${#} == 3 ]; then
    ns="$1"
    device="$2"
    bridge="$3"
    table_cmd="${ns_prefix}"' '"${ns}"' '"${table_cmd}"
  else
    device="$1"
    bridge="$2"
  fi

  eval "${table_cmd}"" -F"
  eval "${table_cmd}"" -X"
  eval "${table_cmd}"" -t nat -F"
  eval "${table_cmd}"" -t nat -X"
  eval "${table_cmd}"" -t mangle -F"
  eval "${table_cmd}"" -t mangle -X"
  eval "${table_cmd}"" -t raw -F"
  eval "${table_cmd}"" -t raw -X"
  eval "${table_cmd}"" -t security -F"
  eval "${table_cmd}"" -t security -X"
  eval "${table_cmd}"" -P INPUT ACCEPT"
  eval "${table_cmd}"" -P FORWARD ACCEPT"
  eval "${table_cmd}"" -P OUTPUT ACCEPT"

}

set_iptables() {
  table_cmd="iptables "
  nic="$1"
  bridge="$2"
  iptables -N TCP
  iptables -N UDP

  iptables -A INPUT -i lo -j ACCEPT
  #iptables -A FORWARD -i lo -j ACCEPT
  #iptables -A INPUT ! -i lo -s 127.0.0.0/8 -j REJECT

### DROPspoofing packets
iptables -A INPUT -s 10.0.0.0/8 -j DROP 
iptables -A INPUT -s 169.254.0.0/16 -j DROP
iptables -A INPUT -i ${nic} -s 172.16.0.0/12 -j DROP
iptables -A INPUT -s 127.0.0.0/8 -j DROP
iptables -A INPUT -s 192.168.0.0/24 -j DROP

iptables -A INPUT -s 224.0.0.0/4 -j DROP
iptables -A INPUT -d 224.0.0.0/4 -j DROP
iptables -A INPUT -s 240.0.0.0/5 -j DROP
iptables -A INPUT -d 240.0.0.0/5 -j DROP
iptables -A INPUT -s 0.0.0.0/8 -j DROP
iptables -A INPUT -d 0.0.0.0/8 -j DROP
iptables -A INPUT -d 239.255.255.0/24 -j DROP
iptables -A INPUT -d 255.255.255.255 -j DROP

# Droping all invalid packets
iptables -A INPUT -m state --state INVALID -j DROP
iptables -A FORWARD -m state --state INVALID -j DROP
iptables -A OUTPUT -m state --state INVALID -j DROP

# flooding of RST packets, smurf attack Rejection
iptables -A INPUT -p tcp -m tcp --tcp-flags RST RST -m limit --limit 2/second --limit-burst 2 -j ACCEPT

  iptables -A INPUT -p tcp -m tcp -m multiport --dports 80,443,9001,9050,10001 -j ACCEPT
  iptables -A INPUT -m conntrack --ctstate RELATED,ESTABLISHED -j ACCEPT
  iptables -A INPUT -m state --state ESTABLISHED,RELATED -j ACCEPT
  iptables -A INPUT -m conntrack --ctstate INVALID -j DROP
  iptables -A INPUT -p icmp --icmp-type 8 -m conntrack --ctstate NEW -j ACCEPT
  iptables -A INPUT -i ${nic} -p udp -m conntrack --ctstate NEW -j UDP
  iptables -A INPUT -i ${nic} -p tcp --syn -m conntrack --ctstate NEW -j TCP
  iptables -A INPUT -i ${nic} -p udp -j REJECT --reject-with icmp-port-unreachable
  iptables -A INPUT -i ${nic} -p tcp -j REJECT --reject-with tcp-rst
  iptables -A INPUT -i ${nic} -p udp -j REJECT --reject-with icmp-proto-unreachable
  iptables -A INPUT -i ${nic} -p udp -j REJECT --reject-with icmp-port-unreachable
  iptables -A INPUT -i ${nic} -p tcp -j REJECT --reject-with tcp-rst
  iptables -A INPUT -i ${nic} -j REJECT --reject-with icmp-proto-unreachable
  iptables -A INPUT -i ${nic} -p icmp --icmp-type echo-request -m limit --limit 30/min --limit-burst 8 -j ACCEPT
  iptables -A INPUT -i ${nic} -p icmp --icmp-type echo-request -j DROP
  iptables -A INPUT -i ${nic} -p icmp --icmp-type echo-request -m limit --limit 30/min --limit-burst 8 -j ACCEPT
  iptables -A INPUT -i ${nic} -p icmp --icmp-type echo-request -j DROP
  iptables -I TCP -i ${nic} -p tcp -m recent --update --seconds 60 --name TCP-PORTSCAN -j REJECT --reject-with tcp-rst
  iptables -D INPUT -i ${nic} -p tcp -j REJECT --reject-with tcp-rst
  iptables -A INPUT -i ${nic} -p tcp -m recent --set --name TCP-PORTSCAN -j REJECT --reject-with tcp-rst
  iptables -I TCP -i ${nic} -p tcp -m recent --update --seconds 60 --name TCP-PORTSCAN -j REJECT --reject-with tcp-rst
  iptables -D INPUT -i ${nic} -p tcp -j REJECT --reject-with tcp-rst
  iptables -A INPUT -i ${nic} -p tcp -m recent --set --name TCP-PORTSCAN -j REJECT --reject-with tcp-rst
  iptables -I UDP -i ${nic} -p udp -m recent --update --seconds 60 --name UDP-PORTSCAN -j REJECT --reject-with icmp-port-unreachable
  iptables -D INPUT -i ${nic} -p udp -j REJECT --reject-with icmp-port-unreachable
  iptables -A INPUT -i ${nic} -p udp -m recent --set --name UDP-PORTSCAN -j REJECT --reject-with icmp-port-unreachable
  iptables -D INPUT -i ${nic} -j REJECT --reject-with icmp-proto-unreachable
  iptables -A INPUT -i ${nic} -j REJECT --reject-with icmp-proto-unreachable

  iptables -t nat -A POSTROUTING -o ${nic} -j MASQUERADE
  iptables -A FORWARD -m conntrack --ctstate RELATED,ESTABLISHED -j ACCEPT
  iptables -A FORWARD -i ${bridge} -o ${nic} -j ACCEPT

  iptables -t nat -A PREROUTING -p tcp --dport 9001 -j DNAT --to 172.16.0.5:9001
  iptables -t nat -A PREROUTING -p tcp --dport 9050 -j DNAT --to 172.16.0.5:9050

  #iptables -A INPUT -j DROP

  iptables -A OUTPUT -m state --state ESTABLISHED,RELATED -j ACCEPT
  iptables -A OUTPUT -p tcp -m tcp -m multiport --dports 80,443,9001,9050,10001 -j ACCEPT
  #iptables -A OUTPUT -j DROP
  iptables -A FORWARD -m state --state ESTABLISHED,RELATED -j ACCEPT
  iptables -A FORWARD -p tcp -m tcp -m multiport --dports 80,443,9001,9050,10001 -j ACCEPT
  #iptables -A FORWARD -j DROP

}

save_tables() { echo "DEBUG: ${LINENO}" >&2
  iptables-save > /etc/iptables/iptables.rules
}
veths() { echo "DEBUG: ${LINENO}" >&2
  lxc_id=$1
  lxc_name='lxc'${lxc_id}
  add_veth "$(declare -p wan)" 
}
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

#pacman --noconfirm -Syu
set_bridge_up "$(declare -p wan)"
echo "1" > /proc/sys/net/ipv4/ip_forward
set_iptables_flush ${wan[dev]} ${wan[bridge]}
set_iptables ${wan[dev]} ${wan[bridge]}
save_tables
