# check_bgp_mikrotik_os7
Simple script to check status of BGP session through API on Mikrotik Routers with OS7.

## Requirements
It's require REQUESTES:
python -m pip install requests #python3
python -m pip install requests==2.7.0 #python 2.7
sudo yum install python-requests #python 2.6.6

It has been tested on:
* Python (2.6.6 && 2.7.6 && 3.10.6)
* Ubuntu 22.04
* CentOS (6,7)

### How to use it

usage: check_bgp_mikrotik_os7.py -H <HOSTNAME> -u <USERNAME> -p <PASSWORD> -b <BGP_IP>

HOSTNAME - address of mikrotik router
USERNAME - API username
PASSWORD - API password
BGP_IP - BGP IP

### Nagios configuration

First edit your nagios commands.cfg file and add:

    define command{
        command_name check_mikrotik_bgp
        command_line python $USER1$/check_bgp_mikrotik_os7.py -H $HOSTADDRESS$ -u $ARG1$ -p $ARG2$ -b $ARG3$
    }
    
    
Then add checks in your host.cfg file. This is example of how to define one command check:

 *check_bgp_mikrotik_os7.py -H 10.200.20.100 -u api-user -p api-pass -b 10.200.20.210

    define host {
    use                            generic-router
    host_name                      mikrotik_rtr-10-1
    alias                          mikrotik_rtr-10-1
    address                        10.200.20.100
    }

    define service {
    use                            generic-service
    host_name                      mikrotik_rtr-10-1
    service_description            Check iBGP
    check_command                  check_mikrotik_bgp!api-user!api-pass!10.200.20.210
    check_interval                 15
    notifications_enabled          1
    }
 
Here is an example plugin answer:

    [root@monitor ~]# python /usr/lib64/nagios/plugins/./check_bgp_mikrotik_os7.py -H 10.200.20.100 -u api-user -p api-pass -b 10.200.20.210
    OK - 10.200.20.210 state is established. Established for 33w2d12h43m28s760ms

