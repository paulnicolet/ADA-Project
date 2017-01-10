class Flow:
    """
    Represents a flow.

    Parameters:
        src the source Node
        dst the destination Node
        directed True if the flow is directed
        weight the importance of the flow.
    """

    def __init__(self, src, dst, directed=False):
        self.src = src
        self.dst = dst
        self.directed = directed
        self.weight = 0

        # Avoid symmetrical undirected flows
        if not directed and src.name > dst.name:
                self.src = dst
                self.dst = src

    def __str__(self):
        link = '-->' if self.directed else '<-->'
        return '[Flow] {} {} {} ({}).'.format(self.src.name,
                                              link,
                                              self.dst.name,
                                              self.weight)

    def __eq__(self, other):
        cond = (self.src == other.src) and (self.dst == other.dst) and (self.directed == other.directed)
        return isinstance(other, type(self)) and cond

    def __hash__(self):
        mod = 1231 if self.directed else 1237
        return (hash(self.src) ^ hash(self.dst)) % mod

    @staticmethod
    def is_overlapping(i1, i2):
        """
        Returns True if the intervals are overlapping.
        Need strict inequalities : A-B-A should count as (A-B) and (B-A), so
        they should not be detected as overlapping.

        Parameters:
            i1 Interval as tuple
            i2 Interval as tuple
        """
        return (i1[0] < i2[0] < i1[1]) or (i2[0] < i1[0] < i2[1])

    @property
    def symmetrical(self):
        """
        Return the symetrical flow
        """
        return Flow(src=self.dst, dst=self.src, directed=self.directed)
