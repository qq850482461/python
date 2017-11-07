from IPy import IP
import nmap

ip_network = IP('192.168.1.1').make_net('255.255.255.254')
for i in ip_network:
    print(i)