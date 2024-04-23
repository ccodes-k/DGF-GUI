import asyncio
import bitstruct
import struct
from bleak import BleakClient

class HeartRateMonitor:
    def __init__(self, address):
        self.address = address
        self.hr_measurement_uuid = "00002A37-0000-1000-8000-00805F9B34FB"
        self.client = BleakClient(address)
        self.is_monitoring = False

    async def connect(self):
        await self.client.connect()

    async def start_monitoring(self):
        if not await self.client.is_connected():
            await self.connect()

        def handle_hr_notification(sender, data):
            hr_fmt, snsr_detect, snsr_cntct_spprtd, nrg_expnd, rr_int = bitstruct.unpack("b1b1b1b1b1<", data)
            if hr_fmt:
                hr_val, = struct.unpack_from("<H", data, 1)
            else:
                hr_val, = struct.unpack_from("<B", data, 1)
            print(f"HR Value: {hr_val}")
            with open('./assets/ReadFiles/HR.txt', 'W') as f:
                f.write(f"{hr_val}")
                f.flush
            # You can modify this to save HR values to a file or process them as needed

        await self.client.start_notify(self.hr_measurement_uuid, handle_hr_notification)
        self.is_monitoring = True

    async def stop_monitoring(self):
        if self.is_monitoring:
            await self.client.stop_notify(self.hr_measurement_uuid)
            self.is_monitoring = False

    async def disconnect(self):
        if await self.client.is_connected():
            await self.client.disconnect()

    async def run(self):
        try:
            await self.start_monitoring()
            while self.is_monitoring:
                await asyncio.sleep(1)
        except KeyboardInterrupt:
            pass
        finally:
            await self.stop_monitoring()
            await self.disconnect()

# Renamed function for running the heart rate monitor
# async def runHR():
#     address = "a0:9e:1a:c3:53:b9"
#     monitor = HeartRateMonitor(address)
#     await monitor.run()

# # Call the renamed function using asyncio.run() in your script
# asyncio.run(runHR())
