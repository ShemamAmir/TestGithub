#read this from the bottom up!

from pox.core import core
import pox.openflow.libopenflow_01 as of
import pox.openflow.nicira as nx
import pox.topology.topology as topology
import pox.openflow.topology as oft
from pox.lib.packet import arp, ethernet
from pox.lib.addresses import IPAddr, EthAddr
import networkx as netx
import time

from functools import partial

log = core.getLogger()


# topo is a graph that describes the entire controlled network. it is built in
# the handlers to various discovery events, which might (?) be racey.
topo = netx.Graph()

# this is a map of switches to switch handlers
# it's really only used to allow one worker to find the connection of another
# switch.
# also possibly racey.
switches = {}

class SwitchHandler (object):
    def _handle_PacketIn(self, event, delayed=False):
        packet = event.parsed
      
        # when a packet is received, we know:
        # 1) that there is a vertex in the graph representing the packet src
        topo.add_node(packet.src.toRaw())

        # 2) there is a port on this switch corresponding to the packets in_port
        dp_port = (self.switch.dpid, event.port)
        topo.add_node(dp_port)

        # 3) there is an edge between this switch and that dp_port
        topo.add_edge(self.switch.dpid, dp_port)

        # 4) there is an edge between that dp_port and the source of this packet
        topo.add_edge(dp_port, packet.src.toRaw())

        # only handle IP
        if packet.type != ethernet.IP_TYPE:
            # this may be needed so we don't squash lldp messages
            event.halt = False
            return

        # Determine source and destination vertex
        # Hint: think about the source (packet.src) and destination 
        #   (packet.dst) of a packet

        # Have networkx find the shortest path through the graph
        try: path = netx.shortest_path(topo, srcVertex, dstVertex)
        except: path = None
        if None == path:
            print "No route found!"
            return

        path_str = ""
        cur_switch = None

        # TODO: Install forwarding entries in switches

    def __init__ (self, switch):
        # switches can "exist" for a time even when their connection is down
        # we don't handle the downed switch case, but when it comes back up,
        # this lets us take advantage of the new connection
        def connection_up(connection):
            self.connection = connection
            connection.addListenerByName("PacketIn",
                    self._handle_PacketIn)

        # bookkeeping:
        self.switch = switch
        switches[self.switch.dpid] = self

        # TODO: Add vertex to graph, for switch
        # Switch details:
        #  switch.dpid = unique identifier for switch
        # To add a vertex:
        #   topo.add_node(vertex)

        # register for the connection-up event, and...
        switch.addListenerByName("SwitchConnectionUp",
            lambda event: connection_up(event.connection))
        # fake like it was called, because we missed the first event already
        connection_up(switch._connection)

def launch ():
  # this prevents needing to add these modules on the command line
  from pox.topology import launch
  launch()

  from pox.openflow.discovery import launch
  launch()

  from pox.openflow.topology import launch
  launch()

  #this is called when a switch joins
  def start_switch (event):
    log.debug("Controlling something or whatever!") # % (event.connection,))
    #create a worker instance for each switch
    SwitchHandler(event.switch)
  
  #this is called when a new link is found
  def link_event (event):
        # TODO: Add edge to graph
        # Link details:
        #   event.link.dpid1 = id for switch 1
        #   event.link.port1 = port on switch 1
        #   event.link.dpid2 = id for switch 2
        #   event.link.port2 = port on switch 2
        # To add an edge:
        #   topo.add_edge(srcVertex, dstVertex)

  #register for switch join events *from the topology module*
      core.topology.addListenerByName("SwitchJoin", start_switch)

  #register for link-discovery events *from the discovery modules*
      core.openflow_discovery.addListenerByName("LinkEvent", link_event)
