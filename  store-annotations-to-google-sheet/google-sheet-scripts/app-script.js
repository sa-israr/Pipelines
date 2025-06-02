function handleSpreadsheetPost(e) {
  try {
    const body = JSON.parse(e.postData.contents);

    if (body.type !== "spreadsheet" || !body.data) {
      return ContentService.createTextOutput(JSON.stringify({ error: "Invalid payload structure" }))
                           .setMimeType(ContentService.MimeType.JSON);
    }

    const payload = body.data;
    const columns = payload.columns || [];
    const rows = payload.rows || [];
    const sheetName = "Sheet2";

    const sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName(sheetName);
    if (!sheet) {
      Logger.error("Sheet not found: " + sheetName);
      return ContentService.createTextOutput(JSON.stringify({ error: "Sheet not found: " + sheetName }))
                           .setMimeType(ContentService.MimeType.JSON);
    }

    Logger.log("Columns received: " + columns.join(", "));
    Logger.log("Number of rows: " + rows.length);

    if (sheet.getLastRow() === 0 && columns.length > 0) {
      sheet.getRange(1, 1, 1, columns.length).setValues([columns]);
    }

    if (rows.length > 0) {
      sheet.getRange(sheet.getLastRow() + 1, 1, rows.length, columns.length).setValues(rows);
    }

    return ContentService.createTextOutput(JSON.stringify({ status: "success", rowsAdded: rows.length }))
                         .setMimeType(ContentService.MimeType.JSON);
  } catch (error) {
    Logger.log("Error: " + error.message);
    return ContentService.createTextOutput(JSON.stringify({ error: error.message }))
                         .setMimeType(ContentService.MimeType.JSON);
  }
}
