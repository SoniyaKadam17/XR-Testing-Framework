class PacketGenerator:


    def __init__(self):

        self.total_packets = 0



    def send_packet(self, payload):


        self.total_packets += 1


        # Simulation only
        return True