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
            
            try
            {
                // open log file for append. Will create if not existing.
                using (StreamWriter sw = File.AppendText(logDir + logFile))
                {
                    sw.WriteLine(GetUTC("timestamp") + "," + logData);
                    //sw.Close(); //close the file.
                }
            }
            catch (Exception)
            {  
                throw;
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
            // if not exist JSON files, create them.
            CheckPath("JSON");
            
            // IF the array is OLDER than 24hours, remove the oldest value from the array
            // OTHERWISE keep adding to the array.
            if (dataPointsList.Count > 0)
            {
                int indexLatest = dataPointsList.Count - 1;
                TimeSpan minsDiff= dataPointsList[indexLatest].UnixAge().Subtract(dataPointsList[0].UnixAge());

                string debugresult = Convert.ToString(minsDiff.TotalMinutes);
                

                if (minsDiff.TotalMinutes > 1440)
                {
                    dataPointsList.RemoveAt(0);
                }
            }


            // set up the dataitem that will be added.
            DataItem dataItemToAdd = new DataItem(GetUTC("timestamp"),logData);
            

            //append the newest value to the end of the array (array should be 24 hours long)
            dataPointsList.Add(dataItemToAdd);


                string DailyLog = "24HourLog.csv"; // the log file for the continuous logging
                StreamWriter sw;

                // Create the daily log file if it doesnt exist.
                if (!File.Exists(DailyLog))
                {
                    using (sw = File.CreateText(DailyLog));
                }

                // open log file for append. Will create if not existing.

                foreach (DataItem d in dataPointsList)
                {
                    using (sw = File.AppendText(DailyLog))
                    {
                        sw.WriteLine(d.LogDate + "," + d.H_value);
                        //sw.Close(); //close the file.
                    } 
                }
            
            // create the 2 hour JSON file.

            // create the 24 hour JSON file. 


        }

        /*
            SETTERS AND GETTERS
         */

    }
}
