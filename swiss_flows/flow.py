class Flow:
    """
    Represents a flow.

    Parameters:
        src the source Node
        dst the destination Node
        src_time the emission time at the source Node
        dst_time the emission time at the destination Node
        directed True if the flow is directed
        weight importance of the flow
    """
    
    def __init__(self, src, dst, src_time, dst_time, directed=False):
        self.src = src
        self.dst = dst
        self.src_time = src_time
        self.dst_time = dst_time
        self.directed = directed
        self.weight = 0

    def __str__(self):
        link = '-->' if self.directed else '<-->'
        return '[Flow] {} {} {} {} {}, weight = {}.'.format(self.src.name,
                                                      link,
                                                      self.dst.name,
                                                      self.src_time,
                                                      self.dst_time,
                                                      self.weight)
