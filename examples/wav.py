from structo import SerialiableObject, fixedblob

class RiffHeader(SerialiableObject):
    chunkId: fixedblob(4)

