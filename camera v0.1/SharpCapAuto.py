import time
import datetime
clr.AddReference("System.Drawing")
import System.Drawing

capturedir = "c:\\temp\\"

# Choose the ZWO camera. 
def selectcam():
   pass

SharpCap.SelectedCamera.Controls.OutputFormat.Value = 'PNG files (*.png)'
if (SharpCap.SelectedCamera.Controls.Exposure.AutoAvailable):
   SharpCap.SelectedCamera.Controls.Exposure.Automatic = True
   
SharpCap.SelectedCamera.Controls.Exposure.Value = 15000   # Set the exposure to 1000ms (1s)

while True:
   SharpCap.SelectedCamera.CaptureSingleFrameTo(capturedir + "capture.png")
   time.sleep(1)
   bm = System.Drawing.Bitmap(capturedir + "capture.png")
   g = System.Drawing.Graphics.FromImage(bm)
   f = System.Drawing.Font("Arial", 14)
   stamp = "http://DunedinAurora.NZ \nSkyCam No 2\n" + System.DateTime.Now.ToString() + " NZDST" + "\nFOV ~70deg, South."
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
