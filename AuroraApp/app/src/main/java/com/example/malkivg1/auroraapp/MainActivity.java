package com.example.malkivg1.auroraapp;

import android.content.Intent;
import android.support.v7.app.ActionBarActivity;
import android.os.Bundle;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.widget.ArrayAdapter;
import android.widget.Button;
import android.widget.ImageButton;
import android.widget.Spinner;
import android.widget.Toast;

import java.util.ArrayList;

/*
* This activity will populate a spinner with a number of preselected locations.
* */
public class MainActivity extends ActionBarActivity {

    Spinner spinLocations; // spinner of observing locations
    LocationObject[] ObsLocale = new LocationObject[3]; // create array of observing locations
    ImageButton imgbtnGo; // Start button

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        // set up the spinner
        SetupArray();
        SetupSpinner();

        // Setup the Start button and onClick
        imgbtnGo = (ImageButton) findViewById(R.id.imgbtnGo);
        GoClick gc = new GoClick();
        imgbtnGo.setOnClickListener(gc);

    }

    class GoClick implements View.OnClickListener
    {
        // This will bounce us to the next activity, passing on the location that has been selected
        @Override
        public void onClick(View view) {
            // REad the current item position from the spinner.
            int localeIndex = spinLocations.getSelectedItemPosition();

            //create a locationObject for this locale. This will get passed to the next activity.
            LocationObject CurrentSite = ObsLocale[localeIndex];

            // Create the intent to go to the weather page
            Intent GotoWeather = new Intent(MainActivity.this, Weather.class);

            // This should bundle up the current site to pass along
            // VAUGHN - be aware of customisation of an object to make it parcelable.
            GotoWeather.putExtra("CurrentSite", CurrentSite);

            startActivity(GotoWeather);
        }
    }



    public void SetupArray()
    {
        // OK, hardcode in a location to observe from.
        ObsLocale[0] = new LocationObject("Dunedin",-45.8667,170.5000, "Dunedin" );
        ObsLocale[1] = new LocationObject("Papatowai",-46.6000,169.4667, "Balclutha" );
        ObsLocale[2] = new LocationObject("Invercargill",-46.4131,168.3475, "Invercargill" );
    }

    public void SetupSpinner()
    {
        // create a string array to populate the spinner with location names
        String[] localNames = new String[ObsLocale.length];

        for (int i = 0; i < ObsLocale.length; i++)
        {
            localNames[i] = ObsLocale[i].getLocName();
        }

        //Find the spinner.
        spinLocations = (Spinner) findViewById(R.id.spinLocations);
        int LayoutID = android.R.layout.simple_spinner_dropdown_item;

        // setup the array adaptor from the array
        ArrayAdapter<String> loc = new ArrayAdapter<String>(this, LayoutID, localNames);

        // use setAdaptor and associate the array adapter with the spinner
        spinLocations.setAdapter(loc);
    }

}
