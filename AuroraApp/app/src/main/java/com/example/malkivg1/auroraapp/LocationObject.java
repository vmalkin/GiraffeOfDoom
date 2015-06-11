package com.example.malkivg1.auroraapp;

import android.os.Parcel;
import android.os.Parcelable;

/**
 * Created by malkivg1 on 13/05/2015.
 */

/*
* This will be used to populate the spinner and store info for passing out to web interfaces.
* */

 public class LocationObject implements Parcelable{

    private String locName;
    private double locLat; // -ve is south
    private double locLong; // -ve is west
    private String closestStation; // to get the best weather info.
    private String SiteReport; // The closest weather station

    //Normal constructor
    public LocationObject (String locName, double locLat, double locLong, String closestStation)
    {
        this.setLocName(locName);
        this.setLocLat(locLat);
        this.setLocLong(locLong);
        this.setClosestStation(closestStation);
    }

    // Code example for parcelable object from
    // https://github.com/erangaeb/dev-notes/blob/master/android-parcelable/User.java
    public LocationObject (Parcel in)
    {
        this.locName = in.readString();
        this.locLat = in.readDouble();
        this.locLong = in.readDouble();
        this.closestStation = in.readString();
        this.SiteReport = in.readString();
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

    public void setLocLat(double locLat) {
        this.locLat = locLat;
    }

    public double getLocLong() {
        return locLong;
    }

    public void setLocLong(double locLong) {
        this.locLong = locLong;
    }

    public String getClosestStation() {
        return closestStation;
    }

    public void setClosestStation(String closestStation) {
        this.closestStation = closestStation;
    }

    public String getSiteReport() {
        return SiteReport;
    }

    public void setSiteReport(String siteReport) {
        SiteReport = siteReport;
    }

    //These methods are necessary to make this class parcelable
    @Override
    public int describeContents() {
        return 0;
    }

    @Override
    public void writeToParcel(Parcel parcel, int i) {
        parcel.writeString(locName);
        parcel.writeDouble(locLat);
        parcel.writeDouble(locLong);
        parcel.writeString(closestStation);
        parcel.writeString(SiteReport);
    }

    public static final Parcelable.Creator<LocationObject> CREATOR = new Parcelable.Creator<LocationObject>() {

        public LocationObject createFromParcel(Parcel in) {
            return new LocationObject(in);
        }

        @Override
        public LocationObject[] newArray(int i) {
            return new LocationObject[0];
        }

    };
}
