
from intake.source.base import DataSource
known = [
    'from_process',
    'from_http_server',
    'from_kafka',
    'from_kafka_batched',
    'from_tcp',
    'from_textfile',
    'filenames'
]


class StreamzSource(DataSource):
    name = 'streamz'
    container = 'streamz'

    def __init__(self, method, metadata=None, **kwargs):
        if method not in known:
            raise ValueError('Streamz method %s not known, must be one of'
                             '%s' % (method, known))
        self.method = method
        self.kwargs = kwargs
        self.stream = None
        super().__init__(metadata)

    def _get_schema(self):
        if self.stream is None:
            import streamz.sources
            meth = getattr(streamz.sources, self.method)
            kwargs = self.kwargs.copy()
            kwargs['start'] = False
            self.stream = meth(**kwargs)
        return {'stream': str(self.stream)}

    def read(self):
        self._get_schema()
        return self.stream
