import hid

class Connection:
    """ Simple wrapper for hidapi.
    Intended to read and write OUT/IN reports easily.
    """
    def __init__(self):
        self.connection = None
        self.info = None
    def connect(self, pid, vid):
        devs = hid.enumerate()
        for d in devs:
            if d['product_id'] == int(pid) and d['vendor_id'] == int(vid):
                self.info = d
                self.connection = hid.device()
                self.connection.open_path(self.info['path'])
        if self.connection is None: raise AssertionError("Could not find a matching device.")
        else: print(f"Successfully conntected to {self.info['product_string']}.")
    def close(self):
        if self.connection is None: return
        self.connection.close()
        print(f"Closed {self.info['product_string']}.")
    def write_out(self, m):
        # TODO: do some sanity checks
        self.connection.write(m)
    def read_in(self, cmd, num_bytes):
        data = self.connection.read(4 + num_bytes)
        if data[0] == 85 and data[1] == 85 and data[2] == num_bytes and data[3] == cmd:
            return data[4:]
        else: return None