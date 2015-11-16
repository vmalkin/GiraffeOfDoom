using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace SerialDataExample
{
    /*
      This class is used to create the array of datapoints for the JSON file. Values are currently stored as strings.
     */
    
    class DataItem
    {
        private string logDate; // the UTC date
        private string h_value; // The magnetometer value
        private double runAvg; // running average at the datapoints position in the array



        // CONSTRUCTOR  
        public DataItem(string logDate, string h_value, double runAvg)
        {
            this.logDate = logDate;
            this.h_value = h_value;
            this.runAvg = runAvg;
        }

        // A datapoint can return it's datetime in unix time. This allows us to calculate it's age in the array it belongs to
        public DateTime UnixAge()
        {
            DateTime dt = new DateTime();
            dt = DateTime.Parse(logDate);
            return dt;
        }


        // Setters and Getters
        public string LogDate
        {
            get { return logDate; }
            set { logDate = value; }
        }
        
        public string H_value
        {
            get { return h_value; }
            set { h_value = value; }
        }

        public double RunAvg
        {
            get { return runAvg; }
            set { runAvg = value; }
        }
    }
}
