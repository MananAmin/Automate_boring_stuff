import re
import sys

acl_regex = r"access-list\s+(\d)+\s+(deny|permit)\s+(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\s+(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})"
acl_no = 0
ispermit = 1
src_addr = 2
src_mask = 3

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

def match_acl(str,packet):
    matches = re.search(acl_regex, str)

    if not matches:
        sys.exit("invalid syntax of acl")
    matches = matches.groups()
    if len(matches)>=3 and len(matches)<=4:
        if matches[ispermit]=="permit":
            if is_ip_allowed(matches[src_addr],matches[src_mask],packet):
                return True,True
            else:
                return None,False
        else:
            if is_ip_allowed(matches[src_addr],matches[src_mask],packet):
                return False,True
            else:
                return None,False
    else:
        sys.exit("invalid syntax of acl")

def packet_filtering(rules,packets):
    for packet in packets:
        packet = packet.rstrip()
        result = False
        for line in rules:
            if line.startswith("access-list"):
                if "any" in line:
                    # handle case when there's keyword any in rule
                    line = line.replace("any","0.0.0.0 255.255.255.255")
                result, final = match_acl(line,packet)
                if final:
                    break
            else:
                # ignoring interface and ip access-group related rules
                pass

        if result:
            print("Packet from "+packet+" permitted")
        else:
            print("Packet from "+packet+" denied")

if __name__=="__main__":
    with open('input/acl1.txt') as f:
        rules = f.readlines()

    with open('input/acl2.txt') as f:
        packets = f.readlines()

    packet_filtering(rules,packets)