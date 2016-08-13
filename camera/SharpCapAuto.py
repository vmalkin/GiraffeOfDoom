import time
import datetime
clr.AddReference("System.Drawing")
import System.Drawing

capturedir = "c:\\temp\\"

# Choose the ZWO camera. 
def selectcam():
   pass


def createtimestamp(flag):
   dt = datetime.datetime.utcnow()
   thing = ""
   if flag == "dir":
      thing = str(dt.date())
   elif flag == "file":
      thing = str(dt.hour) + str(dt.minute) + str(dt.second)
   return thing

SharpCap.SelectedCamera.Controls.OutputFormat.Value = 'PNG files (*.png)'
if (SharpCap.SelectedCamera.Controls.Exposure.AutoAvailable):
   SharpCap.SelectedCamera.Controls.Exposure.Automatic = True

while True:
   SharpCap.SelectedCamera.CaptureSingleFrameTo(capturedir + "capture.png")
   time.sleep(1)
   bm = System.Drawing.Bitmap(capturedir + "capture.png")
   g = System.Drawing.Graphics.FromImage(bm)
   f = System.Drawing.Font("Arial", 14)
   stamp = "http://DunedinAurora.NZ \nSkyCam No 2\n" + System.DateTime.Now.ToString() + " NZST"
   g.DrawString(stamp, f, System.Drawing.Brushes.Yellow, System.Drawing.Point(0,0))
   g.Dispose()
   f.Dispose()
   
   a = createtimestamp("dir")
   b = createtimestamp("file")
   c = a + " " + b + ".png"
   print(c)
   
   try:
      bm.Save(capturedir + c)
      bm.Save(capturedir + "timestamped.png")
   except:
      print("Unable to save image")
   
   bm.Dispose()
# do more with png file here
   time.sleep(120)