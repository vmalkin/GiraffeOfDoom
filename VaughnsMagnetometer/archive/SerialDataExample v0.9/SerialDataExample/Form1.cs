// http://www.codeproject.com/Articles/75770/Basic-serial-port-listening-application
// http://csharp.simpleserial.com/

using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.IO;
using System.IO.Ports;
using System.Linq;
using System.Text;
using System.Threading;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace SerialDataExample
{
    public partial class Form1 : Form
    {
        string versionNum = "0.85";
        string RxString; // X, Y, and Z mag data in CSV format
        int RxStringLength = 1; //expected min RxString length 
        string ComPortID = "Com7";
        //int magWriteFreq = 4; // How often the magnetometer updates per minute
        string rawLogsDir = @"RawData\";
        //string processedDataDir = @"Logs\";
        List<DataItem> dataPoints = new List<DataItem>();
        
        //Utility classes needed
        LogFileManager lf = new LogFileManager(); // logfile manager 
        DataProcessManager dp = new DataProcessManager(); // Data processing manager


        public Form1()
        {
            InitializeComponent();
            this.Text = "Welcome to Serial Catcher version " + versionNum;
        }


        private void Form1_Load(object sender, EventArgs e)
        {
            InitApp();
            LoadArrayLog();
        }

        private void LoadArrayLog()
        {
            string logFile = rawLogsDir + "RAW-" + lf.GetUTC("filename") + ".csv";
            
            if(File.Exists(logFile))
            {
                StreamReader reader = new StreamReader(File.OpenRead(logFile));
                DataItem di;
                string[] delimiters = { "," };

                while (!reader.EndOfStream)
                {                  
                    string line = reader.ReadLine();
                    //MessageBox.Show(line);

                    string[] values = line.Split(delimiters, StringSplitOptions.None);

                    if (values[0] != "Date UTC")
                    {
                        di = new DataItem(values[0] + "," + values[1], values[2], Convert.ToDouble(values[2]));
                        dataPoints.Add(di);  
                    }

                }
                reader.Close();
            }
            UserFeedback("Array loaded. " + dataPoints.Count + " items in size.");
            
        }

        private void InitApp()
        {
            var ports = SerialPort.GetPortNames();
            ComPortDropdown.DataSource = ports;
        }

        // Connect to the com port
        private void ComConnect_Click(object sender, EventArgs e) 
        {
            // WE NEED TO HANDLE EXCEPTIONS HERE
            if (!serialPort1.IsOpen)
            { 
                serialPort1.PortName = ComPortID; // a lot of this should be moved
                serialPort1.BaudRate = 9600;

                serialPort1.Open();
                UserFeedback("Opening com port: " + ComPortID + ". Waiting for data...");
            }

            else
            {
                UserFeedback("Com port is already open");
            }

            ComConnect.Enabled = false;
            ComDisconnect.Enabled = true;
        }

        // Dicsonnect from the com port
        private void ComDisconnect_Click(object sender, EventArgs e)
        {
            if (serialPort1.IsOpen == true)
            {
                serialPort1.Close();
                UserFeedback("Com port is closed");
            }

            ComConnect.Enabled = true;
            ComDisconnect.Enabled = false;
        }


        // THIS FUNCTION NEEDS TO WRITE TO LOGFILE
        private void LogData(object sender, EventArgs e)
        {
            string rawLogFile = "RAW-" + lf.GetUTC("filename") + ".csv";
            //string processedLogFile = "PROCESSED-" + lf.GetUTC("filename") + ".csv";

            // Test for correct string length from Mag
            if (RxString.Length < RxStringLength)
            {
                UserFeedback("ERROR: Magnetometer datastring too small");
            }
            else 
            {
                // Data to RAW logfiles
                string h_valueRaw = dp.Mag3110_ParseData(RxString); // Get the RXString, parse this to get H value.
                lf.WriteData(rawLogsDir, rawLogFile, h_valueRaw); // write the RAW data to logfile.

                // Data to PROCESSED logfiles
                string h_valueProcessed = dp.Mag3110_Process_Data(h_valueRaw); //process the data
                //lf.WriteData(processedDataDir, processedLogFile, h_valueProcessed); // write the PROCESSED data to logfile.

                // create the JSON files for graph display.
                lf.WriteJSON(dataPoints, h_valueProcessed); 

                // Update userfeedback with current value.
                string userResponse = "Data recieved: \n" + lf.GetUTC("timestamp") + "\n" + h_valueProcessed;
                string latestDataPoint = "\n\nDatapoint[" + dataPoints.Count + "]" + dataPoints[dataPoints.Count - 1].H_value + " " + dataPoints[dataPoints.Count - 1].RunAvg;
                userResponse = userResponse + latestDataPoint;
                UserFeedback(userResponse); 

            }
  
        }

        
        // THIS FUNCTION IS FOR WHEN DATA IS RECIEVED
        private void serialPort1_DataReceived(object sender, SerialDataReceivedEventArgs e)
        {
            RxString = serialPort1.ReadLine(); // this is better - reads to NL/CR
            //RxString = serialPort1.ReadExisting();
            this.Invoke(new EventHandler(LogData));
        }

        private void UserFeedback(string message)
        {
            lblStatus.Text = message;
        }

        private void ComPortDropdown_SelectedIndexChanged(object sender, EventArgs e)
        {
            ComPortID = ComPortDropdown.SelectedItem.ToString();
            UserFeedback("Com port set to " + ComPortID);
        }

        private void configureComPortToolStripMenuItem_Click(object sender, EventArgs e)
        {
            
        }
    }
}
