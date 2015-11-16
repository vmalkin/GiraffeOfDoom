using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace SerialDataExample
{
    /*
        Utility class for data processing of the raw coms data.
     */
    class DataProcessManager
    {
        // Takes the serial string and separates into X_Now, Y_Now, Z_Now, and returns the SINGLE value we need
        public string Mag3110_ParseData(string SerialDataToParse)
        {
            // break the string down into a string.split array on commas
            //string[] delimiters = { ",",""};
            //string[] DataArray = SerialDataToParse.Split(delimiters, StringSplitOptions.None);

            // ProcessData for each element. WE ONLY WANT THE X VALUE.
            //string datavalue = DataArray[0]; // grab X from array. Really H
            string datavalue = SerialDataToParse.Trim();
            return datavalue;
        }

        // This particlar function is needed for the MAG3110 sensor, which has a floor/ceiling of 320/-320 and
        // flips the values, but retains the general trend of data. 
        public string Mag3110_Process_Data(string DataElement)
        {
            // assign to x_Old values
            return DataElement;
        }

        // This function identifies Sudden Commencement-type curves in the data
        // We are lookig for a curve that changes x-amount in 5 mins, with no reverse fluctuations
        public void SuddenCommencement(List<DataItem> dataPointsList)
        { 
            int scThreshold = 20;
            int scInterval = 5 * 4; // 5 mins x 4 readings per minute

        }


    }
}
