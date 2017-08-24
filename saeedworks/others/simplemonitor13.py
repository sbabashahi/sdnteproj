from operator import attrgetter
from ryu.app import controller
from ryu.controller import ofp_event
from ryu.controller.handler import MAIN_DISPATCHER, DEAD_DISPATCHER
from ryu.controller.handler import set_ev_cls
from ryu.lib import hub

class SimpleMonitor13(controller.SimpleSwitch13):

    def __init__(self, *args, **kwargs):
        super(SimpleMonitor13, self).__init__(*args, **kwargs)
        self.datapaths = {}	#a dictionary of switchs
        self.monitor_thread = hub.spawn(self._monitor)	#a thread for requesting statics

    @set_ev_cls(ofp_event.EventOFPStateChange, [MAIN_DISPATCHER, DEAD_DISPATCHER])	#connection and disconnection of switch ,add and remove switch to switch dictionary
    def _state_change_handler(self, ev):
        datapath = ev.datapath
        if ev.state == MAIN_DISPATCHER:
            if datapath.id not in self.datapaths:
                self.logger.debug('register datapath: %016x', datapath.id)
                self.datapaths[datapath.id] = datapath
        elif ev.state == DEAD_DISPATCHER:
            if datapath.id in self.datapaths:
                self.logger.debug('unregister datapath: %016x', datapath.id)
                del self.datapaths[datapath.id]

    def _monitor(self):		#request for statical information every 10 sec
        while True:
            for dp in self.datapaths.values():
                self._request_stats(dp)
            hub.sleep(3)

    def _request_stats(self, datapath):		#send request for flow and port status
        self.logger.debug('send stats request: %016x', datapath.id)
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        #req = parser.OFPFlowStatsRequest(datapath)
        #datapath.send_msg(req)

        req = parser.OFPPortStatsRequest(datapath, 0, ofproto.OFPP_ANY)
        datapath.send_msg(req)

    @set_ev_cls(ofp_event.EventOFPFlowStatsReply, MAIN_DISPATCHER)	#receive  flow status replay
    def _flow_stats_reply_handler(self, ev):
        body = ev.msg.body

        #self.logger.info('datapath           eth-dst             out-port packets  bytes')
        #self.logger.info('----------------   -----------------   -------- -------- --------')
        #for stat in sorted([flow for flow in body if flow.priority > 0], key=lambda flow: (flow.match['eth_dst'])):
            #self.logger.info('%016x  %17s %8x %8d %8d', ev.msg.datapath.id,stat.match['eth_dst'], stat.instructions[0].actions[0].port, stat.packet_count, stat.byte_count)

    @set_ev_cls(ofp_event.EventOFPPortStatsReply, MAIN_DISPATCHER)	#receive port status replay
    def _port_stats_reply_handler(self, ev):
        body = ev.msg.body
        self.logger.info('datapath         port       rx-pkts  rx-bytes rx-error  tx-pkts  tx-bytes tx-error')
        self.logger.info('---------------- --------   -------- -------- --------  -------- -------- --------')
        for stat in sorted(body, key=attrgetter('port_no')):
            self.logger.info('%016x %8x %8d %8d %8d %8d %8d %8d', ev.msg.datapath.id, stat.port_no, stat.rx_packets, stat.rx_bytes, stat.rx_errors, stat.tx_packets, stat.tx_bytes, stat.tx_errors)
