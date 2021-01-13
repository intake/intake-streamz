
from intake.source.base import DataSource
from intake.source import import_name


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
        super().__init__(metadata=metadata)

    def _get_schema(self):
        import streamz
        if self.stream is None:
            stream = streamz.Stream
            for part in self.method:
                kw = part.get("kwargs", {})
                for functional in part.get("func_value", []):
                    kw[functional] = import_name(kw[functional])
                stream = getattr(stream, part["method"])(**part.get("kwargs", {}))
            self.stream = stream
        if self.start:
            self.stream.start()
        return {'stream': str(self.stream)}

    def read(self):
        self._get_schema()
        return self.stream

    def to_dask(self):
        return self.read().scatter()

    @property
    def plot(self):
        # override since there is no hvPlot(streamz), only streamz.hvPlot
        try:
            from hvplot import hvPlot
        except ImportError:
            raise ImportError("The intake plotting API requires hvplot."
                              "hvplot may be installed with:\n\n"
                              "`conda install -c pyviz hvplot` or "
                              "`pip install hvplot`.")
        fields = self.metadata.get('fields', {})
        for attrs in fields.values():
            if 'range' in attrs:
                attrs['range'] = tuple(attrs['range'])
        s = self.read()
        plot = s.plot
        plot._metadata['fields'] = fields
        plot._plots = self.metadata.get('plots', {})
        s.start()
        return plot
