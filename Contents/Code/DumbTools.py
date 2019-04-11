import urllib2


class DumbKeyboard:
    clients = ['Plex for iOS', 'Plex Media Player', 'Plex Web', 'Plex for Samsung']
    KEYS = list('abcdefghijklmnopqrstuvwxyz1234567890-=;[]\\\',./')
    SHIFT_KEYS = list('ABCDEFGHIJKLMNOPQRSTUVWXYZ!@#$%^&*()_+:{}|\"<>?')

    def __init__(self, prefix, oc, callback, dktitle=None, dkthumb=None,
                 dkplaceholder=None, dksecure=False, **kwargs):
        cb_hash = hash(str(callback)+str(kwargs))
        Route.Connect(prefix+'/dumbkeyboard/%s'%cb_hash, self.Keyboard)
        Route.Connect(prefix+'/dumbkeyboard/%s/submit'%cb_hash, self.Submit)
        # Add our directory item
        oc.add(DirectoryObject(key=Callback(self.Keyboard, query=dkplaceholder),
                               title=str(dktitle) if dktitle else \
                                     u'%s'%L('DumbKeyboard Search'),
                               thumb=dkthumb))
        self.Callback = callback
        self.callback_args = kwargs
        self.secure = dksecure

    def Keyboard(self, query=None, shift=False, includeExternalMedia=1):
        if self.secure and query is not None:
            string = ''.join(['*' for i in range(len(query[:-1]))]) + query[-1]
        else:
            string = query if query else ""

        oc = ObjectContainer()
        # Submit
        oc.add(DirectoryObject(key=Callback(self.Submit, query=query),
                               title=u'%s: %s'%(L('Submit'), string.replace(' ', '_'))))
        # Space
        oc.add(DirectoryObject(key=Callback(self.Keyboard,
                                            query=query+" " if query else " "),
                               title='Space'))
        # Backspace (not really needed since you can just hit back)
        if query is not None:
            oc.add(DirectoryObject(key=Callback(self.Keyboard, query=query[:-1]),
                                   title='Backspace'))
        # Shift
        oc.add(DirectoryObject(key=Callback(self.Keyboard, query=query, shift=True),
                               title='Shift'))
        # Keys
        for key in self.KEYS if not shift else self.SHIFT_KEYS:
            oc.add(DirectoryObject(key=Callback(self.Keyboard,
                                                query=query+key if query else key),
                                   title=u'%s'%key))
        return oc

    def Submit(self, query, includeExternalMedia=1):
        kwargs = {'query': query}
        kwargs.update(self.callback_args)
        return self.Callback(**kwargs)
