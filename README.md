# csv-to-json-flask-app

## Summary

The Flask code provided serves as a web application that converts CSV data into JSON format.

1. **CSV to JSON Conversion Function**: 
   - There is a function named `convert_CSV_to_JSON` responsible for converting CSV content into a JSON object.
   - It reads the uploaded CSV file, extracts the data, and transforms the data into dot notation.

2. **Flask Routes and Templates**: 
   - The Flask application defines the route `'/'` which serves as the main entry point and renders the `index.html` template.

3. **HTML Templates**: 
   - The `index.html` template includes a form where users can upload a CSV file.
   - When the form is submitted, it triggers the conversion process.
   - The template displays the JSON output or any error messages.
   - When the reset button is clicked, it clears the JSON output from the template.

4. **Error Handling**: 
   - The code includes error handling to manage cases where the uploaded file is not a valid CSV or if there are any errors during the conversion process.
   - Error messages are displayed to the user on the web interface.

5. **Sample CSV File**: 
   - The application directory also includes the `sample_data.csv` file.
   - The code is tailored to similar kinds of CSV or spreadsheet files.

## Usage

### Hosted App

1. Visit [https://ayush16855.pythonanywhere.com/](https://ayush16855.pythonanywhere.com/) in your web browser.
2. Upload a CSV file using the provided form.
3. Click the "Convert" button to initiate the conversion process.
4. View the JSON output or any error messages displayed on the web interface.

### Local

Alternatively, you can use the setup it on your local machine.
To use the CSV to JSON converter locally:
1. Clone this repository to your local machine.
2. Ensure you have Python and Flask installed.
3. Run the Flask application by executing `python app.py` in your terminal.
4. Open your web browser and navigate to `http://localhost:5000`.
5. Upload a CSV file using the provided form.
6. Click the "Convert" button to initiate the conversion process.
7. View the JSON output or any error messages displayed on the web interface.


## Notes

Feel free to modify the code or HTML templates to suit your specific requirements. The application is designed to handle various CSV formats and can be adapted for similar spreadsheet files.
