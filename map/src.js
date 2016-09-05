var mymap = L.map('map').setView([51.505, -0.09], 10);

L.tileLayer('https://api.mapbox.com/styles/v1/mapbox/streets-v8/tiles/256/{z}/{x}/{y}?access_token={accessToken}', {
    maxZoom: 18,
    accessToken: 'pk.eyJ1IjoiYmVuLXdpbGxpcyIsImEiOiJjaXNsZ3Q2NnowMDZuMnNuNTRkOWx3aG9qIn0.kPrDlJl3RLatF8ip5BPsVg'
}).addTo(mymap);

var markers = new L.FeatureGroup().addTo(mymap);

setInterval(function() {
$.ajax(
    generate_ajax_options()
).done(function(result) {
    markers.clearLayers();
    readings = result.value;
    for (var i = 0; i < readings.length; i++) {
        plot(readings[i])
    }
})
}, 500)

function plot(reading) {
    var marker = L.marker([reading["longitude"], reading["latitude"]])
    .bindPopup(
        "<b>Time: " +
        reading["Timestamp"] +
        "</b><br/>" +
        "Temperature: " +
        reading["temperature"] +
        "<br/>" +
        "Humidity: " +
        reading["humidity"] +
        "<br/>" +
        "Pressure: " +
        reading["pressure"] +
        "<br/>"
    );
     markers.addLayer(marker);
}


function generate_ajax_options() {

    d = new Date();
    d.setSeconds(d.getSeconds() - 30)

    accountName = "wmdata"
    uri = "/wmRecords"
    domain = "table.core.windows.net"

    CanonicalizedResource = "/" + accountName + uri;
    date = d.toUTCString()

    StringToSign = date + "\n" + CanonicalizedResource;
    secretKey = CryptoJS.enc.Base64.parse("cW+cbRXpdJib1LI8ldaU07byO5qSBbd4YAqwxYSEX8vKmQKnCE9HtFaEiZUCQbllTZPBz0M2xa9SNyyYgIImlw==")

    var signature = CryptoJS.enc.Base64.stringify(CryptoJS.HmacSHA256(StringToSign, secretKey));


    return {
        "url": "https://"+accountName+".table.core.windows.net"+uri,
        "method": "GET",
        "headers": {
            'Authorization': 'SharedKeyLite '+accountName+':'+signature,
            'Date': date,
            'x-ms-date': date,
            'x-ms-version': '2015-12-11',
            'Accept': 'application/json;odata=nometadata'
        }
    }
}
