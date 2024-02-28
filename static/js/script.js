$(document).ready(function() {

    // Capture Convert Event 
    $('#convert-button').click(function() {
        const file = $('#csv-file')[0].files[0];
        $('#csv-file').val('');
        if (file) {
            const reader = new FileReader();
            reader.onload = function(e) {
                const csvContent = e.target.result;
                const convertedData = convertCSVtoJson(csvContent);
                saveDataToLocalStorage('convertedData', convertedData);
                displayJson(convertedData);
                $('#download-button').show();
            };
            reader.readAsText(file);
        } else {
            alert('Please select a CSV file.');
        }
    });

    // Download Json File
    $('#download-button').click(function() {
        const convertedData = getDataFromLocalStorage('convertedData');
        if (convertedData) {
            const formattedJsonContent = JSON.stringify(convertedData, null, 4);
            const blob = new Blob([formattedJsonContent], { type: 'application/json' });
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = 'output.json';
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            URL.revokeObjectURL(url);
        } else {
            alert('No Data found!');
        }
    });

});

// Convert CSV to JSON
function convertCSVtoJson(csvContent) {
    console.log(typeof(csvContent))
    console.log(csvContent)
    // Initialize the output object
    let output = { "parts": {} };
    let currentKey = null;

    // Read the CSV file
    let fileContent = csvContent.split('\n');
    fileContentFilter = fileContent.slice(2);
    // Iterate over each row in the CSV
    fileContentFilter.forEach((line) => {
        let row = line.split(',');

        // Check if the first column is not empty and not "Guideline"
        if (row.includes('Area')) {
            output['Area'] = row[row.indexOf('Area') + 1];
        }
        if (row.includes('Dims')) {
            output['Dims'] = row[row.indexOf('Dims') + 1].replace(/\\/g, '').replace(/"/g, '');
        }

        if (row[0] !== '' && row[0] !== "Guideline") {
            // Update the current key
            currentKey = row[0];
            // Create a new entry in the output dictionary
            output['parts'][currentKey] = { "Guideline": "", "Standards": [] };
        } else {
            // Check if there is a current key
            if (currentKey) {
                // Check the content of the row and update the output dictionary accordingly
                if (row[0] === "Guideline") {
                    output['parts'][currentKey]["Guideline"] = row[2];
                } else if (row[1] === "Standard") {
                    output['parts'][currentKey]["Standards"].push({ "notes": [], "standard": row[2] });
                } else if (row[3] && output['parts'][currentKey]["Standards"].length > 0) {
                    output['parts'][currentKey]["Standards"][output['parts'][currentKey]["Standards"].length - 1]["notes"].push(row[3]);
                }
            }
        }
    });

    return output;
}

// Method to display JSON
function displayJson(data) {
    $('#json-output').jsonViewer(data);
}

// Method to store data into local storage
function saveDataToLocalStorage(key, data) {
    localStorage.setItem(key, JSON.stringify(data));
}

// Method to retrieve data into local storage
function getDataFromLocalStorage(key) {
    const data = localStorage.getItem(key);
    return data ? JSON.parse(data) : null;
}