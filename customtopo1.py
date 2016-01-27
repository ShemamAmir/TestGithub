from mininet.cli import CLI
from mininet.util import dumpNodeConnections
from mininet.node import CPULimitedHost
from mininet.link import TCLink
class singleTopologyPerformance:
          def __init__(self, k=3):
          Topo = singleTopologyPerformance()
          Topo.__init__(self)
                    switch=self.addSwitch('switch1')
                    linkoptions=dict(bw=10,delay='10ms',max_queue_size=1000,use_htb=true)
                    for h in range(k):
                                host=self.addHost('h%s'%(h+1),cpu=.4/k)
                                self.addLink(host,switch, **linloptions)
def performanceTest():
        topo=SingleTopologyPerformance(k=5)
        net=Mininet(topo=topo,host=CPULimitedHost,link=TCLink)
        net.start()
        print "displaying host connection information"
        dumpNodeConnections(net.hosts)
        print "testing network connectivity"
        net-pingAll()
        print "checking BW between h1 and h3"
        h1,h3=net.get('h1','h3')
        net.iperf((h1,h3))
        net.stop()
if __name__ == '__main__':
        setLogLevel('info')
        performanceTest()
        
    
  
