const french_stopwords = ["de", "se", "des", "ca", "ce", "ne", "pas", "par", "pour", "s'y",
    "un", "une", "sur", "les", "en", "au", "que", "hors", "sans", "a",
    "avec", "dans", "du", "sa", "son", "ses", "qc", "qn", "la", "y", "le", "c'est",
    "!", "d'", "m'", "l'", ",e", ",ve", ",ice", ",ne", ",le", ",que", ",ière"]

const english_stopwords = ["over", "to", "in", "into", "oneself", "with", "so", "sth", "by", "one's",
    "on", "the", "of", "at", "from", "together", "out", "against", "a", "an", "up", "for"]

function normalizeString(str, stopwords) {

    str = str.toLowerCase();

    // Step 1: Replace "-" and "/" with blank space
    str = str.replace(/[-/]/g, ' ');

    // Step 2: Remove text within round or square brackets
    str = str.replace(/\(.*?\)|\[.*?]/g, '');

    // Step 3: Remove accents
    str = str.normalize('NFD').replace(/[\u0300-\u036f]/g, '');

    // Step 4: Remove stop words
    stopwords.forEach((word) => {
        const regex = new RegExp(`\\b${word}\\b`, 'gi');
        str = str.replace(regex, '');
    });

    // Step 5: remove two or more consecutive blank spaces
    str = str.replace(/\s{2,}/g, ' ');

    // Step 6: remove leading and trailing blank spaces
    return str.trim();
}

const rows = [1, 2, 3]
rows.forEach((row) => {
    console.log(row)
})

for (var i = 0; i < rows.length; i++) {
    console.log(rows[i])
}

// const raw_words =
//     ["pave-me/nt (m)", "débridé", "déchaîné", "aléa (m)",
//       "aléas (m)", "survenance", "survenir", "galerie de toit (f)",
//       "porte-skis (m)", "triage (m)", "trier", "déclaration (f)", "énoncé (m)",
//       "relevé (m)", "foncier", "primordial", "épancher (son coeur)", "exutoire à qc (m)"]
//
//  let result = []
//  raw_words.forEach((word) => {
//    result.push(normalizeString(word, french_stopwords))
//  })
//
// console.log(`Original: ${raw_words}`);
// console.log(`Normalized: ${result}`);
// console.log(new  Date("1/1/2010"))


function updateAndAppendRow(rowNumber) {
    // Get active spreadsheet and worksheet
    var sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();

    // Check if the row number is valid
    if (rowNumber <= 0 || rowNumber > sheet.getLastRow()) {
        return "Invalid row number";
    }

    // Get the entire row data
    var rowData = sheet.getRange(rowNumber, 1, 1, sheet.getLastColumn()).getValues()[0];

    // Update column G (which is the 7th element in the rowData array)
    rowData[6] = rowData[6] + 1;

    // Update column F with today's date (which is the 6th element in the rowData array)
    rowData[5] = new Date();

    // Update the row data in the sheet
    sheet.getRange(rowNumber, 1, 1, sheet.getLastColumn()).setValues([rowData]);

    // Append a copy of the updated row to the bottom of the sheet
    sheet.appendRow(rowData);

    return "Row updated and appended";
}

















