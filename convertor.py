from flask import Flask, request, jsonify

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

@app.route('/convert', methods=['POST'])
def convert_csv_to_json():
    csv_file = request.files.get('csvFile')
    if csv_file:
        try:
            csv_content = csv_file.read()
            json_output = convertCSVtoJson(csv_content)
            return jsonify(json_output)
        except Exception as e:
            return jsonify({"error": str(e)}), 400
    else:
        return jsonify({"error": "CSV file is missing"}), 400

if __name__ == '__main__':
    app.run(debug=True)
