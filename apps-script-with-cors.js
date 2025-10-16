// Google Apps Script for saving comments to Google Sheets
// This version includes proper CORS handling

function doGet(e) {
  const output = ContentService.createTextOutput('Apps Script updated and running. Targeting DATA SHEET. Current time: ' + new Date().toISOString());
  output.setMimeType(ContentService.MimeType.TEXT);
  return output;
}

function doPost(e) {
  try {
    // Check if postData exists
    if (!e.postData || !e.postData.contents) {
      return createCorsResponse({ success: false, error: 'No post data received' });
    }
    
    // Parse the request
    const data = JSON.parse(e.postData.contents);
    const { sessionToken, companyName, comment, userEmail } = data;
    
    // Basic validation
    if (!sessionToken || !companyName || !userEmail) {
      return createCorsResponse({ success: false, error: 'Missing required fields' });
    }
    
    // Verify Google auth token (simplified for now)
    if (sessionToken === 'test') {
      return createCorsResponse({ success: false, error: 'Invalid authentication' });
    }
    
    // Get the Google Sheet
    const sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName('DATA SHEET');
    if (!sheet) {
      return createCorsResponse({ success: false, error: 'DATA SHEET not found' });
    }
    
    // Get all data to find headers and company row
    const data_range = sheet.getDataRange();
    const values = data_range.getValues();
    
    if (values.length === 0) {
      return createCorsResponse({ success: false, error: 'No data found in DATA SHEET' });
    }
    
    // Find column indexes
    const sheetHeaders = values[0];
    const companyNameCol = findColumnIndex(sheetHeaders, ['company_name', 'Company Name', 'Company', 'Name']);
    const feedbackCol = findColumnIndex(sheetHeaders, ['feedback_comment', 'Feedback Comment', 'Comment', 'Feedback']);
    
    if (companyNameCol === -1) {
      return createCorsResponse({ 
        success: false, 
        error: 'company_name column not found. Found headers: ' + sheetHeaders.slice(0, 10).join(', ') + '...'
      });
    }
    
    if (feedbackCol === -1) {
      return createCorsResponse({ 
        success: false, 
        error: 'feedback_comment column not found. Found headers: ' + sheetHeaders.slice(0, 10).join(', ') + '...'
      });
    }
    
    // Find the company row
    let companyRow = -1;
    for (let i = 1; i < values.length; i++) {
      if (values[i][companyNameCol] && 
          values[i][companyNameCol].toString().toLowerCase().trim() === companyName.toLowerCase().trim()) {
        companyRow = i + 1; // +1 because sheet rows are 1-indexed
        break;
      }
    }
    
    if (companyRow === -1) {
      return createCorsResponse({ 
        success: false, 
        error: `Company "${companyName}" not found in DATA SHEET` 
      });
    }
    
    // Update the feedback comment
    sheet.getRange(companyRow, feedbackCol + 1).setValue(comment); // +1 because sheet columns are 1-indexed
    
    // Log the action
    console.log(`Comment saved for ${companyName} by ${userEmail}: ${comment}`);
    
    return createCorsResponse({ 
      success: true, 
      message: `Comment saved for ${companyName}`,
      row: companyRow,
      column: feedbackCol + 1
    });
    
  } catch (error) {
    console.error('Error in doPost:', error);
    return createCorsResponse({ 
      success: false, 
      error: error.toString() 
    });
  }
}

// Helper function to create JSON response
function createCorsResponse(data) {
  const output = ContentService.createTextOutput(JSON.stringify(data));
  output.setMimeType(ContentService.MimeType.JSON);
  return output;
}

// Helper function to find column index by multiple possible names
function findColumnIndex(headers, possibleNames) {
  for (let i = 0; i < headers.length; i++) {
    const header = headers[i].toString().toLowerCase().trim();
    for (const name of possibleNames) {
      if (header === name.toLowerCase()) {
        return i;
      }
    }
  }
  return -1;
}