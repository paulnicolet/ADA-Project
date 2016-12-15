class Flow:
    """
    Represents a flow.

    Parameters:
        src the source Node
        dst the destination Node
        directed True if the flow is directed
        weight importance of the flow
    """
    
    def __init__(self, src, dst, directed=False):
        self.src = src
        self.dst = dst
        self.directed = directed
        self.weight = 0

    def __str__(self):
        link = '-->' if self.directed else '<-->'
        return '[Flow] {} {} {}, weight = {}.'.format(self.src.name,
                                                        link,
                                                        self.dst.name,
                                                        self.weight)
