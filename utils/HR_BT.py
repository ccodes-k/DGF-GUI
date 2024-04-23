import asyncio
import bitstruct
import struct
from bleak import BleakClient

HR_MEAS = "00002A37-0000-1000-8000-00805F9B34FB"

class HRMonitor:
    def __init__(self, address):
        self.address = address
        self.hr_value = None
        self.loop = asyncio.get_event_loop()
    
    async def connect(self):
        async with BleakClient(self.address) as client:
            connected = await client.is_connected()
            print("Connected: {0}".format(connected))
            
            def hr_val_handler(sender, data):
                """Notification handler for Heart Rate Measurement."""
                (hr_fmt,
                 snsr_detect,
                 snsr_cntct_spprtd,
                 nrg_expnd,
                 rr_int) = bitstruct.unpack("b1b1b1b1b1<", data)
                if hr_fmt:
                    self.hr_value, = struct.unpack_from("<H", data, 1)
                else:
                    self.hr_value, = struct.unpack_from("<B", data, 1)
                
            await client.start_notify(HR_MEAS, hr_val_handler)
            while await client.is_connected():
                await asyncio.sleep(1)
    
    def get_hr_value(self):
        return self.hr_value

async def main(address):
    hr_monitor = HRMonitor(address)
    await hr_monitor.connect()

if __name__ == '__main__':
    address = "a0:9e:1a:c3:53:b9"
    asyncio.run(main(address))