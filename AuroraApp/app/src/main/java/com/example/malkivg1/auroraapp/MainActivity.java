package com.example.malkivg1.auroraapp;

import android.support.v7.app.ActionBarActivity;
import android.os.Bundle;
import android.view.Menu;
import android.view.MenuItem;
import android.widget.Spinner;

/*
* This activity will populate a spinner with a number of preselected locations.
* */
public class MainActivity extends ActionBarActivity {

    Spinner spinLocations;
    LocationObject[] ObsLocale; // create array of observing locations

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        // OK, hardcode in a location to observe from.
        ObsLocale[0] = new LocationObject("Dunedin",-45.8667,170.5000 );
        ObsLocale[1] = new LocationObject("Papatowai",-46.6000,169.4667 );
        ObsLocale[2] = new LocationObject("Invercargill",-46.4131,168.3475 );


    }



}
