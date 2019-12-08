#!/usr/bin/env python3.6
"""
Learning to use Scapy to manipulate proxy requests to a IP Range.


"""

import logging
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)
import random
import sys
import os
os.sys.path.append('/home/hiddenx/Mini-Projects/Google_Dorks_Utility/pydev/lib/python3.6/site-packages')

from scapy.all import *


def init_packet(ipacket):
    """Create dictionary containing packet paramters"""
    src_ip = ipacket['source_ip']
    dst_ip = ipacket['destination_ip']
    dst_port = int(ipacket['destination_port'])
    rwin = 8192
    seq = random.getrandbits(32)
    src_port = random.randrange(32768,61000)
    tcp_options, timestamps = [], []
    #
    # if wscale != 0:
    #     tcp_options.append(('WScale', args.wscale))
    #
    # if mss != 0:
    #     tcp_options.append(('MSS', args.mss))
    #
    # if sack != 0:
    #     tcp_options.append(('SAckOK', b''))
    #
    # if tsval != 0:
    #     tsval = args.tsval
    #     tsecr = 0
    #     tcp_options.append(('Timestamp', (tsval, tsecr)))
    #     timestamps = [('Timestamp', (tsval, tsecr))]
    # else:
    #     timestamps = []

    print(tcp_options)

    packet_params = {"src_ip":src_ip, "dst_ip":dst_ip, "src_port":src_port,
                 "dst_port":dst_port, "rwin":rwin, "seq":seq, "ack":0,
                 "tcp_options":tcp_options, "timestamps":timestamps}
    return packet_params


def update_timestamp(packet_params, previous):
    """If TCP timestamps are being used, extract tsecr from reply packets
    and increase TSval by one, every time this function is called.
    """
    # TODO change this so that the TSval increase is clock-based as per RFC7323
    # timestamp clock should tick by 1 every 1ms to 1s - lets aim for every 100ms
    reply_opts = dict(previous['TCP'].options)
    if 'Timestamp' in reply_opts:
        tsecr = reply_opts['Timestamp'][0]
        tsval = packet_params['timestamps'][0][1][0] + 1
        packet_params['timestamps'] = [('Timestamp', (tsval, tsecr))]
    return packet_params


def update_seq_ack(packet_params, previous):
    """Increase Sequence and Acknowledgement number"""
    seq = packet_params.get("seq") + 1
    ack = previous.seq +1
    packet_params['seq'] = seq
    packet_params['ack'] = ack
    return packet_params


def packet_constructor(packet_params, packet_flags):
    """Craft an IP or TCP packet for sending"""
    src_ip = packet_params.get("src_ip")
    dst_ip = packet_params.get("dst_ip")
    src_port = packet_params.get("src_port")
    dst_port = packet_params.get("dst_port")
    seq = packet_params.get("seq")
    ack = packet_params.get("ack")
    rwin = packet_params.get("rwin")
    tcp_options = packet_params.get("tcp_options")
    timestamps = packet_params.get("timestamps")

    if packet_flags == 'IP':
        packet = IP(src=src_ip, dst=dst_ip)
    elif packet_flags == 'S':
        packet = TCP(sport=src_port, dport=dst_port, flags='S', seq=seq,
                     window=rwin, options=tcp_options)
    else:
        packet = TCP(sport=src_port, dport=dst_port, flags=packet_flags,
                     seq=seq, ack=ack, window=rwin, options=timestamps)
    return packet


def handshake(packet_params):
    """Perform TCP 3-Way Handshake and connection teardown"""
    ip = packet_constructor(packet_params, 'IP')
    syn = packet_constructor(packet_params, 'S')
    # send SYN, retrieve SYN/ACK
    print(ip)
    synack = sr1((ip/syn), timeout=3, retry=3, verbose=0)
    if synack is None :
        print("ERROR: No SYN/ACK received from target. Please check the "
              "destination IP and Port are correct.")
        rst = packet_constructor(packet_params, 'R')
        send(ip/rst)
        sys.exit(1)

    # Update seq, ack and tcp timestamp clock (if required)
    packet_params = update_seq_ack(packet_params, synack)
    packet_params = update_timestamp(packet_params, synack)

    # send ACK to complete the establishing handshake
    ack = packet_constructor(packet_params, 'A')
    send(ip/ack)

    packet_params = update_timestamp(packet_params, synack)

    fin = packet_constructor(packet_params, 'FA')

    # send FIN, store FIN/ACK response
    finack = sr1((ip/fin), timeout=3, retry=2, verbose=1)

    if finack is None:
        print("ERROR: No FIN/ACK received from target.")
        rst = packet_constructor(packet_params, 'R')
        send(ip/rst)
        sys.exit(1)

    packet_params = update_seq_ack(packet_params, finack)
    packet_params = update_timestamp(packet_params, synack)

    # send ACK to complete the termination handshake
    ack = packet_constructor(packet_params, "A")
    send(ip/ack)


if __name__ == "__main__":
    ipacket = {"source_ip":'103.130.189.170',"destination_ip":'185.58.16.41',"destination_port":'8888'}
    packet_params = init_packet(ipacket)
    handshake(packet_params)
    # curl -x http://185.58.16.41:8888 -L http://ask.com
