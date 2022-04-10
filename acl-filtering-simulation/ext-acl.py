import re
import sys

acl_regex = r"access-list\s+(\d)+\s+(deny|permit)\s+(tcp|ip|udp)\s+(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\s+(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})+\s+(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})+\s+(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})+\s+(range\s\d+-\d+)?(eq\s\d+)?"
packet_regex = r"(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\s+(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\s+(\d+)"

acl_no = 0
ispermit = 1
protocol = 2
src_addr = 3
src_mask = 4
dest_addr = 5
dest_mask = 6
port_range =7
port =8

packet_src_ip = 0
packet_dest_ip =1
packet_dest_port= 2
# there are total 4 posibilities for each rule and packet combination
 
#  permit and match , break loop pemitted
#  permit and not match, keep checking 
#  not permit and match, denied
#  not permit and not match, keep checking


def is_ip_allowed(ip,mask,act):

    split_ip = ip.split(".")
    split_mask = mask.split(".")
    split_act = act.split(".")
    for i in range(len(split_mask)):
        expected = (~int(split_mask[i])) & int(split_ip[i])
        actual = (~int(split_mask[i])) & int(split_act[i])
        if expected!=actual:
            return False
    return True

def match_acl(rule,packet):
    matches = re.search(acl_regex, rule)

    if not matches:
        sys.exit("invalid syntax of acl")

    matches = matches.groups()
    port_match = True
    result = True
    result = result and is_ip_allowed(matches[src_addr],matches[src_mask],packet[packet_src_ip])
    result = result and is_ip_allowed(matches[dest_addr],matches[dest_mask],packet[packet_dest_ip])

    if "eq" in rule:
        port = rule.split("eq")[1].rstrip()
        if port !=packet[packet_dest_port]:
            port_match = False

    if "range" in rule:
        ports = rule.split("range")[1].rstrip().split("-")
        if not (packet[packet_dest_port]>=ports[0] and packet[packet_dest_port]<=ports[1]):
            port_match = False

    result = result and port_match
    if matches[ispermit]=="permit":
        if result:
            return True,True
        else:
            return False,False
    else:
        if result:
            return False,True
        else:
            return False,False
    


def packet_filtering(rules,packets):
    for packet in packets:
        packet = packet.rstrip()
        matches = re.search(packet_regex, packet)

        if not matches:
            sys.exit("invalid syntax of packet")
        packets = matches.groups()

        result = False
        for line in rules:
            if line.startswith("access-list"):
                if "any" in line:
                    # handle case when there's keyword any in rule
                    line = line.replace("any","0.0.0.0 255.255.255.255")

                result, final = match_acl(line,packets)

                if final:
                    break
            else:
                # ignoring interface and ip access-group related rules
                pass

        if result:
            print("Packet from "+packets[packet_src_ip]+" to "+packets[packet_dest_ip]+" on port "+packets[packet_dest_port]+" permitted")
        else:
            print("Packet from "+packets[packet_src_ip]+" to "+packets[packet_dest_ip]+" on port "+packets[packet_dest_port]+" denied")



if __name__=="__main__":
    rules = None
    with open('input/ext-acl1.txt') as f:
        rules = f.readlines()

    with open('input/ext-acl2.txt') as f:
        packets = f.readlines()
    
    packet_filtering(rules,packets)
