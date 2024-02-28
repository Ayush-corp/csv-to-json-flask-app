from flask import Flask, request, render_template, jsonify

app = Flask(__name__)

def convertCSVtoJson(csvContent):

    # Initialize the output object
    output = {"parts": {}}
    currentKey = None

    try:
        csvContent = csvContent.decode('utf-8')
    except UnicodeDecodeError:
        csvContent = csvContent.decode('utf-8', errors='replace')

    # Read the CSV file
    fileContent = csvContent.split('\n')
    fileContentFilter = fileContent[2:]  # Skip the first two lines

    # Iterate over each row in the CSV
    for line in fileContentFilter:
        row = line.split(',')[:-1]

        # Remove empty row
        if len(row) == 0:
            continue
        
        # Check if the first column is not empty and not "Guideline"
        if 'Area' in row:
            output['Area'] = row[row.index('Area') + 1]
        if 'Dims' in row:
            output['Dims'] = row[row.index('Dims') + 1].replace("\\", '').replace('"', '')

        if row[0] != '' and row[0] != "Guideline":
            # Update the current key
            currentKey = row[0]
            # Create a new entry in the output dictionary
            output['parts'][currentKey] = {"Guideline": "", "Standards": []}

        else:
            # Check if there is a current key
            if currentKey:
                # Check the content of the row and update the output dictionary accordingly
                if row[0] == "Guideline":
                    output['parts'][currentKey]["Guideline"] = row[2]
                elif row[1] == "Standard":
                    output['parts'][currentKey]["Standards"].append({"notes": [], "standard": row[2]})
                elif row[3] and len(output['parts'][currentKey]["Standards"]) > 1:
                    output['parts'][currentKey]["Standards"][-1]["notes"].append(row[3])
    return output

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        csv_file = request.files['csvFile']
        if csv_file.filename != '':
            try:
                csv_content = csv_file.read()
                json_output = convertCSVtoJson(csv_content)
                return render_template('index.html', json_output=json_output)
            except Exception as e:
                error_message = f"Error: {str(e)}"
                return render_template('index.html', error=error_message)
        else:
            error_message = "No file selected"
            return render_template('index.html', error=error_message)
    return render_template('index.html')


