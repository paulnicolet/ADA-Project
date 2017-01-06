class Flow:
    """
    Represents a flow.

    Parameters:
        src the source Node
        dst the destination Node
        directed True if the flow is directed
    """

    def __init__(self, src, dst, directed=False):
        self.src = src
        self.dst = dst
        self.directed = directed

    def __str__(self):
        link = '-->' if self.directed else '<-->'
        return '[Flow] {} {} {}.'.format(self.src.name,
                                            link,
                                            self.dst.name)

    def __eq__(self, other):
        cond = (self.src == other.src) and (self.dst == other.dst) and (self.directed == other.directed)
        return isinstance(other, type(self)) and cond

    def __hash__(self):
        mod = 1231 if self.directed else 1237
        return (hash(self.src) ^ hash(self.dst)) % mod

    @property
    def symmetrical(self):
        """
        Return the symetrical flow
        """
        return Flow(src=self.dst, dst=self.src, directed=self.directed)

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
