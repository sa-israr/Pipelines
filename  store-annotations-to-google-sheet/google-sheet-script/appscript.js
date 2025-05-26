function doPost(e) {
  try {
    Logger.log("Received POST data: " + e.postData.contents);
    var data = JSON.parse(e.postData.contents);
    var sheetName = data.path || "Sheet1";
    var action = data.action;
    var annotations = data.annotations || [];

    var sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName(sheetName);
    if (!sheet) {
      Logger.log("Sheet not found: " + sheetName);
      return ContentService.createTextOutput(JSON.stringify({error: "Sheet not found: " + sheetName}))
                           .setMimeType(ContentService.MimeType.JSON);
    }

    Logger.log("Action: " + action + ", Annotations count: " + annotations.length);

    if (action === "write" && annotations.length > 0) {
      
      var headers = sheet.getRange(1, 1, 1, sheet.getLastColumn()).getValues()[0];
      Logger.log("Sheet headers: " + headers.join(", "));

      
      var rows = annotations.map(function(annotation, idx) {
        var row = headers.map(function(header) {
          var val = annotation[header];
          return (val !== undefined && val !== null) ? val : "";
        });
        Logger.log("Prepared row " + (idx+1) + ": " + row.join(", "));
        return row;
      });

     
      sheet.getRange(sheet.getLastRow() + 1, 1, rows.length, headers.length).setValues(rows);

      return ContentService.createTextOutput(JSON.stringify({status: "success", rowsAdded: rows.length}))
                           .setMimeType(ContentService.MimeType.JSON);
    } else {
      Logger.log("Invalid action or empty annotations");
      return ContentService.createTextOutput(JSON.stringify({error: "Invalid action or empty annotations"}))
                           .setMimeType(ContentService.MimeType.JSON);
    }
  } catch (error) {
    Logger.log("Error: " + error.message);
    return ContentService.createTextOutput(JSON.stringify({error: error.message}))
                         .setMimeType(ContentService.MimeType.JSON);
  }
}
