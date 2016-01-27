from mininet.net import Mininet
from mininet.topo import Topo
net = Mininet()
#creating nodes in the network 
c0 = net.addController()
h0 = net.addHost('h0')
s0 = net.addSwitch('s0')
h1 = net.addHost('h1')
#creating the links betwwen nodes
net.addLink(h0,s0)
net.addLink(h1,s0)
#configuring ip add in interfaces
h0.setIP('192.168.1.1',24)
h1.setIP('192.168.1.2',24)

net.start()
net.pingAll()
net.stop()
