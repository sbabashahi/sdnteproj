#class that used in dijkstra
class priorityDictionary(dict):
    def __init__(self):
        self.__heap = []
        dict.__init__(self)

    def smallest(self):
        '''Find smallest item after removing deleted items from front of heap.'''
        if len(self) == 0:
            raise(IndexError, "smallest of empty priorityDictionary")
        heap = self.__heap
        while heap[0][1] not in self or self[heap[0][1]] != heap[0][0]:
            lastItem = heap.pop()
            insertionPoint = 0
            while 1:
                smallChild = 2 * insertionPoint + 1
                if smallChild + 1 < len(heap) and heap[smallChild] > heap[smallChild + 1]:
                    smallChild += 1
                if smallChild >= len(heap) or lastItem <= heap[smallChild]:
                    heap[insertionPoint] = lastItem
                    break
                heap[insertionPoint] = heap[smallChild]
                insertionPoint = smallChild
        return heap[0][1]

    def __iter__(self):
        '''Create destructive sorted iterator of priorityDictionary.'''
        def iterfn():
            while len(self) > 0:
                x = self.smallest()
                yield x
                del self[x]
        return iterfn()
    def __setitem__(self, key, val):
        '''Change value stored in dictionary and add corresponding pair to heap.
Rebuilds the heap if the number of deleted items gets large, to avoid memory leakage.'''
        dict.__setitem__(self, key, val)
        heap = self.__heap
        if len(heap) > 2 * len(self):
            self.__heap = [(v, k) for k, v in self.iteritems()]
            self.__heap.sort()  # builtin sort probably faster than O(n)-time heapify
        else:
            newPair = (val, key)
            insertionPoint = len(heap)
            heap.append(None)
            while insertionPoint > 0 and newPair < heap[(insertionPoint - 1) // 2]:
                heap[insertionPoint] = heap[(insertionPoint - 1) // 2]
                insertionPoint = (insertionPoint - 1) // 2
            heap[insertionPoint] = newPair
    def setdefault(self, key, val):
        '''Reimplement setdefault to pass through our customized __setitem__.'''
        if key not in self:
            self[key] = val
        return self[key]

###hop_cost
hop_cost = {1: 1, 2:1, 3:1, 4:1}
###nodes and where they connected by which port
vertexs  = {'h1':{'s1':'eth0',},
            'h2':{'s2':'eth0',},
            'h3':{'s3':'eth0',},
            'h4':{'s4':'eth0',},
            'h5':{'s5':'eth0',},
            'h6':{'s6':'eth0',},
            'h7':{'s7':'eth0',},
            'h8':{'s8':'eth0',},
            'h9':{'s9':'eth0',},
            's1':{'h1':'eth1', 's2':'eth2' ,'s3':'eth3' ,'s8':'eth4' ,'s9':'eth5' ,},
            's2':{'h2':'eth1', 's1':'eth2' ,'s3':'eth3' ,'s4':'eth4' ,'s9':'eth5' ,},
            's3':{'h3':'eth1', 's1':'eth2' ,'s2':'eth3' ,'s4':'eth4' ,'s5':'eth5' ,},
            's4':{'h4':'eth1', 's2':'eth2' ,'s3':'eth3' ,'s5':'eth4' ,'s6':'eth5' ,},
            's5':{'h5':'eth1', 's3':'eth2' ,'s4':'eth3' ,'s6':'eth4' ,'s7':'eth5' ,},
            's6':{'h6':'eth1', 's4':'eth2' ,'s5':'eth3' ,'s7':'eth4' ,'s8':'eth5' ,},
            's7':{'h7':'eth1', 's5':'eth2' ,'s6':'eth3' ,'s8':'eth4' ,'s9':'eth5' ,},
            's8':{'h8':'eth1', 's1':'eth2' ,'s6':'eth3' ,'s7':'eth4' ,'s9':'eth5' ,},
            's9':{'h9':'eth1', 's1':'eth2' ,'s2':'eth3' ,'s7':'eth4' ,'s8':'eth5' ,},}

###edges and the cost of them
edges   = { 'h1':{'s1': 1,},
            'h2':{'s2': 1,},
            'h3':{'s3': 1,},
            'h4':{'s4': 1,},
            'h5':{'s5': 1,},
            'h6':{'s6': 1,},
            'h7':{'s7': 1,},
            'h8':{'s8': 1,},
            'h9':{'s9': 1 ,},
            's1':{'h1': 1 , 's2': 1 ,'s3': 1 ,'s8': 1 ,'s9': 1 ,},
            's2':{'h2': 1 , 's1': 1 ,'s3': 1 ,'s4': 1 ,'s9': 1 ,},
            's3':{'h3': 1 , 's1': 1 ,'s2': 1 ,'s4': 1 ,'s5': 1 ,},
            's4':{'h4': 1 , 's2': 1 ,'s3': 1 ,'s5': 1 ,'s6': 1 ,},
            's5':{'h5': 1 , 's3': 1 ,'s4': 1 ,'s6': 1 ,'s7': 1 ,},
            's6':{'h6': 1 , 's4': 1 ,'s5': 1 ,'s7': 1 ,'s8': 1 ,},
            's7':{'h7': 1 , 's5': 1 ,'s6': 1 ,'s8': 1 ,'s9': 1 ,},
            's8':{'h8': 1 , 's1': 1 ,'s6': 1 ,'s7': 1 ,'s9': 1 ,},
            's9':{'h9': 1 , 's1': 1 ,'s2': 1 ,'s7': 1 ,'s8': 1 ,},}
####
alter_paths = { 's1': {'s2': { 'path1': {'path': ['s1', 's3', 's2'], 'cost': 0}, 'path2': {'path': ['s1', 's9', 's2'], 'cost': 0},
                               'path3': {'path': ['s1', 's8', 's9', 's2'], 'cost': 0}, 'path4': {'path': ['s1', 's3', 's4', 's2'], 'cost': 0}},
                       's3': { 'path1': {'path': ['s1', 's2', 's3'], 'cost': 0}, 'path2': {'path': ['s1' ,'s2', 's4', 's3'], 'cost': 0},
                               'path3': {'path': ['s1', 's9', 's2', 's3'], 'cost': 0}},
                       's8': { 'path1': {'path': ['s1', 's9', 's8'], 'cost': 0}, 'path2': {'path': ['s1' ,'s9', 's7', 's8'], 'cost': 0},
                               'path3': {'path': ['s1', 's2', 's9', 's8'], 'cost': 0}},
                       's9': { 'path1': {'path': ['s1', 's2', 's9'], 'cost': 0}, 'path2': {'path': ['s1', 's8', 's9'], 'cost': 0},
                               'path3': {'path': ['s1', 's3', 's2', 's9'], 'cost': 0}, 'path4': {'path': ['s1', 's8', 's7', 's9'], 'cost': 0}},
                      },
                's2': {'s1': { 'path1': {'path': ['s2', 's3', 's1'], 'cost': 0}, 'path2': {'path': ['s2', 's9', 's1'], 'cost': 0},
                               'path3': {'path': ['s2', 's9', 's8', 's1'], 'cost': 0}, 'path4': {'path': ['s2', 's4', 's3', 's1'], 'cost': 0}},
                       's4': { 'path1': {'path': ['s2', 's3', 's4'], 'cost': 0}, 'path2': {'path': ['s2' ,'s3', 's5', 's4'], 'cost': 0},
                               'path3': {'path': ['s2', 's1', 's3', 's4'], 'cost': 0}},
                       's9': { 'path1': {'path': ['s2', 's1', 's9'], 'cost': 0}, 'path2': {'path': ['s2' ,'s1', 's8', 's9'], 'cost': 0},
                               'path3': {'path': ['s2', 's3', 's1', 's9'], 'cost': 0}},
                       's3': { 'path1': {'path': ['s2', 's4', 's3'], 'cost': 0}, 'path2': {'path': ['s2', 's1', 's3'], 'cost': 0},
                               'path3': {'path': ['s2', 's4', 's5', 's3'], 'cost': 0}, 'path4': {'path': ['s2', 's9', 's1', 's3'], 'cost': 0}},
                      },
                's3': {'s2': { 'path1': {'path': ['s3', 's1', 's2'], 'cost': 0}, 'path2': {'path': ['s3', 's4', 's2'], 'cost': 0},
                               'path3': {'path': ['s3', 's1', 's9', 's2'], 'cost': 0}, 'path4': {'path': ['s3', 's5', 's4', 's2'], 'cost': 0}},
                       's1': { 'path1': {'path': ['s3', 's2', 's1'], 'cost': 0}, 'path2': {'path': ['s3' ,'s2', 's9', 's1'], 'cost': 0},
                               'path3': {'path': ['s3', 's4', 's2', 's1'], 'cost': 0}},
                       's5': { 'path1': {'path': ['s3', 's4', 's5'], 'cost': 0}, 'path2': {'path': ['s3' ,'s2', 's4', 's5'], 'cost': 0},
                               'path3': {'path': ['s3', 's4', 's6', 's5'], 'cost': 0}},
                       's4': { 'path1': {'path': ['s3', 's2', 's4'], 'cost': 0}, 'path2': {'path': ['s3', 's5', 's4'], 'cost': 0},
                               'path3': {'path': ['s3', 's1', 's2', 's4'], 'cost': 0}, 'path4': {'path': ['s3', 's5', 's6', 's4'], 'cost': 0}},
                      },
                's4': {'s3': { 'path1': {'path': ['s4', 's2', 's3'], 'cost': 0}, 'path2': {'path': ['s4', 's5', 's3'], 'cost': 0},
                               'path3': {'path': ['s4', 's2', 's1', 's3'], 'cost': 0}, 'path4': {'path': ['s4', 's6', 's5', 's3'], 'cost': 0}},
                       's2': { 'path1': {'path': ['s4', 's3', 's2'], 'cost': 0}, 'path2': {'path': ['s4' ,'s5', 's3', 's2'], 'cost': 0},
                               'path3': {'path': ['s4', 's3', 's1', 's2'], 'cost': 0}},
                       's6': { 'path1': {'path': ['s4', 's5', 's6'], 'cost': 0}, 'path2': {'path': ['s4' ,'s3', 's5', 's6'], 'cost': 0},
                               'path3': {'path': ['s4', 's5', 's7', 's6'], 'cost': 0}},
                       's5': { 'path1': {'path': ['s4', 's3', 's5'], 'cost': 0}, 'path2': {'path': ['s4', 's6', 's5'], 'cost': 0},
                               'path3': {'path': ['s4', 's2', 's3', 's5'], 'cost': 0}, 'path4': {'path': ['s4', 's6', 's7', 's5'], 'cost': 0}},
                      },
                's5': {'s4': { 'path1': {'path': ['s5', 's3', 's4'], 'cost': 0}, 'path2': {'path': ['s5', 's6', 's4'], 'cost': 0},
                               'path3': {'path': ['s5', 's3', 's2', 's4'], 'cost': 0}, 'path4': {'path': ['s5', 's7', 's6', 's4'], 'cost': 0}},
                       's3': { 'path1': {'path': ['s5', 's4', 's3'], 'cost': 0}, 'path2': {'path': ['s5' ,'s4', 's2', 's3'], 'cost': 0},
                               'path3': {'path': ['s5', 's6', 's4', 's3'], 'cost': 0}},
                       's7': { 'path1': {'path': ['s5', 's6', 's7'], 'cost': 0}, 'path2': {'path': ['s5' ,'s6', 's8', 's7'], 'cost': 0},
                               'path3': {'path': ['s5', 's4', 's6', 's7'], 'cost': 0}},
                       's6': { 'path1': {'path': ['s5', 's4', 's6'], 'cost': 0}, 'path2': {'path': ['s5', 's7', 's6'], 'cost': 0},
                               'path3': {'path': ['s5', 's3', 's4', 's6'], 'cost': 0}, 'path4': {'path': ['s5', 's7', 's8', 's6'], 'cost': 0}},
                      },
                's6': {'s5': { 'path1': {'path': ['s6', 's4', 's5'], 'cost': 0}, 'path2': {'path': ['s6', 's7', 's5'], 'cost': 0},
                               'path3': {'path': ['s6', 's4', 's3', 's5'], 'cost': 0}, 'path4': {'path': ['s6', 's8', 's7', 's5'], 'cost': 0}},
                       's4': { 'path1': {'path': ['s6', 's5', 's4'], 'cost': 0}, 'path2': {'path': ['s6' ,'s5', 's3', 's4'], 'cost': 0},
                               'path3': {'path': ['s6', 's7', 's5', 's4'], 'cost': 0}},
                       's8': { 'path1': {'path': ['s6', 's7', 's8'], 'cost': 0}, 'path2': {'path': ['s6' ,'s5', 's7', 's8'], 'cost': 0},
                               'path3': {'path': ['s6', 's7', 's9', 's8'], 'cost': 0}},
                       's7': { 'path1': {'path': ['s6', 's5', 's7'], 'cost': 0}, 'path2': {'path': ['s6', 's8', 's7'], 'cost': 0},
                               'path3': {'path': ['s6', 's8', 's9', 's7'], 'cost': 0}, 'path4': {'path': ['s6', 's4', 's5', 's7'], 'cost': 0}},
                      },
                's7': {'s6': { 'path1': {'path': ['s7', 's5', 's6'], 'cost': 0}, 'path2': {'path': ['s7', 's8', 's6'], 'cost': 0},
                               'path3': {'path': ['s7', 's9', 's8', 's6'], 'cost': 0}, 'path4': {'path': ['s7', 's5', 's4', 's6'], 'cost': 0}},
                       's5': { 'path1': {'path': ['s7', 's6', 's5'], 'cost': 0}, 'path2': {'path': ['s7' ,'s8', 's6', 's5'], 'cost': 0},
                               'path3': {'path': ['s7', 's6', 's4', 's5'], 'cost': 0}},
                       's9': { 'path1': {'path': ['s7', 's8', 's9'], 'cost': 0}, 'path2': {'path': ['s7' ,'s6', 's8', 's9'], 'cost': 0},
                               'path3': {'path': ['s7', 's8', 's1', 's9'], 'cost': 0}},
                       's8': { 'path1': {'path': ['s7', 's6', 's8'], 'cost': 0}, 'path2': {'path': ['s7', 's9', 's8'], 'cost': 0},
                               'path3': {'path': ['s7', 's5', 's6', 's8'], 'cost': 0}, 'path4': {'path': ['s7', 's9', 's1', 's8'], 'cost': 0}},
                      },
                's8': {'s7': { 'path1': {'path': ['s8', 's6', 's7'], 'cost': 0}, 'path2': {'path': ['s8', 's9', 's7'], 'cost': 0},
                               'path3': {'path': ['s8', 's6', 's5', 's7'], 'cost': 0}, 'path4': {'path': ['s8', 's1', 's9', 's7'], 'cost': 0}},
                       's6': { 'path1': {'path': ['s8', 's7', 's6'], 'cost': 0}, 'path2': {'path': ['s8' ,'s7', 's5', 's6'], 'cost': 0},
                               'path3': {'path': ['s8', 's9', 's7', 's6'], 'cost': 0}},
                       's1': { 'path1': {'path': ['s8', 's9', 's1'], 'cost': 0}, 'path2': {'path': ['s8' ,'s7', 's9', 's1'], 'cost': 0},
                               'path3': {'path': ['s8', 's9', 's2', 's1'], 'cost': 0}},
                       's9': { 'path1': {'path': ['s8', 's1', 's9'], 'cost': 0}, 'path2': {'path': ['s8', 's7', 's9'], 'cost': 0},
                               'path3': {'path': ['s8', 's1', 's2', 's9'], 'cost': 0}, 'path4': {'path': ['s8', 's6', 's7', 's9'], 'cost': 0}},
                      },
                's9': {'s1': { 'path1': {'path': ['s9', 's2', 's1'], 'cost': 0}, 'path2': {'path': ['s9', 's8', 's1'], 'cost': 0},
                               'path3': {'path': ['s9', 's2', 's3', 's1'], 'cost': 0}, 'path4': {'path': ['s9', 's7', 's8', 's1'], 'cost': 0}},
                       's2': { 'path1': {'path': ['s9', 's1', 's2'], 'cost': 0}, 'path2': {'path': ['s9' ,'s1', 's3', 's2'], 'cost': 0},
                               'path3': {'path': ['s9', 's8', 's1', 's2'], 'cost': 0}},
                       's7': { 'path1': {'path': ['s9', 's8', 's7'], 'cost': 0}, 'path2': {'path': ['s9' ,'s8', 's6', 's7'], 'cost': 0},
                               'path3': {'path': ['s9', 's1', 's8', 's7'], 'cost': 0}},
                       's8': { 'path1': {'path': ['s9', 's1', 's8'], 'cost': 0}, 'path2': {'path': ['s9', 's7', 's8'], 'cost': 0},
                               'path3': {'path': ['s9', 's2', 's1', 's8'], 'cost': 0}, 'path4': {'path': ['s9', 's7', 's6', 's8'], 'cost': 0}},
                      },
              }

####
port_stat_time = 0
paths_to_change = []
###dijkstra with two matrix cost and next hop
def dijkstra(graph ,start ,end= None):
    D = {}  # dictionary of final distances
    P = {}  # dictionary of predecessors
    Q = priorityDictionary()  # est.dist. of non-final vert.
    Q[start] = 0

    for v in Q:
        D[v] = Q[v]
        if v == end: break
        for w in graph[v]:
            vwLength = D[v] + graph[v][w]
            if w in D:
                if vwLength < D[w]:
                    raise(ValueError,"Dijkstra: found better path to already-final vertex")
            elif w not in Q or vwLength < Q[w]:
                Q[w] = vwLength
                P[w] = v

    return (D, P)
###shortest path between source and destination
def shortestPath(G,start,end):
    D,P = dijkstra(G,start,end)
    Path = []
    cost = 0
    while 1:
        Path.append(end)
        if end == start: break
        end1 = end
        end = P[end]
        cost = cost + G[end][end1]
    Path.reverse()
    return Path ,cost
###all the shortest path form source
def shortestPath2(G, start):
    D,P= dijkstra(G,start)
    nodes = set(G.keys())
    path = [[] for y in range(10)]
    for m in nodes:
        if m[0] == 's': continue
        if m == start : continue
        end = m
        while 1:
            path[int(m[1])].append(end)
            if end == start: break
            end = P[end]
        path[int(m[1])].reverse()
    return path

###all shortest path for all nodes
def graphShortest(G):
    nodes = set(G.keys())
    path = [[] for y in range(90)]
    for m in nodes:
        if m[0] == 's' : continue
        pathm = shortestPath2(G,m)
        for i in range (10):
            path[((int(m[1])-1)*10)+i] = pathm[i]
    return path
###########################################################

from ryu.base import app_manager
from ryu.controller import ofp_event
from ryu.controller.handler import CONFIG_DISPATCHER, MAIN_DISPATCHER
from ryu.ofproto import ofproto_v1_3
from ryu.controller.handler import set_ev_cls
from ryu.lib.packet import packet
from ryu.lib.packet import ethernet
from operator import attrgetter
from ryu.lib import hub
import sys

class SimpleSwitch13(app_manager.RyuApp):
    OFP_VERSIONS = [ofproto_v1_3.OFP_VERSION]	#set OpenFlow Version
    ##creator func of class
    def __init__(self, *args, **kwargs):
        super(SimpleSwitch13, self).__init__(*args, **kwargs)
        self.path = graphShortest(edges)	#execute the shortest path in initialtion
    	#from pprint import pprint
	#pprint(self.path)
	self.prepath = self.path
	self.edgesnow = {}
    	for host1 in edges:
	    self.edgesnow[host1] = {}
    	    for host2 in edges[host1]:
		edges[host1][host2] = 0
        	self.edgesnow[host1][host2] = 0
        self.switchdic = {}
	self.prior = 1
        self.linko = 1
        self.thsh = 5000
        self.monitor_thread = hub.spawn(self._monitor)	#a thread for requesting statics


    ##func to add a miss flow rule in switch handshake
    @set_ev_cls(ofp_event.EventOFPSwitchFeatures, CONFIG_DISPATCHER)	#controller will know in config event must call this func
    def switch_features_handler(self, ev):
        datapath = ev.msg.datapath	#the path to switch
        self.switchdic['s'+str(datapath.id)]=datapath
        ofproto = datapath.ofproto	#OpenFlow version protocol used in the path
        parser = datapath.ofproto_parser	#parser for processing this protocol message
        #Rule to match if there is no matched yet with downest priority
        match = parser.OFPMatch()	#make match field it's empty so all packets will be matched
        actions = [parser.OFPActionOutput(ofproto.OFPP_CONTROLLER, ofproto.OFPCML_NO_BUFFER)]	#the action will be send packet to controller and don't buffer the packet
        self.add_flow(datapath, 0, match, actions)	#add flow to the switch table priority 0 is the downest in the table
        ###########new code here###########
        dstflood = 'ff:ff:ff:ff:ff:ff'	#address for flooding
        hostport = 1	#port of connected host to every switch
        switch = 's'+str(datapath.id)	#switch that we connect for handeling
        print('Installing Rules Of : ' + switch)
        ##calcuate next switch
        if datapath.id != 9:
            nextswitch = 's'+str(datapath.id+1)
        else:
            nextswitch = 's1'
        nextswitchport = int(vertexs[switch][nextswitch][-1])	#port connected to next switch
        ##Rule1 if flood and is from switch host drop packet
        actions = []	#no action for droping
        match = parser.OFPMatch(eth_dst=dstflood, eth_src='00:00:00:00:00:0'+str(datapath.id))
        self.add_flow(datapath, 41, match, actions)
        ##Rule2 if flood and received from switch host send to next switch this rule have more priority to Rule1
        actions = [parser.OFPActionOutput(nextswitchport)]
        match = parser.OFPMatch(eth_dst=dstflood, in_port=hostport)
        self.add_flow(datapath, 42, match, actions)
        ##Rule3 if flood send to switch host and next switch
        actions = [parser.OFPActionOutput(hostport),parser.OFPActionOutput(nextswitchport)]
        match = parser.OFPMatch(eth_dst=dstflood)
        self.add_flow(datapath, 40, match, actions)
        ##get every route that this switch is in it and install the rule
        switchinpath = [(index, row.index(switch)) for index, row in enumerate(self.path) if switch in row]	#all the paths that this switch is there
	for i in range(len(switchinpath)):
            srchost = '00:00:00:00:00:0'+self.path[switchinpath[i][0]][0][1]	#srouce host of this route
            dsthost = '00:00:00:00:00:0'+self.path[switchinpath[i][0]][-1][1]	#destination host of this route
            nexteth = int(vertexs[self.path[switchinpath[i][0]][(switchinpath[i][1])]][self.path[switchinpath[i][0]][(switchinpath[i][1]) + 1]][3])	#which port must send the packet
            #ipdst = '10.0.0.'+self.path[switchinpath[i][0]][-1][1]	#destination host ip address
            actions = [parser.OFPActionOutput(nexteth)]
            match = parser.OFPMatch(eth_src=srchost, eth_dst=dsthost)
            self.add_flow(datapath, 1, match, actions, time=25)

    ##add flow to switch flow table function
    def add_flow(self, datapath, priority, match, actions, time=0, buffer_id=None):
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser
        inst = [parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS,actions)]	#create the actions instruction rule
        if buffer_id:
            mod = parser.OFPFlowMod(command=ofproto.OFPFC_ADD, datapath=datapath, buffer_id=buffer_id, hard_timeout=time, priority=priority, match=match, instructions=inst)	#create rule if the packet is buffered in switch
        else:
            mod = parser.OFPFlowMod(command=ofproto.OFPFC_ADD, datapath=datapath, priority=priority, match=match, hard_timeout=time, instructions=inst)	#create rule when packet not bufferd
        datapath.send_msg(mod)	#send the rule to switch

    ##remove flow from switch flow table
    def rem_flow(self, datapath, priority, match, actions, port = 0):
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser
        if port == 0 :
    	    print('Port not insert')
    	    port = ofproto.OFPP_ANY
        inst = []
        mod = parser.OFPFlowMod(command=ofproto.OFPFC_DELETE, datapath=datapath, priority=priority, out_port=port, match=match, out_group=ofproto.OFPG_ANY, instructions=inst)
        datapath.send_msg(mod)


    ##manage the packet in event if a packet haven't matched to any rule
    @set_ev_cls(ofp_event.EventOFPPacketIn, MAIN_DISPATCHER)	#when have a packet in this func will call
    def _packet_in_handler(self, ev):
        msg = ev.msg	#message from this packet in event
        datapath = msg.datapath
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser
        in_port = msg.match['in_port']	#find the in port
        pkt = packet.Packet(msg.data)
        eth = pkt.get_protocols(ethernet.ethernet)[0] #find ethernet type lldp,icmp,arp,...
        dst = eth.dst
        src = eth.src
        dpid = datapath.id	#switch id
        #print('switch '+str(dpid)+' new incoming from '+str(src)+' to '+str(dst))	#need more...


    def _monitor(self):		#request for statical information every 10 sec
        round=0
	while True:
            if round == 0:
                round = 1
                hub.sleep(10)
            else:
                hub.sleep(5)
            for dp in self.switchdic.values():
		self._request_stats(dp)
    
    def rebuildnet(self):
	for sw in self.switchdic:
            ofproto = self.switchdic[sw].ofproto	#OpenFlow version protocol used in the path
            parser = self.switchdic[sw].ofproto_parser	#parser for processing this protocol message
            ###add flow
	    switchinpath = [(index, row.index(sw)) for index, row in enumerate(self.path) if sw in row]	#all the paths that this switch is there
            from pprint import pprint; pprint(self.path)
	    for i in range(len(switchinpath)):
                srchost = '00:00:00:00:00:0'+self.path[switchinpath[i][0]][0][1]	#srouce host of this route
                dsthost = '00:00:00:00:00:0'+self.path[switchinpath[i][0]][-1][1]	#destination host of this route
                print(srchost,dsthost, sw)
                nexteth = int(vertexs[self.path[switchinpath[i][0]][(switchinpath[i][1])]][self.path[switchinpath[i][0]][(switchinpath[i][1]) + 1]][3])	#which port must send the packet
                #ipdst = '10.0.0.'+self.path[switchinpath[i][0]][-1][1]	#destination host ip address
                actions = [parser.OFPActionOutput(nexteth)]
                match = parser.OFPMatch(eth_src=srchost, eth_dst=dsthost)
                self.add_flow(self.switchdic[sw], self.prior+1, match, actions, time=25)
	    
	self.prior += 1 


    def _request_stats(self, datapath):		#send request for flow and port status
        #self.logger.debug('send stats request: %016x', datapath.id)
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser
        ###Port Stat Req
    	req = parser.OFPPortStatsRequest(datapath, 0, ofproto.OFPP_ANY)
        datapath.send_msg(req)
    	###Flow Stat Req
    	req = parser.OFPFlowStatsRequest(datapath)
    	datapath.send_msg(req)


    def findNextHop(self, host, port):
        return [key for key, value in vertexs[host].items() if value == port][0]


    ####Flow Stat
    @set_ev_cls(ofp_event.EventOFPFlowStatsReply, MAIN_DISPATCHER)
    def _flow_stats_reply_handler(self, ev):
        body = ev.msg.body
        #self.logger.info('datapath         in-port           eth-dst           out-port   packets  bytes')
        #self.logger.info('---------------- ' '----------------- ----------------- ' '--------   -----    ------')
	#for stat in sorted([flow for flow in body if flow.priority==1], key=lambda flow: (flow.match['eth_src'],flow.match['eth_dst'])):
    	    #self.logger.info('%016x %8s %17s %8d %8d', ev.msg.datapath.id, stat.match['eth_src'], stat.match['eth_dst'], stat.packet_count, stat.byte_count)


    ####Port Stat
    @set_ev_cls(ofp_event.EventOFPPortStatsReply, MAIN_DISPATCHER)	#receive port status replay
    def _port_stats_reply_handler(self, ev):
        global paths_to_change
        #print('Port Stat New Income...')
    	body = ev.msg.body
        global port_stat_time
        port_stat_time = port_stat_time + 1	
        for stat in sorted(body, key=attrgetter('port_no')):
	    if stat.port_no > 5:
                continue
            nowswitch = str('s'+str(ev.msg.datapath.id))
            nowport = 'eth'+str(stat.port_no)
            nexthop = self.findNextHop(nowswitch, nowport)
            self.edgesnow[nowswitch][nexthop] = (int(stat.rx_bytes) + int(stat.tx_bytes)) -  edges[nowswitch][nexthop]
            #print(nowswitch, nexthop , self.edgesnow[nowswitch][nexthop], edges[nowswitch][nexthop] )
            edges[nowswitch][nexthop] = int(stat.rx_bytes) + int(stat.tx_bytes)
        #check to get report from all switches
        if port_stat_time == 9 and self.linko:
            self.linko = 0
            print('done.....')
            port_stat_time = 0
	    self.max_link()
	    self.check_links()
            self.add_alter_links()
            self.rebuildnet()
            paths_to_change = []
            #from pprint import pprint; pprint(self.edgesnow)

    def install_path(self, src, dst, path):
        #install path that must be replaced
        srchost = '00:00:00:00:00:0' + src[-1]
        dsthost = '00:00:00:00:00:0' + dst[-1]
        for item in range(len(path)-1):
            switch = path[item]
            datapath = self.switchdic[switch]
            ofproto = datapath.ofproto  #OpenFlow version protocol use$
            parser = datapath.ofproto_parser
            nexteth = int(vertexs[path[item]][path[item+1]][-1])
            actions = [parser.OFPActionOutput(nexteth)]
            match = parser.OFPMatch(eth_src=srchost, eth_dst=dsthost)
            self.add_flow(datapath, 1, match, actions)


    def add_alter_links(self):
        #for path that need to changed remove link and call install path
        for switch in self.switchdic:
	    datapath = self.switchdic[switch]
            ofproto = datapath.ofproto  #OpenFlow version protocol use$
            parser = datapath.ofproto_parser
            for path in paths_to_change:
                if path[2] == switch:	#if path is for current switch
                    srchost = '00:00:00:00:00:0'+path[0][-1]
                    dsthost = '00:00:00:00:00:0'+path[1][-1]
                    x = (int(path[0][-1]) - 1) * 10 + int(path[1][-1])	#find the flow that match this path
                    index = self.path[x].index(path[2])
                    del self.path[x][index]	#delete head and tail
                    del self.path[x][index]
                    for item in path[4]:	#insert new path
                        self.path[x].insert(index, item)
                        index = index + 1
                    while len(self.path[x]) != len(set(self.path[x])):	#check if path has loop
                       find = 0
                       for item in range(1, len(self.path[x])-1):
                           for item2 in range(item+1, len(self.path[x])-1):
                               if self.path[x][item] == self.path[x][item2]:
                                   self.path[x] = self.path[x][:item] + self.path[x][item2:]	#delete finded loop
                                   find = 1
                                   if find:
                                      break
                           if find:
                               find = 0
                               break


    def rebuild_link(self, s1, s2, cost):
        #create a list of paths that need to change 
        #min_cost = cost
        #for path in range(1,len(alter_paths[s1][s2])+1):
            #if min_cost > alter_paths[s1][s2]['path'+str(path)]['cost']*hop_cost[len(alter_paths[s1][s2]['path'+str(path)]['path'])]:	#TODO need to check len
	#	    min_path = alter_paths[s1][s2]['path'+str(path)]['path']
	#	    min_cost = alter_paths[s1][s2]['path'+str(path)]['cost']
        #if min_cost < cost:	#if path need to change
        if len(alter_paths[s1][s2]) == 3:
            min_path = alter_paths[s1][s2]['path'+str(1)]['path']
        elif alter_paths[s1][s2]['path'+str(1)]['cost'] > alter_paths[s1][s2]['path'+str(2)]['cost']:
            min_path = alter_paths[s1][s2]['path'+str(2)]['path']
        else:
            min_path = alter_paths[s1][s2]['path'+str(1)]['path']
        for path in self.path:
	    if len(path):
	        for switch in range(1, len(path)-2):	#find paths that use this link
		    if path[switch] == s1 and path[switch+1] == s2:
		        paths_to_change.append([path[0], path[-1], s1, s2, min_path]) #add path to paths_to_change
		        break
            #need_to_change = need_to_cahnge + [(h1,h2,s1,s2,min_path)]


    def check_links(self):
        #check if any of link has traffic more than thereshold
        for switch in range(1,10):
            thisswitch='s'+str(switch)
            for item in self.edgesnow[thisswitch]:
                if item[0] == 's':
                    if self.thsh < self.edgesnow[thisswitch][item]:
                        self.rebuild_link(thisswitch, item, self.edgesnow[thisswitch][item])


    def max_link(self):
        #find the max cost in every alter_paths path
        for switch1 in alter_paths:
            for switch2 in alter_paths[switch1]:
                for spath in range(1,len(alter_paths[switch1][switch2])+1):
                    alter_paths[switch1][switch2]['path'+str(spath)]['cost'] = 0
                    for path in range(len(alter_paths[switch1][switch2]['path'+str(spath)]['path'])-1):
                        #print(path)
                        #print(switch1, switch2, alter_paths[switch1][switch2]['path'+str(spath)]['path'][path], alter_paths[switch1][switch2]['path'+str(spath)]['path'][path+1])
                        sl1 = alter_paths[switch1][switch2]['path'+str(spath)]['path'][path]
                        sl2 = alter_paths[switch1][switch2]['path'+str(spath)]['path'][path+1]
                        #print(self.edgesnow[sl0][sl2])
                        if alter_paths[switch1][switch2]['path'+str(spath)]['cost'] < self.edgesnow[sl1][sl2]:
                            alter_paths[switch1][switch2]['path'+str(spath)]['cost'] = self.edgesnow[sl1][sl2]
