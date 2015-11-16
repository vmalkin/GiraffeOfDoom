using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace SerialDataExample
{
    /*
        Utility class to hold logfile functions
     */
    class LogFileManager
    {

        // TO check a filepath exists, if not, create one.
        public void CheckPath(string filePath)
        {
            if (!Directory.Exists(filePath)) // if the log directory does not exist
            {
                Directory.CreateDirectory(filePath);
            }
        }


        // Append data to the logfiles
        public void WriteData(string logDir, string logFile, string logData)
        {
            CheckPath(logDir);

            // If the logfile does not exist (ie we are creating a new logfile, we need 
            // to create a new one and add a header line for charting programs like Google Charts.
            using (FileStream fs = new FileStream(logDir + logFile, FileMode.Append, FileAccess.Write, FileShare.ReadWrite))
            {
                using (StreamWriter sw = new StreamWriter(fs))
                {
                    if (!File.Exists(logDir + logFile))
                    {
                        // Using FileStream seems to prevent the crashing due to external programs accessing the log file while
                        // this program is trying to also write to the log. It also seems to prevent prpoblems when copying the the 
                        // file necessary for Google charts.
                        sw.WriteLine("Date UTC, Time UTC, Reading");

                    }
                    else
                    {
                        sw.WriteLine(GetUTC("timestamp") + "," + logData); // get the timestamp and append the data, write to file. 
                        //sw.Close(); //close the file.
                    }
                }
            }
        }

        // Get the UTC time. This function will return the time formatted in two ways:
        // as YYYY-MM-DD for logfile names
        // as YYYY-MM-DD,HH:MM:SS for logfile data
        public string GetUTC(string returnType)
        {
            string timeUTC = null;

            // Get current time. Use datetime.UTCNow to give us the UTC time 
            DateTime time_dt_UTC = DateTime.UtcNow;

            if (returnType == "timestamp")
            {
                //Convert the datetime object to a string for logging data
                // A decimal second is being used for display only
                // change seconds to ss.fff if we can justify millisecond accuracy
                timeUTC = time_dt_UTC.ToString("yyyy-MM-dd,HH:mm:ss.f");
            }
            else if (returnType == "filename")
            {
                //Convert the datetime object to a string for filenames
                timeUTC = time_dt_UTC.ToString("yyyy-MM-dd");
            }

            return timeUTC;
        }


        // This function will update an internal array for storage, and create
        // a 2 hour and 24 hour JSON file used to update a javascript graph
        // Of course, we're only recording the X value as it represents H...
        public void WriteJSON(List<DataItem> dataPointsList, string logData)
        {
            // IF the array is OLDER than 24hours, remove the oldest value from the array
            // OTHERWISE keep adding to the array.
            if (dataPointsList.Count > 24 * 60 * 4) // 24 hours, by 60 mins, by 4 updates a min
            {
                dataPointsList.RemoveAt(0);
            }

            // set up the dataitem that will be added.
            DataItem dataItemToAdd = new DataItem(GetUTC("timestamp"), logData, Convert.ToDouble(logData));

            //append the newest value to the end of the array (array should be 24 hours long)
            dataPointsList.Add(dataItemToAdd);

            // Perform a running average on the array, and write the appropriate value in each datapoint.
            int sampleInterval = 10;  // MUST be an even number for this to work  

            // When the array is big enough, starting at the right place in the array, compute the new running average...
            if (dataPointsList.Count > sampleInterval)
            {
                for (int i = sampleInterval; i < dataPointsList.Count - 1; i++)
                {
                    double dpAvg = 0; //the running average for the datapoint

                    for (int j = i - sampleInterval; j < i; j++)
                    {
                        dpAvg = dpAvg + Convert.ToDouble(dataPointsList[j].H_value); // Convert the H value to a double and sum
                    }

                    dpAvg = dpAvg / sampleInterval; //the actual average

                    // IN order to position the average marker correctly, it must be at sampleInterval / 2 back from i
                    dataPointsList[i].RunAvg = dpAvg;
                }
            }


            // Now write the new datapoint values to the CurrentUTC file. This will get passed to the web-chart and we should be able to 
            // plot a running average against the raw data.
            string CurrentUTC = "CurrentUTC.csv";

            File.Delete(CurrentUTC);
            using (FileStream ft = new FileStream(CurrentUTC, FileMode.Append, FileAccess.Write, FileShare.ReadWrite))
            {
                using (StreamWriter sw = new StreamWriter(ft))
                {
                    sw.WriteLine("Date UTC," + "Time UTC," + "Reading," + "Running Average (Interval = " + sampleInterval + ")"); // Headings for currentUTC file
                
                    // Write the array to the file
                    for (int i = 0; i < dataPointsList.Count - 1; i++)
                    {
                        sw.WriteLine(dataPointsList[i].LogDate + "," + dataPointsList[i].H_value + "," + dataPointsList[i].RunAvg); // Write the values to the file
                    }
                }
            }
        }
    }
}
