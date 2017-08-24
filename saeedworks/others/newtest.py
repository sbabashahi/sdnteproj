#!/usr/bin/env python
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import CPULimitedHost
from mininet.link import TCLink
from mininet.term import makeTerm

class Torus(Topo):
	def build(self):
		s1 = self.addSwitch('s1')    #adding switchs
   	s2 = net.addSwitch('s2')
   	s3 = net.addSwitch('s3')
	s4 = net.addSwitch('s4')
   	s5 = net.addSwitch('s5')
    	s6 = net.addSwitch('s6')
    	s7 = net.addSwitch('s7')
    	s8 = net.addSwitch('s8')
    	s9 = net.addSwitch('s9')


    h1 = net.addHost('h1')     #adding hosts
    h2 = net.addHost('h2')
    h3 = net.addHost('h3')
    h4 = net.addHost('h4')
    h5 = net.addHost('h5')
    h6 = net.addHost('h6')
    h7 = net.addHost('h7')
    h8 = net.addHost('h8')
    h9 = net.addHost('h9')


    net.addLink(s1, h1)        #adding links switch to hosts
    net.addLink(s2, h2)
    net.addLink(s3, h3)
    net.addLink(s4, h4)
    net.addLink(s5, h5)
    net.addLink(s6, h6)
    net.addLink(s7, h7)
    net.addLink(s8, h8)
    net.addLink(s9, h9)

    
    net.addLink(s1, s2)        #adding links switch to switch
    net.addLink(s1, s3)
    net.addLink(s1, s8)
    net.addLink(s1, s9)        #adding links switch to switch
    net.addLink(s2, s3)
    net.addLink(s2, s4)
    net.addLink(s2, s9)        #adding links switch to switch
    net.addLink(s3, s4)
    net.addLink(s3, s5)
    net.addLink(s4, s5)        #adding links switch to switch
    net.addLink(s4, s6)
    net.addLink(s5, s6)
    net.addLink(s5, s7)        #adding links switch to switch
    net.addLink(s6, s7)
    net.addLink(s6, s8)
    net.addLink(s7, s8)        #adding links switch to switch
    net.addLink(s7, s9)
    net.addLink(s8, s9)
    
def myTopo():
        topo = Torus()
        net = Mininet(topo=topo)
        net.build()
        net.start()
        print "****Dumping Host connections****"
        dumpNodeConnections(net.hosts)
        #net.startTerms()
        #net.stop()
if __name == '__main__':
    myTopo()
