
from intake.source.base import DataSource


class StreamzSource(DataSource):
    name = 'streamz'
    container = 'streamz'
    """
    """

    def __init__(self, method_chain, start=False, metadata=None, **kwargs):
        """

        method_chain: list[tuple(str, dict)]
            Each element of the list is like (method_name, kwargs)
            which will be applied to the stream object in sequence.
        """
        self.method = method_chain
        self.kwargs = kwargs
        self.stream = None
        self.start = start
        super().__init__(metadata)

    def _get_schema(self):
        import streamz
        if self.stream is None:
            stream = streamz.Stream
            for meth, kw in self.method:
                stream = getattr(stream, meth)(**kw)
            self.stream = stream
        if self.start:
            self.stream.start()
        return {'stream': str(self.stream)}

    def read(self):
        self._get_schema()
        return self.stream
