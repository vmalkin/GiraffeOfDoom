package com.example.malkivg1.auroraapp;

import android.content.Intent;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.os.AsyncTask;
import android.os.Bundle;
import android.os.Environment;
import android.support.v7.app.ActionBarActivity;
import android.view.View;
import android.widget.AdapterView;
import android.widget.ArrayAdapter;
import android.widget.ImageView;
import android.widget.Spinner;
import android.widget.Switch;
import android.widget.TextView;
import android.widget.Toast;

import org.json.JSONException;
import org.json.JSONObject;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.MalformedURLException;
import java.net.URL;


public class Weather extends ActionBarActivity {

    TextView txtvSunrise;
    TextView txtvSunset;
    TextView txtvCityName;
    TextView txtvMoonPhase;
    ImageView imgvMoonPhase;
    ImageView imgvWeather;
    Spinner spinMenu;

    JSONObject JSONAstroData; //JSON object for astronomy data
    JSONObject JSONWeatherData; //JSON object for Weather data

    String API_KEY = "f965b02b2c487024";
    String API_CITY = ""; // Needs to be passed in from previous Activity
    String urlAstroString = "";
    String urlWeatherString;
    String AgeOfMoon;

    LocationObject CurrentSite;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_weather);

        // Fetch the intent bundle
        Intent LocaleBundle = getIntent();
        CurrentSite = LocaleBundle.getParcelableExtra("CurrentSite");

        // Set the city to the designated weather station
        API_CITY = CurrentSite.getClosestStation();
        urlAstroString = "http://api.wunderground.com/api/" + API_KEY + "/astronomy/q/NZ/" + API_CITY + ".json";
        urlWeatherString = "http://api.wunderground.com/api/" + API_KEY + "/conditions/q/NZ/" + API_CITY + ".json";

        txtvSunrise = (TextView) findViewById(R.id.txtvSunrise);
        txtvSunset = (TextView) findViewById(R.id.txtvSunset);
        txtvCityName = (TextView) findViewById(R.id.txtvCityName);
        txtvMoonPhase = (TextView) findViewById(R.id.txtvMoonPhase);
        imgvMoonPhase = (ImageView) findViewById(R.id.imgvMoonPhase);
        imgvWeather = (ImageView) findViewById(R.id.imgvWeather);
        spinMenu = (Spinner) findViewById(R.id.spinMenu);

        //Toast.makeText(Weather.this,API_CITY,Toast.LENGTH_LONG).show();

        // get weather data
        asyncGetWeatherData WeatherData = new asyncGetWeatherData(urlWeatherString);
        WeatherData.execute();

        // get astro data
        asyncGetAstroData AstroData = new asyncGetAstroData(urlAstroString);
        AstroData.execute();

        // Set up the menu spinner
        SetupSpinner();

    }

    /*
     * GET IMAGE FROM URL
     * Modified Example from http://stackoverflow.com/questions/18953632/how-to-set-image-from-url-for-imageview
     * */
    // Void 1 - passed into doInBackground
    // Void 2 - sent to OnProgressUpdate
    // Void 3 - returned from DoInBackground and passed  on to onPostExecute
    public class ImageLoadTask extends AsyncTask<String, Void, Bitmap> {

        private String url;
        private ImageView iv;

        public ImageLoadTask(String url, ImageView iv) {
            this.url = url;
            this.iv = iv;
        }


        @Override
        protected Bitmap doInBackground(String... strings) {
            try {
                URL urlConnection = new URL(url);
                HttpURLConnection connection = (HttpURLConnection) urlConnection
                        .openConnection();
                connection.setDoInput(true);
                connection.connect();
                InputStream input = connection.getInputStream();
                Bitmap myBitmap = BitmapFactory.decodeStream(input);
                return myBitmap;
            } catch (Exception e) {
                e.printStackTrace();
            }
            return null;
        }

        @Override
        protected void onPostExecute(Bitmap result) {
            super.onPostExecute(result);
            iv.setImageBitmap(result);
        }
    }

    /*
    * GET ASTRO DATA
    *
    * */
    // Void 1 - passed into doInBackground
    // Void 2 - sent to OnProgressUpdate
    // Void 3 - returned from DoInBackground and passed  on to onPostExecute
    class asyncGetAstroData extends AsyncTask<String, Void, String> {
        private String JSONstring = "";
        private String urlAstroString;

        public asyncGetAstroData(String urlAstroString) {
            this.urlAstroString = urlAstroString;
        }

        // here we do the HTTP connection, get the JSON data, inputstream, etc
        @Override
        protected String doInBackground(String... strings) {

            // create a URL object based on the string
            URL URLObject = null;
            try {
                URLObject = new URL(urlAstroString);
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

                // Set up the streamreader and buffered reader
                InputStreamReader istrRead = new InputStreamReader(istr);
                BufferedReader br = new BufferedReader(istrRead);

                //NOW build up a string from the buffered reader
                String responseString;
                StringBuilder sbld = new StringBuilder();

                try {
                    while ((responseString = br.readLine()) != null) {
                        sbld = sbld.append(responseString);
                    }
                } catch (IOException e) {
                    // TODO Auto-generated catch block
                    e.printStackTrace();
                }

                //NOW create the jsonstring
                JSONstring = sbld.toString();
            }
            return JSONstring;
        }

        // here we findViewByID and set up things
        protected void onPostExecute(String JSONstring) {
            JSONAstroData = SetupJSON(JSONstring);

            // Ok, we're going to make a UDF to process the JSON data.
            ProcessAstroObject(JSONAstroData);
        }
    }

    /*
    * GET WEATHER DATA
    *
    * */
    // Void 1 - passed into doInBackground
    // Void 2 - sent to OnProgressUpdate
    // Void 3 - returned from DoInBackground and passed  on to onPostExecute

    class asyncGetWeatherData extends AsyncTask<String, Void, String> {
        private String JSONstring = "";
        private String urlWeatherString;

        public asyncGetWeatherData(String urlWeatherString) {
            this.urlWeatherString = urlWeatherString;
        }

        // here we do the HTTP connection, get the JSON data, inputstream, etc
        @Override
        protected String doInBackground(String... strings) {

            // create a URL object based on the string
            URL URLObject = null;
            try {
                URLObject = new URL(urlWeatherString);
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
                    while ((responseString = br.readLine()) != null) {
                        sbld = sbld.append(responseString);
                    }
                } catch (IOException e) {
                    // TODO Auto-generated catch block
                    e.printStackTrace();
                }

                //NOW create the jsonstring
                JSONstring = sbld.toString();
            }
            return JSONstring;
        }

        //Process the weather data
        protected void onPostExecute(String JSONstring) {
            JSONWeatherData = SetupJSON(JSONstring);
            //Toast.makeText(Weather.this, JSONWeatherData.toString(), Toast.LENGTH_LONG).show();

            // Ok, we're going to make a UDF to process the JSON data.
            ProcessWeatherObject(JSONWeatherData);
        }
    }


    /*
    * PROCESS THE WEATHER JSONOBJECT
    *
    * */
    public void ProcessWeatherObject(JSONObject WeatherData) {
        JSONObject CurrentObs = null; //get Moon_Phase object
        try {
            CurrentObs = WeatherData.getJSONObject("current_observation");
        } catch (JSONException e) {
            e.printStackTrace();
        }

        String IconURL = null;
        try {
            IconURL = CurrentObs.getString("icon_url");
        } catch (JSONException e) {
            e.printStackTrace();
        }

        // LOad the image icon URL into the ImageView
        ImageLoadTask LoadImg = new ImageLoadTask(IconURL, imgvWeather);
        LoadImg.execute();

        String IconDescription = null;
        try {
            IconDescription = CurrentObs.getString("icon");
        } catch (JSONException e) {
            e.printStackTrace();
        }

        // set the txtvCityName
        String Report = "";
        txtvCityName.setText("Conditions at " + API_CITY + ": " + IconDescription);

        //add data to object report
        Report = "Report for " + CurrentSite.getLocName() + "\nWeather is " + IconDescription + "\n";
        CurrentSite.setSiteReport(Report);
    }


    /*
    * PROCESS THE ASTRONOMY JSONOBJECT
    *
    * */
    public void ProcessAstroObject(JSONObject AstroData) {
        JSONObject MoonData = null; //get Moon_Phase object
        try {
            MoonData = AstroData.getJSONObject("moon_phase");
        } catch (JSONException e) {
            e.printStackTrace();
        }

        String strAgeOfMoon = null;
        try {
            strAgeOfMoon = MoonData.getString("ageOfMoon");
        } catch (JSONException e) {
            e.printStackTrace();
        }

        /*
         * Assign moon phase and grab image from my website
         */
        AgeOfMoon = strAgeOfMoon; //MOON AGE

        // We need to make a correction as the moon age up to 9 is in single digits
        // but the moon-phase filenames have a lead zero.
        switch (AgeOfMoon)
        {
            case "0":
                AgeOfMoon = "00";
                break;

            case "1":
                AgeOfMoon = "01";
                break;

            case "2":
                AgeOfMoon = "02";
                break;

            case "3":
                AgeOfMoon = "03";
                break;

            case "4":
                AgeOfMoon = "04";
                break;

            case "5":
                AgeOfMoon = "05";
                break;

            case "6":
                AgeOfMoon = "06";
                break;

            case "7":
                AgeOfMoon = "07";
                break;

            case "8":
                AgeOfMoon = "08";
                break;

            case "9":
                AgeOfMoon = "09";
                break;

        }

        // load the image from the URL
        String MoonImgURL = "http://www.swordoforion.comli.com/moonAnim/" + AgeOfMoon + ".jpg";
        ImageLoadTask LoadImg = new ImageLoadTask(MoonImgURL, imgvMoonPhase);
        txtvMoonPhase.setText("Moon is " + AgeOfMoon + " days old.");
        LoadImg.execute();

        /*
        * NOW get sunrise data
        *
        * */
        JSONObject SunriseData = null;
        try {
            SunriseData = MoonData.getJSONObject("sunrise");
        } catch (JSONException e) {
            e.printStackTrace();
        }

        String SRHour = null;
        try {
            SRHour = SunriseData.getString("hour");
        } catch (JSONException e) {
            e.printStackTrace();
        }

        String SRMin = null;
        try {
            SRMin = SunriseData.getString("minute");
        } catch (JSONException e) {
            e.printStackTrace();
        }

        /*
        * NOW get sunset data
        *
        * */
        JSONObject SunsetData = null;
        try {
            SunsetData = MoonData.getJSONObject("sunset");
        } catch (JSONException e) {
            e.printStackTrace();
        }

        String SSHour = null;
        try {
            SSHour = SunsetData.getString("hour");
        } catch (JSONException e) {
            e.printStackTrace();
        }

        String SSMin = null;
        try {
            SSMin = SunriseData.getString("minute");
        } catch (JSONException e) {
            e.printStackTrace();
        }

        /*
         * Concatenate into the TextView texts
         *
         * */
        txtvSunrise.setText("Sunrise: " + SRHour + ":" + SRMin);
        txtvSunset.setText("Sunset: "+SSHour + ":" + SSMin);

        //Populate the object's Site report
        String Report = "";
        Report = CurrentSite.getSiteReport();

        //Toast.makeText(Weather.this, Report, Toast.LENGTH_LONG).show();

        Report = Report + "\n" + txtvSunrise.getText() + "\n" + txtvSunset.getText();
        Report = Report + "\nMoon is " + AgeOfMoon + " days old.";

        //Toast.makeText(Weather.this, Report, Toast.LENGTH_LONG).show();

        CurrentSite.setSiteReport(Report);
    }

    /*
    * This code takes in a json file and returns a json object
    * */
    public JSONObject SetupJSON(String jsonString) {
        //NOW create a JSON object and return this.
        JSONObject jsonObject = null;
        try {
            jsonObject = new JSONObject(jsonString);
        } catch (JSONException e) {
            // TODO Auto-generated catch block
            e.printStackTrace();
        }

        return jsonObject;
    }

    /* ######################################################################
    *  MENU SPINNER SETUP STARTS
    * */
    public void SetupSpinner() {
        // create a string array to populate the spinner with Menu items
        String[] MenuList = {"Choose an option...","View aurora conditions", "Choose new location"};

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
                    // GO to Aurora Activity
                    // Create the intent to go to the Aurora page
                    Intent GotoAurora = new Intent(Weather.this, Aurora.class);

                    // This should bundle up the current site to pass along
                    // VAUGHN - be aware of customisation of an object to make it parcelable.
                    GotoAurora.putExtra("CurrentSite", CurrentSite);
                    startActivity(GotoAurora);

                    break;

                case 2:
                    // Go back to choose site
                    Intent GotoStart = new Intent(Weather.this, MainActivity.class);
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
