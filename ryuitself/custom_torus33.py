#!/usr/bin/env python
from mininet.cli import CLI
from mininet.net import Mininet
from mininet.node import RemoteController
from mininet.term import makeTerm


if '__main__' == __name__:
	#create net with a remote controller
	net = Mininet(controller=RemoteController)
	#add controller and set the controller port
	c0 = net.addController('c0', port=6633)
	#adding switch
    	s1 = net.addSwitch('s1')
	s2 = net.addSwitch('s2')
    	s3 = net.addSwitch('s3')
    	s4 = net.addSwitch('s4')
	s5 = net.addSwitch('s5')
  	s6 = net.addSwitch('s6')
    	s7 = net.addSwitch('s7')
	s8 = net.addSwitch('s8')
    	s9 = net.addSwitch('s9')
        #adding hosts
	h1 = net.addHost('h1', ip='10.0.0.1/24', mac='00:00:00:00:00:01')
	h2 = net.addHost('h2', ip='10.0.0.2/24', mac='00:00:00:00:00:02')
	h3 = net.addHost('h3', ip='10.0.0.3/24', mac='00:00:00:00:00:03')
	h4 = net.addHost('h4', ip='10.0.0.4/24', mac='00:00:00:00:00:04')
	h5 = net.addHost('h5', ip='10.0.0.5/24', mac='00:00:00:00:00:05')
	h6 = net.addHost('h6', ip='10.0.0.6/24', mac='00:00:00:00:00:06')
	h7 = net.addHost('h7', ip='10.0.0.7/24', mac='00:00:00:00:00:07')
	h8 = net.addHost('h8', ip='10.0.0.8/24', mac='00:00:00:00:00:08')
	h9 = net.addHost('h9', ip='10.0.0.9/24', mac='00:00:00:00:00:09')
        #adding links switch to hosts
	#net.addLink(host, switch, bw=10, delay='5ms', loss=2, max_queue_size=1000, use_htb=True)
	net.addLink(s1, h1)
	net.addLink(s2, h2)
	net.addLink(s3, h3)
    	net.addLink(s4, h4)
	net.addLink(s5, h5)
	net.addLink(s6, h6)
    	net.addLink(s7, h7)
	net.addLink(s8, h8)
	net.addLink(s9, h9)
        #adding links switch to switch
	net.addLink(s1, s2)
	net.addLink(s1, s3)
	net.addLink(s1, s8)
    	net.addLink(s1, s9)
        net.addLink(s2, s3)
	net.addLink(s2, s4)
        net.addLink(s2, s9)
	net.addLink(s3, s4)
	net.addLink(s3, s5)
        net.addLink(s4, s5)
	net.addLink(s4, s6)
	net.addLink(s5, s6)
        net.addLink(s5, s7)
	net.addLink(s6, s7)
	net.addLink(s6, s8)
        net.addLink(s7, s8)    
	net.addLink(s7, s9)
	net.addLink(s8, s9)
        #start net
	net.build()
	net.start()
	#net.startTerms()
        print("\n\n\nNetwork Topology is Ready...\n\n\n")
        #ch = input("Input Number key to continue...")
        try:
                input("Press Enter to continue... ")
        except SyntaxError:
                pass
	#reciver
	h1.cmd('../ditg/bin/ITGRecv -l rec_log1 &')
	h2.cmd('../ditg/bin/ITGRecv -l rec_log2 &')
	h3.cmd('../ditg/bin/ITGRecv -l rec_log3 &')
	h4.cmd('../ditg/bin/ITGRecv -l rec_log4 &')
	h5.cmd('../ditg/bin/ITGRecv -l rec_log5 &')
	h6.cmd('../ditg/bin/ITGRecv -l rec_log6 &')
	h7.cmd('../ditg/bin/ITGRecv -l rec_log7 &')
	h8.cmd('../ditg/bin/ITGRecv -l rec_log8 &')
	h9.cmd('../ditg/bin/ITGRecv -l rec_log9 &')
	#sender
	h1.cmd('../ditg/bin/ITGSend ./script_file &')
        h2.cmd('../ditg/bin/ITGSend ./script_file &')
	h3.cmd('../ditg/bin/ITGSend ./script_file &')
        h4.cmd('../ditg/bin/ITGSend ./script_file &')
	h5.cmd('../ditg/bin/ITGSend ./script_file &')
        h6.cmd('../ditg/bin/ITGSend ./script_file &')
	h7.cmd('../ditg/bin/ITGSend ./script_file &')
        h8.cmd('../ditg/bin/ITGSend ./script_file &')
	h9.cmd('../ditg/bin/ITGSend ./script_file &')

	CLI(net) 
	#net.stop()
