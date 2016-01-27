from mininet.topo import Topo  
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel
from mininet.net import Mininet
class SingleSwitchTopo(Topo):
 #"single ewitch connected to n hosts"
 def __init__(self,n=2,**opts):
 #initialize topo
   Topo.__init__(self, **opts)
   switch =self.addSwitch('s1')
 #range 
   for h in range(n):
     host = self.addHost('h%s'(h+1))
     self.addLink(host,switch)
 def simpleTest():
 #"create and test simple network"
   topo = SingleSwitchTopo(n=4)
   net = Mininet(topo)
   net.start()
 print "dumping host connection"
     net.pingAll()
     net.stop()
 if __name__ == '__main__':
 #tell mininet to print useful info
       setLogLevel('info')
       simpleTest()
 
