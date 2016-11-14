import time
import datetime
clr.AddReference("System.Drawing")
import System.Drawing

capturedir = "c:\\temp\\"
pausebit = 10
exposetime = 1
defaultcam = 0

sundata = ((0,0),
(5,22),
(5,22),
(5,21),
(5,20),
(5,20),
(6,19),
(6,19),
(6,20),
(6,21),
(5,21),
(5,21),
(5,22))

# Choose the ZWO camera. 
def selectcam():
   pass

def daytime():
   # Daytime
   print("Daytime: " + str(nowhour))
   shutteropen = 0.0001
   return shutteropen
   
   
def nighttime():
   # Nighttime
   print("Night-time " + str(nowhour))
   shutteropen = 30
   return shutteropen
  


# #####################################
# P R O G R A M   S T A R T S   H E R E
# #####################################
SharpCap.SelectedCamera.Controls.OutputFormat.Value = 'PNG files (*.png)'
# Set autoexposure to false
SharpCap.SelectedCamera = SharpCap.Cameras[defaultcam]
SharpCap.SelectedCamera.Controls.Exposure.Automatic = False


while True:
   capturemode = ""
   dt = datetime.datetime.now()
   nowhour = int(dt.strftime('%H'))
   monthnum = int(dt.strftime('%m'))
   sunrise = sundata[int(monthnum)][0]   # Morning twilight starts
   sunset = sundata[int(monthnum)][1]   # Evening twilight ends
   print("\nMonth num: " + str(monthnum) + ". Dawn: " + str(sunrise) + ". Dusk: " + str(sunset))

   if nowhour > sunrise and nowhour < sunset:
      capturemode = "Daytime. Manual exposure"
      exposetime = daytime()
      
   else:
      capturemode = "Night-time. Manual exposure"
      exposetime = nighttime()
   
   # SharpCap.SelectedCamera.Controls.Exposure.ExposureMs = exposetime
   SharpCap.SelectedCamera.Controls.Exposure.Value = exposetime
   print("exposure is " + str(SharpCap.SelectedCamera.Controls.Exposure.Value))

   # Take the snap, save out, append information to image stamp
   SharpCap.SelectedCamera.CaptureSingleFrameTo(capturedir + "capture.png")
   time.sleep(1)
   bm = System.Drawing.Bitmap(capturedir + "capture.png")
   g = System.Drawing.Graphics.FromImage(bm)
   f = System.Drawing.Font("Arial", 14)
   stamp = "http://DunedinAurora.NZ \nSkyCam No 2\n FOV ~70deg, South \n" + capturemode + " " +  str(SharpCap.SelectedCamera.Controls.Exposure.Value) + " seconds\n" + System.DateTime.Now.ToString() + " NZST"
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