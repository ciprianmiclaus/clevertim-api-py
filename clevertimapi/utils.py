from .session import Session


class list_wrapper(object):
    def __init__(self, content, custom_type=None, readonly=False, session=None):
        assert isinstance(content, list)
        assert session is None or isinstance(session, Session)
        self._content = content
        self._custom_type = custom_type
        self._session = session
        if self._custom_type:
            self._custom_type_content = [self._custom_type(content=ct, session=self._session) for ct in self._content]
        else:
            self._custom_type_content = None
        self._readonly = readonly

    def append(self, item):
        assert not self._readonly, "Cannot modify a readonly property"
        if self._custom_type_content is not None:
            assert isinstance(item, self._custom_type)
            self._custom_type_content.append(item)
            self._content.append(item.key)
        else:
            self._content.append(item)

    def extend(self, iterable):
        assert not self._readonly, "Cannot modify a readonly property"
        for item in iterable:
            self.append(item)

    def insert(self, idx, item):
        assert not self._readonly, "Cannot modify a readonly property"
        if self._custom_type_content is not None:
            assert isinstance(item, self._custom_type)
            self._custom_type_content.insert(idx, item)
            self._content.insert(idx, item.key)
        else:
            self._content.insert(idx, item)

    def remove(self, item):
        assert not self._readonly, "Cannot modify a readonly property"
        if self._custom_type_content is not None:
            assert isinstance(item, self._custom_type)
            self._custom_type_content.remove(item)
            self._content.remove(item.key)
        else:
            self._content.remove(item)

    def pop(self, idx=-1):
        assert not self._readonly, "Cannot modify a readonly property"
        if self._custom_type_content is not None:
            self._content.pop(idx)
            return self._custom_type_content.pop(idx)
        else:
            return self._content.pop(idx)

    def clear(self):
        assert not self._readonly, "Cannot modify a readonly property"
        if self._custom_type_content is not None:
            del self._custom_type_content[:]
        del self._content[:]

    def __getitem__(self, idx):
        if self._custom_type_content is not None:
            return self._custom_type_content[idx]
        else:
            return self._content[idx]

    def __setitem__(self, idx, value):
        assert not self._readonly, "Cannot modify a readonly property"
        if self._custom_type_content:
            assert isinstance(value, self._custom_type)
            self._custom_type_content[idx] = value
            self._content[idx] = value.key
        else:
            self._content[idx] = value

    def __len__(self):
        if self._custom_type_content is not None:
            assert len(self._custom_type_content) == len(self._content)
            return len(self._custom_type_content)
        else:
            return len(self._content)

    def __iter__(self):
        if self._custom_type_content is not None:
            for item in self._custom_type_content:
                yield item
        else:
            for item in self._content:
                yield item
