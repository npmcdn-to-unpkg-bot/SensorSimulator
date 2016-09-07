config = {
    "source": "azure", // "azure" or "csv"
    "live": true,
    "update_time": 1 // Seconds
}

function get_data(cb) {
    if (config["source"] == "azure") {
        $.ajax(
            generate_ajax_options()
        ).done(function(result) {
            cb(result.value);

        })
    } else if (config["source"] == "csv") {
        Papa.parse("fake_data2.csv", {
        	download: true,
            header: true,
        	complete: function(results) {
        		cb(results.data)
        	}
        });
    }
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
