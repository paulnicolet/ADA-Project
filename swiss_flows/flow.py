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

    @staticmethod
    def is_period_overlap(flow1, flow2):
        """
        The period of a flow is determined by the interval of time between
        src_time and dst_time. This method determines whether the interval
        of two flows overlap.

        Parameters:
            flow1 The first flow to consider
            flow2 The second flow to consider

        Returns:
            boolean saying whether or not the time periods of the two flows overlap
        """

        f1start = flow1.src_time
        f2start = flow2.src_time

        f1end = flow1.dst_time
        f2end = flow2.dst_time

        return (f1start <= f2start <= f1end) or (f2start <= f1start <= f2end)

