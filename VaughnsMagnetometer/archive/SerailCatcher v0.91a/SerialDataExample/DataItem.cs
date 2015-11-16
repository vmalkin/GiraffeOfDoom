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
        private string x_value; // The magnetometer value
        private string y_value; // The magnetometer value
        private string z_value; // The magnetometer value
        private double runAvg; // running average at the datapoints position in the array



        // CONSTRUCTOR  
        public DataItem(string logDate, string x_value, string y_value, string z_value, double runAvg)
        {
            this.logDate = logDate;
            this.x_value = x_value;
            this.y_value = y_value;
            this.z_value = z_value;
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
        public string X_value
        {
            get { return x_value; }
            set { x_value = value; }
        }

        public string Y_value
        {
            get { return y_value; }
            set { y_value = value; }
        }
        public string Z_value
        {
            get { return z_value; }
            set { z_value = value; }
        }
    }
}
