package com.example.malkivg1.auroraapp;

/**
 * Created by malkivg1 on 13/05/2015.
 */

/*
* This will be used to populate the spinner and store info for passing out to web interfaces.
* */

 public class LocationObject {
    private String locName;
    private double locLat; // -ve is south
    private double locLong; // -ve is west

    public LocationObject (String locName, double locLat, double locLong)
    {
        this.locName = locName;
        this.locLat = locLat;
        this.locLong = locLong;
    }

    public String getLocName() {
        return locName;
    }

    public void setLocName(String locName) {
        this.locName = locName;
    }

    public double getLocLat() {
        return locLat;
    }

    public void setLocLat(float locLat) {
        this.locLat = locLat;
    }

    public double getLocLong() {
        return locLong;
    }

    public void setLocLong(float locLong) {
        this.locLong = locLong;
    }
}
