from flask import Flask, request, render_template, jsonify

app = Flask(__name__)

# Method to convert CSV data into JSON
def convert_CSV_to_JSON(csv_content):

    # Initialize the output object
    output = {"parts": {}, "Project Name": "", "Space Name" : ""}
    current_key = None

    try:
        # Decode CSV content to utf-8
        csv_content = csv_content.decode('utf-8')
    except UnicodeDecodeError:
        # Replace any encoding errors with a placeholder
        csv_content = csv_content.decode('utf-8', errors='replace')

    # Split CSV content into lines
    lines = csv_content.strip('\n\r').split('\n')

    # Extract project name and space name
    output['Project Name'] = lines[0].split(',')[0]
    output['Space Name'] = lines[1].split(',')[0]

    # Remove header lines
    lines = lines[2:]

    # Iterate over each row in the CSV
    for line in lines:
        # Split line into columns
        columns = line.split(',')[:-1]

        # Skip empty rows
        if len(columns) == 0:
            continue

        # Check if the first column is not empty and not "Guideline"
        if 'Area' in columns:
            output['Area'] = columns[columns.index('Area') + 1]
        if 'Dims' in columns:
            output['Dims'] = columns[columns.index('Dims') + 1].replace("\\", '').replace('"', '')

        if columns[0] != '' and columns[0] != "Guideline":
            # Update the current key
            current_key = columns[0]
            # Create a new entry in the output dictionary
            output['parts'][current_key] = {"Guideline": "", "Standards": []}

        else:
            # Check if there is a current key
            if current_key:
                # Check the content of the row and update the output dictionary accordingly
                if columns[0] == "Guideline":
                    output['parts'][current_key]["Guideline"] = columns[2]
                elif columns[1] == "Standard" or (columns[1] == "" and columns[2]):
                    output['parts'][current_key]["Standards"].append({"notes": [], "standard": columns[2]})
                elif columns[3] and len(output['parts'][current_key]["Standards"]) > 1:
                    output['parts'][current_key]["Standards"][-1]["notes"].append(columns[3])

    # Return the JSON output
    return output

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Read the uploaded CSV file
        csv_file = request.files['csvFile']
        if csv_file.filename != '':
            try:
                # Read the content of the CSV file
                csv_content = csv_file.read()
                # Convert CSV content to JSON
                json_output = convert_CSV_to_JSON(csv_content)
                return render_template('index.html', json_output=json_output)
            except Exception as e:
                # Handle any errors during CSV to JSON conversion
                error_message = f"Error: {str(e)}"
                return render_template('index.html', error=error_message)
        else:
            # Error message for no file selected
            error_message = "No file selected"
            return render_template('index.html', error=error_message)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
