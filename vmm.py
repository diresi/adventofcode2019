
class VirtualMemory(object):
    CHUNK_SIZE = 0x100
    CHUNK_SHIFT = 8
    ADDR_MASK = 0xFF
    CHUNK_MASK = ADDR_MASK ^ 0xFFFFFFFF # 4 addressable bytes

    @classmethod
    def unmap_addr(cls, addr):
        chunk = addr >> cls.CHUNK_SHIFT
        addr = addr & cls.ADDR_MASK
        return chunk, addr

    def __init__(self, data=None):
        self._chunks = self.chunkify(data or [])
        self.verbose = False

    def __len__(self):
        if not self._chunks:
            return 0
        max_chunk_start = max(self._chunks)
        max_chunk_start = (max_chunk_start << self.CHUNK_SHIFT) & self.CHUNK_MASK
        return max_chunk_start + self.CHUNK_SIZE

    def __getitem__(self, vaddr):
        def get_scalar_item(vaddr):
            chunk, addr = self.unmap_addr(vaddr)
            chunk_data = self._chunks.get(chunk)
            if chunk_data is None:
                if self.verbose:
                    print(repr(self))
                raise IndexError("va=%s, c=%s, a=%s" % (vaddr, chunk, addr))
            return chunk_data[addr]

        # simple way, map slice access to a bunch of single item accesses
        # if you're looking for a way to improve, this is a good starting point
        if isinstance(vaddr, slice):
            indices = vaddr.indices(vaddr.stop)
            return [get_scalar_item(i) for i in range(*indices)]
        return get_scalar_item(vaddr)

    def __setitem__(self, vaddr, value):
        def set_scalar_item(vaddr, value):
            chunk, addr = self.unmap_addr(vaddr)
            chunk_data = self._chunks.get(chunk)
            if chunk_data is None:
                # autogrow, sparse
                chunk_data = [0] * self.CHUNK_SIZE
                self._chunks[chunk] = chunk_data

            chunk_data[addr] = value

        # slice assignment is too hard, we don't need it yet
        assert isinstance(vaddr, int)
        return set_scalar_item(vaddr, value)

    def chunkify(self, data):
        chunks = {}
        i = 0
        offset = 0

        size = self.CHUNK_SIZE
        dlen = len(data)
        while offset < dlen:
            cdata = data[offset:offset+size]
            clen = len(cdata)
            if clen < size:
                cdata.extend([0] * (size - clen))
            chunks[i] = cdata
            i += 1
            offset += size

        return chunks

    def __repr__(self):
        txt = [repr((x, self._chunks[x])) for x in sorted(self._chunks)]
        return "\n".join(txt)

def test():
    vmm = VirtualMemory()
    assert len(vmm) == 0

    try:
        vmm[0]
        assert False
    except IndexError:
        pass

    vmm[0] = 1
    assert len(vmm) == vmm.CHUNK_SIZE
    assert vmm[0] == 1
    for x in range(1, vmm.CHUNK_SIZE):
        assert vmm[x] == 0

    vmm = VirtualMemory()
    vmm[vmm.CHUNK_SIZE-2] = 1
    vmm[vmm.CHUNK_SIZE-1] = 2
    vmm[vmm.CHUNK_SIZE] = 3
    vmm[vmm.CHUNK_SIZE+1] = 4
    assert vmm[vmm.CHUNK_SIZE-2:vmm.CHUNK_SIZE+2] == [1,2,3,4]

    assert vmm.unmap_addr(0x100) == (1, 0)
    assert vmm.unmap_addr(0x202) == (2, 2)

    chunks = vmm.chunkify(list(range(vmm.CHUNK_SIZE)))
    assert len(chunks) == 1

    content = list(range(2*vmm.CHUNK_SIZE))
    vmm = VirtualMemory(content)
    assert len(vmm) == 2*vmm.CHUNK_SIZE
    assert vmm[vmm.CHUNK_SIZE] == vmm.CHUNK_SIZE

def main():

    test()

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Advent of Code 2019")
    args = parser.parse_args()

    main(**vars(args))
