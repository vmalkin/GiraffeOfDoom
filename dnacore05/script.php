<script type="text/javascript">
const speedcolour = "stop4574";
const densitycolour = "density";
const magcolour = "mag";
const ioncolour = "ion";
const bzcolour = "bz";
const dnacolour = "dna";
const bztext = "bztext";
const utcTxtLabel = "text4560"

const clrLow = "#00f000";
const clrMed = "#ff7000";
const clrhigh = "#ff0000";
const clrNone = "#000000";

function changeStroke(elementID, value)
{
    if (value == "low")
    {
        document.getElementById(elementID).style["stroke"] = clrLow;
    }
    if (value == "med")
    {
        document.getElementById(elementID).style["stroke"] = clrMed;
    }
    if (value == "high")
    {
        document.getElementById(elementID).style["stroke"] = clrhigh;
    }
    
    if (value == "none")
    {
        document.getElementById(elementID).style["stroke"] = clrNone;
    }
}

function changeFill(elementID, value)
{
    if (value == "low")
    {
        document.getElementById(elementID).style["fill"] = clrLow;
    }
    if (value == "med")
    {
        document.getElementById(elementID).style["fill"] = clrMed;
    }
    if (value == "high")
    {
        document.getElementById(elementID).style["fill"] = clrhigh;
    }
    if (value == "none")
    {
        document.getElementById(elementID).style["fill"] = clrNone;
    }
}

function changeGradient(elementID, value)
{
    if (value == "low")
    {
        document.getElementById(elementID).style["stop-color"] = clrLow;
    }
    if (value == "med")
    {
        document.getElementById(elementID).style["stop-color"] = clrMed;
    }
    if (value == "high")
    {
        document.getElementById(elementID).style["stop-color"] = clrhigh;
    }
    
    if (value == "none")
    {
        document.getElementById(elementID).style["stop-color"] = clrNone;
    }
}
function windspeed(value)
{
    changeGradient(speedcolour, value);
}
function density(value)
{
    changeStroke(densitycolour, value);
}
function mag(value)
{
    changeStroke(magcolour, value);
}
function ion(value)
{
    changeStroke(ioncolour, value);
}
function dna(value)
{
    changeFill(dnacolour, value);
}

function bzChange(value)
{
    t = "bz: " + value;
    document.getElementById(bztext).innerHTML = t;

    if (value > 0)
    {
        changeFill(bzcolour, "low");
    }
	if (value <=0 && value > -5)
    {
        changeFill(bzcolour, "med");
    }
    if (value <=-5 && value > -10)
    {
        changeFill(bzcolour, "med");
    }
    if (value <= -10)
    {
        changeFill(bzcolour, "high");
    }
}

function utcText(value)
{
    document.getElementById(utcTxtLabel).innerHTML = value;
}

function wrapper(json)
{
    windspeed(json["speed"]);
    density(json["density"]);
    mag(json["mag"]);
    ion(json["ion"]);
    dna(json["dna"]);
    bzChange(json["bz"]);
    utcText(json["utc"]);
}

$.getJSON( "data.json", function( json ) {
  wrapper(json);
 });
 
window.onload = setInterval(() => {
$.getJSON( "data.json", function( json ) {
  wrapper(json);
 });
}, 180000);;

</script>