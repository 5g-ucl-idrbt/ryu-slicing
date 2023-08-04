import json
from ryu.base import app_manager
from ryu.controller import ofp_event
from ryu.controller.handler import CONFIG_DISPATCHER, MAIN_DISPATCHER
from ryu.controller.handler import set_ev_cls
from ryu.ofproto import ofproto_v1_3
from ryu.lib.packet import packet
from ryu.lib.packet import ethernet
from ryu.lib.packet import ether_types
from ryu.lib.packet import ipv4
from ryu.lib.packet import arp


class TrafficSlicing(app_manager.RyuApp):
    OFP_VERSIONS = [ofproto_v1_3.OFP_VERSION]

    def __init__(self, *args, **kwargs):
        super(TrafficSlicing, self).__init__(*args, **kwargs)

        
         

    @set_ev_cls(ofp_event.EventOFPSwitchFeatures, CONFIG_DISPATCHER)
    def switch_features_handler(self, ev):
        datapath = ev.msg.datapath
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        # Install table-miss flow entry
        match = parser.OFPMatch()
        actions = [parser.OFPActionOutput(ofproto.OFPP_CONTROLLER,
                                         ofproto.OFPCML_NO_BUFFER)]
        self.add_flow(datapath, 0, match, actions)


    def add_flow(self, datapath, priority, match, actions):
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        # construct flow_mod message and send it.
        inst = [parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS, actions)]
        mod = parser.OFPFlowMod(
            datapath=datapath, priority=priority, match=match, instructions=inst
        )
        self.logger.info("add_flow.datapath.send_msg(%s)", vars(mod))
        datapath.send_msg(mod)

    def _send_package(self, msg, datapath, in_port, actions):
        data = None
        ofproto = datapath.ofproto
        if msg.buffer_id == ofproto.OFP_NO_BUFFER:
            data = msg.data

        out = datapath.ofproto_parser.OFPPacketOut(
            datapath=datapath,
            buffer_id=msg.buffer_id,
            in_port=in_port,
            actions=actions,
            data=data,
        )
        self.logger.info("_send_package.datapath.send_msg(%s)", vars(out))
        datapath.send_msg(out)

    @set_ev_cls(ofp_event.EventOFPPacketIn, MAIN_DISPATCHER)
    def _packet_in_handler(self, ev):
        msg = ev.msg
        datapath = msg.datapath
        parser = datapath.ofproto_parser

        in_port = msg.match["in_port"]
        pkt = packet.Packet(msg.data)
        eth = pkt.get_protocol(ethernet.ethernet)
        dest= eth.dst
        sorc=eth.src
        print("desitnation " +dest)
        print("source " + sorc)
        
        dpid = datapath.id
        ip = pkt.get_protocols(arp.arp)[0]
        dst=arp.dst
        src=arp.src
        if src == '12.1.1.2' :
            dst = '10.0.0.2'
        
            actions = [
                parser.OFPActionSetField(ipv4_dst="10.0.0.2"),
                parser.OFPActionSetField(eth_src='1a:4c:db:f8:ac:8f'),
               
                parser.OFPActionOutput(dcp10)
                ]
            match = datapath.ofproto_parser.OFPMatch(ipv4_src=src)
            self.add_flow(datapath, 1, match, actions)
            self._send_package(msg, datapath, in_port, actions)
            
        elif src == '12.1.1.3':
            dst = '10.0.0.3'
            
            actions = [
                parser.OFPActionSetField(ipv4_dst="10.0.0.3"),
                parser.OFPActionSetField(eth_src='1e:31:b2:cf:23:58'),
                
            
                parser.OFPActionOutput(dcp7)
                ]
            match = datapath.ofproto_parser.OFPMatch(ipv4_src=src)
            self.add_flow(datapath, 1, match, actions)
            self._send_package(msg, datapath, in_port, actions)
        elif src == '10.0.0.2':
            dst = '12.1.1.2'
           
            actions = [
                parser.OFPActionSetField(ipv4_src="10.0.0.2"),
                parser.OFPActionSetField(eth_src='1a:4c:db:f8:ac:8f'),
                
                parser.OFPActionOutput(dcp8)
                ]
            match = datapath.ofproto_parser.OFPMatch(ipv4_src=src)
            self.add_flow(datapath, 1, match, actions)
            self._send_package(msg, datapath, in_port, actions)
           
        elif src == '10.0.0.3':
            dst = '12.1.1.3'
         
            actions = [
                parser.OFPActionSetField(ipv4_src="10.0.0.3"),
                parser.OFPActionSetField(eth_src='1a:4c:db:f8:ac:8f'),
                
                parser.OFPActionOutput(dcp8)
                ]
            match = datapath.ofproto_parser.OFPMatch(ipv4_src=src)
            self.add_flow(datapath, 1, match, actions)
            self._send_package(msg, datapath, in_port, actions)	        
	     
