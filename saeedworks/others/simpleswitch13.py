from ryu.base import app_manager
from ryu.controller import ofp_event
from ryu.controller.handler import CONFIG_DISPATCHER, MAIN_DISPATCHER
from ryu.controller.handler import set_ev_cls
from ryu.ofproto import ofproto_v1_3
from ryu.lib.packet import packet
from ryu.lib.packet import ethernet

class SimpleSwitch13(app_manager.RyuApp):
    OFP_VERSIONS = [ofproto_v1_3.OFP_VERSION]	#set OpenFlow Version
	##creator func of class
    def __init__(self, *args, **kwargs):
        super(SimpleSwitch13, self).__init__(*args, **kwargs)
        self.mac_to_port = {}	#dictionary for matching host mac to switch port learn
	##func to add a miss flow rule in switch handshake
    @set_ev_cls(ofp_event.EventOFPSwitchFeatures, CONFIG_DISPATCHER)	#controller will know in config event must call this func
    def switch_features_handler(self, ev):
        datapath = ev.msg.datapath	#the path to switch
        ofproto = datapath.ofproto	#OpenFlow version protocol used in the path 
        parser = datapath.ofproto_parser	#parser for processing this protocol message
        match = parser.OFPMatch()	#make match field it's empty so all packets will be matched
        actions = [parser.OFPActionOutput(ofproto.OFPP_CONTROLLER, ofproto.OFPCML_NO_BUFFER)]	#the action will be send packet to controller and don't buffer the packet
        self.add_flow(datapath, 0, match, actions)	#add flow to the switch table priority 0 is the downest in the table
	##add flow to switch flow table
    def add_flow(self, datapath, priority, match, actions, buffer_id=None):
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser
        inst = [parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS,actions)]	#create the actions instruction rule
        if buffer_id:
            mod = parser.OFPFlowMod(datapath=datapath, buffer_id=buffer_id, priority=priority, match=match,instructions=inst)	#create rule if the packet is buffered in switch
        else:
            mod = parser.OFPFlowMod(datapath=datapath, priority=priority, match=match, instructions=inst)	#create rule when packet not bufferd
        datapath.send_msg(mod)	#send the rule to switch
	##manage the packet in event
    @set_ev_cls(ofp_event.EventOFPPacketIn, MAIN_DISPATCHER)	#when have a packet in this func will call
    def _packet_in_handler(self, ev):
	print self.mac_to_port
        msg = ev.msg
        datapath = msg.datapath
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser
        in_port = msg.match['in_port']	#find the in port 
        pkt = packet.Packet(msg.data)
        eth = pkt.get_protocols(ethernet.ethernet)[0] #find ethernet type lldp,icmp,arp,...
        dst = eth.dst
        src = eth.src
	print(type(src))
	print(type(in_port))
	print(in_port)
        dpid = datapath.id	#switch id
        self.mac_to_port.setdefault(dpid, {})
        self.logger.info("packet in %s %s %s %s", dpid, src, dst, in_port)
        self.mac_to_port[dpid][src] = in_port #learn new source and in port for switch dpid
        if dst in self.mac_to_port[dpid]:
            out_port = self.mac_to_port[dpid][dst]	#if the distination is known 
        else:
            out_port = ofproto.OFPP_FLOOD	#flood if destination is not known
        actions = [parser.OFPActionOutput(out_port)]	#create rule action
        if out_port != ofproto.OFPP_FLOOD:
            match = parser.OFPMatch(in_port=in_port, eth_dst=dst)	#add flow if not flood create a match base on in port and destination mac
            if msg.buffer_id != ofproto.OFP_NO_BUFFER:
                self.add_flow(datapath, 1, match, actions, msg.buffer_id)	#add flow if the packet bufferd in switch
                return
            else:
                self.add_flow(datapath, 1, match, actions)	#packet not bufferd
        data = None	#packet data instance
        if msg.buffer_id == ofproto.OFP_NO_BUFFER:
            data = msg.data	#if notbufferd so add the data to packet
	out = parser.OFPPacketOut(datapath=datapath, buffer_id=msg.buffer_id, in_port=in_port, actions=actions, data=data)
        datapath.send_msg(out)	#in case the action is flood so dont't add flow to flow table just send the packet with the rule
