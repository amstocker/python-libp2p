libp2p for Python
=================

An outline of the libp2p spec as I currently understand it:

- Node Layer
    - This is effectively the highest layer of abstraction (This is basically a nice interface for the swarm layer).
    - The interface consists simply of:
     	```python
     	def id(self):
       		# Returns PeerID object associated with this node.
  
     	def open_stream(self, protocol, remote_peer_info):
       		# Returns stream object representing connection to the peer.  The remote_peer_info
       		# object contains contact information in the form of multiaddresses.
              # (see: https://github.com/jbenet/multiaddr) 
  
     	def set_stream_handler(self, protocol, handler):
       		# Sets handler factory for incoming streams on the given protocol.
     	```
    - *NOTE: In our case this will all be built on some kind of event loop (likely asyncio) and so it will all function with callbacks (cue resounding cry of frustration).*

- Swarm Layer
    - The swarm layer sits on top of all incoming and outgoing *connections* associated with this node.
    - The interface consists of:
    	```python
        def add_transport(self, transport, **options):
          # Adds a transport to be supported by this swarm.  Any transport implementations
            # must inherit from some TBD base class.
            
        def upgrade_connection(self, new_conn, **options):
          # Returns upgraded connections.
            # (I am unsure about what this is for at the moment of writing this.)
            
        def upgrade_to_multiplexer(self, muxer, **options):
          # Returns stream multiplexer from upgraded connection.
            # (I am also unsure about what this is for at the moment of writing this.)
            
        def dial(self, protocol, remote_peer_id, **options):
          # Opens a connection with the remote peer using the transport determined to be
            # the most appropriate.
            
        def set_protocol_handler(self, protocol, handler):
          # Sets handler factory for given protocol.
        ```

- Connections
    - Connections are abstracted to appear as separate streams to the user, but under the hood they may be multiplexed with other streams on the same underlying transport.  This is accomplished using [multistream protocol formats](https://github.com/jbenet/multistream).
        - The point of `multistream` is to have a streaming format that allows easy layering and embedding of multiple streams on the same underlying transport.
      - The `multistream` format requires protocols to be defined as paths (e.g. `/ipfs-dht/0.2.3`), and the stream itself is initiated with a header which contains this information.  The header contains the protocol path (encoded in UTF-8) suffixed by a newline character and prefixed by the header length (encoded as a `varint`; the newline is included in the length):
          ```
          <hdr-len><path>\n
            <arbitrary-stream-data>
            ...
            ```
        - The agenda behind `multistream` is also to develop human readable protocols that can be used with the internet as a whole.  For example:
            ```
            /ipfs/Qmaa4Rw81a3a1VEx4LxB7HADUAXvZFhCoRdBzsMZyZmqHD/ipfs.protocol
            /http/w3id.org/ipfs/ipfs-1.1.0.json
            ```
    - `multistream-select` is a `multistream` protocol that allows for querying and selecting between subprotocols on a stream.  The `multistream-select` protocol listens for or communicates a protocol to speak and then nests (or "upgrades"?) the protocol:
        ```
        /ipfs/QmdRKVhvzyATs3L6dosSb6w8hKuqfZK2SyPVqcYJ5VLYa2/multistream-select/0.3.0
        /ipfs/QmVXZiejj3sXEmxuQxF2RjmFbEiE9w7T82xDn3uYNuhbFb/ipfs-dht/0.2.3
        <dht-message>
        <dht-message>
        ```
