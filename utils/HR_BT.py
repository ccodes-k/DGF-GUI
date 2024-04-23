import asyncio
import bitstruct
import struct
from bleak import BleakClient

class HeartRateMonitor:
    def __init__(self, address, output_file="./assets/ReadFiles/HR.txt"):
        self.address = address
        self.output_file = output_file
        self.running = False
        self.client = None

    async def connect(self):
        async with BleakClient(self.address) as client:
            self.client = client
            connected = await client.is_connected()
            print(f"Connected: {connected}")

            await client.start_notify("00002A37-0000-1000-8000-00805F9B34FB", self.handle_notification)

            self.running = True
            while self.running and await client.is_connected():
                await asyncio.sleep(1)

    async def handle_notification(self, sender, data):
        """Handle heart rate notifications."""
        (hr_fmt,
         snsr_detect,
         snsr_cntct_spprtd,
         nrg_expnd,
         rr_int) = bitstruct.unpack("b1b1b1b1b1<", data)

        if hr_fmt:
            hr_val, = struct.unpack_from("<H", data, 1)
        else:
            hr_val, = struct.unpack_from("<B", data, 1)

        print(f"Received HR Value: {hr_val}")

        # Write heart rate value to the specified text file
        with open(self.output_file, 'w') as file:
            file.write(f"{hr_val}")
            file.flush

    async def start_monitoring(self):
        try:
            await self.connect()
        except Exception as e:
            print(f"Error: {e}")
        finally:
            if self.client:
                await self.client.disconnect()

    def stop_monitoring(self):
        self.running = False
