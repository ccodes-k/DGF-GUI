HR_MEAS = "00002A37-0000-1000-8000-00805F9B34FB"
global_values = {
    'hr_val': 0
}

        # Heart Rate - wave
        self.W2 = pg.PlotWidget(self.F2)
        self.x2 = list(range(100))  # 100 time points
        self.y2 = [randint(50,50) for _ in range(100)]  # 100 data points
        self.W2.setBackground('default')
        pen2 = pg.mkPen(color=(255, 0, 0))
        self.data_line2 =  self.W2.plot(self.x2, self.y2, pen=pen2)
        #self.W1.getPlotItem().hideAxis('left')
        self.W2.getPlotItem().hideAxis('bottom')

        # Heart Rate - wave
        self.x2 = self.x2[1:]  # Remove the first y element.
        self.x2.append(self.x2[-1] + 1)  # Add a new value 1 higher than the last.
        #with open('ReadFiles/HeartReat.txt') as r1:
        #    v1 = r1.read()
        global global_values
        v2 = str(global_values['hr_val'])
        self.y2 = self.y2[1:]  # Remove the first
        self.y2.append(int(v2))  # Add a new value.
        self.data_line2.setData(self.x2, self.y2)  # Update the data.
        self.W2.setYRange(self.y2[-1]+10, self.y2[-1]-10, padding=0)

        # Heart Rate - wave
        global global_values
        #with open('ReadFiles/HeartReat.txt') as self.r1:
        #    self.v1 = self.r1.read()
        self.v2 = str(global_values['hr_val'])
        self.N2.setText("Heart Rate: " + self.v2 + " BPM")

#Heart Rate sensor
async def hr_sensor(address, debug=False):
    async with BleakClient(address) as client:
        connected = client.is_connected  
        print("Connected: {0}".format(connected))

        def hr_val_handler(sender, data):
            global global_values

            """Simple notification handler for Heart Rate Measurement."""
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
            global_values['hr_val'] = hr_val

        await client.start_notify(HR_MEAS, hr_val_handler)

        while client.is_connected:  
            await asyncio.sleep(1)

def run_heart_rate_monitor(address, debug=False):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(hr_sensor(address))

# Start the heart rate monitoring in a separate thread
    # heart_rate_thread = threading.Thread(target=run_heart_rate_monitor, args=(address,))
    # heart_rate_thread.start()