import time
import datetime
clr.AddReference("System.Drawing")
import System.Drawing

capturedir = "c:\\temp\\"

sundata = ((0,0,0,0),
(4,5,21,22),
(4,5,21,22),
(5,6,21,22),
(5,6,21,22),
(5,6,21,22),
(5,6,20,21),
(5,6,20,21),
(6,7,20,21),
(6,7,20,21),
(6,7,20,21),
(6,7,20,21),
(6,7,19,20),
(6,7,19,20),
(6,7,19,20),
(6,7,18,19),
(6,7,18,19),
(6,7,17,18),
(6,7,17,18),
(6,7,17,18),
(6,7,17,18),
(6,7,17,18),
(7,8,17,18),
(7,8,17,18),
(7,8,17,18),
(7,8,16,17),
(7,8,16,17),
(7,8,17,18),
(7,8,17,18),
(7,8,17,18),
(7,8,17,18),
(7,8,17,18),
(7,8,17,18),
(7,8,17,18),
(7,8,17,18),
(6,7,17,18),
(6,7,18,19),
(6,7,18,19),
(6,7,18,19),
(5,6,18,19),
(5,6,19,20),
(5,6,19,20),
(5,6,20,21),
(5,6,20,21),
(5,6,20,21),
(5,6,20,21),
(5,6,20,21),
(5,6,20,21),
(4,5,21,22),
(4,5,21,22),
(4,5,21,22),
(4,5,21,22),
(4,5,21,22))

# Choose the ZWO camera. 
def selectcam():
   pass

SharpCap.SelectedCamera.Controls.OutputFormat.Value = 'PNG files (*.png)'

while True:
   dt = datetime.datetime.now()
   nowhour = (dt.strftime('%H'))
   weeknum = (dt.strftime('%W'))

   tlr = sundata[int(weeknum)][0]   # Morning twilight starts
   r = sundata[int(weeknum)][1]
   s = sundata[int(weeknum)][2]
   tls = sundata[int(weeknum)][3]   # Evening twilight ends

   if nowhour <= tlr or nowhour >= tls:
      # Nighttime
      # load dark frame profile

   else:
      # Daytime
      print("Daytime: " + str(nowhour))
      SharpCap.SelectedCamera.Controls.Exposure.Automatic = True

   SharpCap.SelectedCamera.CaptureSingleFrameTo(capturedir + "capture.png")
   time.sleep(1)
   bm = System.Drawing.Bitmap(capturedir + "capture.png")
   g = System.Drawing.Graphics.FromImage(bm)
   f = System.Drawing.Font("Arial", 14)
   stamp = "http://DunedinAurora.NZ \nSkyCam No 2\n" + System.DateTime.Now.ToString() + " NZST"
   g.DrawString(stamp, f, System.Drawing.Brushes.Red, System.Drawing.Point(0,0))
   g.Dispose()
   f.Dispose()
    
   try:
      bm.Save(capturedir + "timestamped.png")
   except:
      print("Unable to save image")
   
   bm.Dispose()
# do more with png file here
   print("IMage captured at " + System.DateTime.Now.ToString())
   time.sleep(180)