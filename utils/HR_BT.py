# HR_BT.py

import asyncio
import bitstruct
import struct
from bleak import BleakClient
from PyQt5.QtCore import pyqtSignal, QObject

HR_MEAS = "00002A37-0000-1000-8000-00805F9B34FB"

class HeartRateMonitor(QObject):
    hr_updated = pyqtSignal(int)  # Signal emitted when heart rate value is updated

    async def run_HR(self, address, debug=False):
        async with BleakClient(address) as client:
            connected = client.is_connected  
            print("Connected: {0}".format(connected))

            async def hr_val_handler(sender, data):
                """Notification handler for Heart Rate Measurement."""
                (hr_fmt,
                 snsr_detect,
                 snsr_cntct_spprtd,
                 nrg_expnd,
                 rr_int) = bitstruct.unpack("b1b1b1b1b1<", data)
                
                if hr_fmt:
                    hr_val, = struct.unpack_from("<H", data, 1)
                else:
                    hr_val, = struct.unpack_from("<B", data, 1)
                
                print(f"HR Value: {hr_val}")
                self.hr_updated.emit(hr_val)  # Emit signal with updated heart rate value
            
            await client.start_notify(HR_MEAS, hr_val_handler)

            while client.is_connected:  
                await asyncio.sleep(1)
