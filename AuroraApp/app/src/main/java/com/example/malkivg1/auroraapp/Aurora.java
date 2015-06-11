package com.example.malkivg1.auroraapp;

import android.content.Intent;
import android.graphics.Color;
import android.os.AsyncTask;
import android.os.Bundle;
import android.support.v7.app.ActionBarActivity;
import android.view.View;
import android.widget.AdapterView;
import android.widget.ArrayAdapter;
import android.widget.Spinner;
import android.widget.TextView;

import com.jjoe64.graphview.GraphView;
import com.jjoe64.graphview.series.DataPoint;
import com.jjoe64.graphview.series.LineGraphSeries;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.MalformedURLException;
import java.net.URL;
import java.util.ArrayList;
import static java.lang.Math.sqrt;


public class Aurora extends ActionBarActivity {

    Spinner spinMenu;
    // ArrayList<Integer> ChartValues = new ArrayList<Integer>();
    double[] ChartValues;
    public String CSVString;
    TextView txtvLocalInfo;

    LocationObject CurrentSite;



    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_aurora);

        // Fetch the intent bundle
        Intent LocaleBundle = getIntent();
        CurrentSite = LocaleBundle.getParcelableExtra("CurrentSite");

        // Find the screen widgets
        spinMenu = (Spinner) findViewById(R.id.spinMenu);
        txtvLocalInfo = (TextView) findViewById(R.id.txtvLocalInfo);

        // String to get (soon to be) live aurora data
        String urlAuroraCSV = "http://homepages.vodafone.co.nz/~Svmalkin/log.txt";

        // Pass URL to asyncget and retrieve magnetometer data
        asyncGetAstroData AuroraData = new asyncGetAstroData(urlAuroraCSV);
        AuroraData.execute();

        SetupSpinner();

    }

    // Void 1 - passed into doInBackground
    // Void 2 - sent to OnProgressUpdate
    // Void 3 - returned from DoInBackground and passed  on to onPostExecute
    class asyncGetAstroData extends AsyncTask<String, Void, ArrayList<String>> {

        private String urlAuroraCSV;
        ArrayList<String> stringTempValues = new ArrayList<>();

        public asyncGetAstroData(String urlAuroraCSV) {
            this.urlAuroraCSV = urlAuroraCSV;
        }

        // here we do the HTTP connection, get the JSON data, inputstream, etc
        @Override
        protected ArrayList<String> doInBackground(String... strings) {

            // create a URL object based on the string
            URL URLObject = null;
            try {
                URLObject = new URL(urlAuroraCSV);
            } catch (MalformedURLException e) {
                // TODO Auto-generated catch block
                e.printStackTrace();
            }

            // create a HttpURLConnection
            HttpURLConnection connection = null;
            try {
                connection = (HttpURLConnection) URLObject.openConnection();
            } catch (IOException e) {
                // TODO Auto-generated catch block
                e.printStackTrace();
            }

            //Connect to the URL
            try {
                connection.connect();
            } catch (IOException e) {
                // TODO Auto-generated catch block
                e.printStackTrace();
            }

            //We have to catch dud connections ie: http errors like 404 etc.
            int httpStatusCode = 0;
            try {
                httpStatusCode = connection.getResponseCode();
            } catch (IOException e) {
                // TODO Auto-generated catch block
                e.printStackTrace();
            }

            if (httpStatusCode <= 400) //success
            {
                // get the stream from the HTML connection usig a buffered reader.


                InputStream istr = null;
                try {
                    istr = connection.getInputStream();
                } catch (IOException e) {
                    // TODO Auto-generated catch block
                    e.printStackTrace();
                }

                InputStreamReader istrRead = new InputStreamReader(istr);
                BufferedReader br = new BufferedReader(istrRead);

                //NOW build up a string from the buffered reader
                String responseString;
                StringBuilder sbld = new StringBuilder();

                try {
                    while((responseString = br.readLine()) != null)
                    {
                        //sbld = sbld.append(responseString);
                        stringTempValues.add(responseString); // append to tempValues list
                    }
                } catch (IOException e) {
                    // TODO Auto-generated catch block
                    e.printStackTrace();
                }
            }

            return stringTempValues;
        }

        protected void onPostExecute(ArrayList<String> stringTempValues)
        {
            // stringTempValues is the raw string data. What we want to work with is a running average.
            // This will take some of the noise out.

            //Parse string array to get integer values Put into Integer array
            int[] TempValues = new int[stringTempValues.size()]; // Holder for averaged data

            for (int i = 0; i < TempValues.length; i++)
            {
                String line = stringTempValues.get(i);
                String[] ReadData = line.split(",");
                // The string correct value is parsed as an int and added to the tempValues
                TempValues[i] = Integer.parseInt(ReadData[1]);
            }

            // NOW we have an array of integers. Using this, we will generate a new array of running averages to
            // reduce the noisiness of the data.

            ArrayList<Float> RunningAvg = new ArrayList<Float>();

            int runAvg_length = 20; // this value will depend on the same size. Lets say we're going for averaging over 5 mins @ 4x/sec ~= 20
            int CurrentIndex = 0;

            while(CurrentIndex < TempValues.length - runAvg_length)
            {
                float RAvgMean = 0;
                // Starting at CurrentIndex, Total up TempValues[x] to TempValues[x + runAvg_length]
                for (int i = CurrentIndex; i < CurrentIndex + runAvg_length; i++)
                {
                    RAvgMean = RAvgMean + TempValues[i];
                }

                // Find the MEAN
                RAvgMean = RAvgMean / runAvg_length;

                //Write the mean to RunningAvg[x] (If in the future I want a timestamp, the use the time of TempValues[x + runAvg_length]
                RunningAvg.add(RAvgMean);

                // Increment X.
                CurrentIndex++;
                // Repeat until we have come to the end of TempValues.
            }

            // We now have our final list of values. Write to the Chart Values Array
            ChartValues = new double[RunningAvg.size()];

            for(int i = 0; i < RunningAvg.size(); i++)
            {
                ChartValues[i] = RunningAvg.get(i);
            }


            // We want ChartValues to be the final smoothed data
            DrawGraph();
        }
    }

    public void DrawGraph()
    {
        // Create a GraphView
        GraphView graph = (GraphView) findViewById(R.id.grphAuroraPlot);
        //Toast.makeText(Aurora.this,ChartValues.length,Toast.LENGTH_LONG).show();
        // Array of datapoints to be passed into the chart series
        DataPoint[] Readings = new DataPoint[ChartValues.length];

        // loop thru and populate the series
        for (int i = 0; i < ChartValues.length; i++ )
        {
            //Readings[i] = new DataPoint(i, ChartValues.get(i));
            Readings[i] = new DataPoint(i, ChartValues[i]);
        }

        // Create the series
        LineGraphSeries<DataPoint> series = new LineGraphSeries<DataPoint>(Readings);

        // Jazz up the formatting and then draw the graph
        graph.setBackgroundColor(Color.DKGRAY);
        graph.setTitle("Recent Auroral Activity - 2 hours");
        graph.setTitleColor(Color.WHITE);
        graph.getGridLabelRenderer().setGridColor(Color.WHITE); // Hmmmmmm!
        graph.getGridLabelRenderer().setHorizontalLabelsVisible(false);
        graph.getGridLabelRenderer().setVerticalLabelsVisible(false);

        graph.getViewport().setXAxisBoundsManual(true);
        //graph.getViewport().setMinX((ChartValues.length - 400));
        graph.getViewport().setMinX(1);
        graph.getViewport().setMaxX(ChartValues.length);

        series.setThickness(4);
        series.setColor(Color.GREEN);

        graph.addSeries(series);

        // Perform analysis of the data
        ChartAnalysis();
    }

    // Return a value to indicate how disturbed is the geomagnetic field.
    // We will be doing this naively, by looking for arbitrarily large jumps in
    // data. The more of these per unit of time, the more active the geomagnetic
    // field where the magnetometer is located.
    public void ChartAnalysis()
    {
        String AuroraReport = "\n\nBest times to view the aurora are at least an hour after sunset and before dawn. Aurora are best seen when the moon is up to 7 days old and after 21 days";
        String Report = CurrentSite.getSiteReport();
        String GraphActivity = null;
        //ANALYSIS
        // We are going for a simplistic analysis of the array. We will make a note of the square of
        // the differences between readings. This should exagerate larger changes. We want to count how
        // often this large change occurs over time, which will give us a indication (of sorts!)
        // It also simplifies the issue of values being positive or negative.

        final int AURORA_ACTIVITY = 2; // How much the x-axis can wiggle by
        final int MINOR_THRESHOLD = 4; // Min num of wiggles per hour
        final int MAX_THRESHOLD = 8; // Max wiggles
        int AuroraHourlyCount = 0; // count of current wiggles

        for (int i = 1; i < ChartValues.length; i++)
        {
            double j = ChartValues[i] - ChartValues[i-1];
            int j_test = (int)sqrt(j * j); // just remove the sign by squaring and see if the value is over the threshold.
            if (j_test > AURORA_ACTIVITY)
            {
                AuroraHourlyCount++;
            }
        }

        if (AuroraHourlyCount <  MINOR_THRESHOLD)
        {
            GraphActivity = "\n\nThere is minimal activity. Aurora unlikely tonight";
        }
        else if(AuroraHourlyCount > MINOR_THRESHOLD && AuroraHourlyCount < MAX_THRESHOLD)
        {
            GraphActivity = "\n\nThere is some activity. Aurora possible tonight";
        }
        else if(AuroraHourlyCount > MAX_THRESHOLD)
        {
            GraphActivity = "\n\nChance of an aurora high tonight.";
        }



        // REPORTING

        Report = Report + AuroraReport + GraphActivity;

        CurrentSite.setSiteReport(Report);
        txtvLocalInfo.setText(CurrentSite.getSiteReport());  //Set the report.

    }

    /* ######################################################################
    *  MENU SPINNER SETUP STARTS
    * */
    public void SetupSpinner() {
        // create a string array to populate the spinner with Menu items
        String[] MenuList = {"Choose an option...","Choose new location"};

        //Find the spinner.
        spinMenu = (Spinner) findViewById(R.id.spinMenu);
        int LayoutID = android.R.layout.simple_spinner_dropdown_item;

        // setup the array adaptor from the array
        ArrayAdapter<String> MenuItems = new ArrayAdapter<String>(this, LayoutID, MenuList);

        // use setAdaptor and associate the array adapter with the spinner
        spinMenu.setAdapter(MenuItems);

        SpinnerSelect sp = new SpinnerSelect();
        spinMenu.setOnItemSelectedListener(sp);
    }

    //http://developer.android.com/guide/topics/ui/controls/spinner.html
    public class SpinnerSelect implements AdapterView.OnItemSelectedListener
    {
        @Override
        public void onItemSelected(AdapterView<?> parent, View view, int position, long id) {

            switch(position)
            {
                case 0:
                    break;

                case 1:
                    // Go back to choose site
                    Intent GotoStart = new Intent(Aurora.this, MainActivity.class);
                    startActivity(GotoStart);
                    break;
            }

        }

        @Override
        public void onNothingSelected(AdapterView<?> parent) {

        }
    }

    /*
    *  MENU SPINNER SETUP ENDS
    *  ######################################################################
    * */


}