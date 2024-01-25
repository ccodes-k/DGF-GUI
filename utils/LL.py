# To update LL Label & LL.txt
# LL is lat and long

from utils.server1 import Talker

def update_LT(self, server):
        if server is None:
            Lat = 0
            Long = 0
            LatD = 0
            LongD = 0
        else: 
            Lat = float(server.Lat[0-1]) + ( float(server.Lat[2-8]) / 60)
            Long = float(server.Long[0-2]) + ( float(server.Long[3-9]) / 60)
            LatD = server.LatD
            LongD = server.LongD

            with open('/assets/ReadFiles/lat_long.txt', 'w') as f:
                LL_str = Lat + " " + Long
                f.write(LL_str)
                f.flush
            
            self.LLL.setText("Lat: " + Lat + " " + LatD + " | Long: " + Long + " " + LongD)