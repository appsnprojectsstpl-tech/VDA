/**
 * @jest-environment jsdom
 */

const fs = require('fs');
const path = require('path');

describe('DataImport.fromCSV', () => {
  beforeAll(() => {
    // Provide missing globals
    global.localStorage = {
      getItem: jest.fn(),
      setItem: jest.fn()
    };

    // Mock insforge
    window.insforge = {
      insert: jest.fn()
    };

    // Load the script
    const scriptContent = fs.readFileSync(path.resolve(__dirname, '../advanced_features.js'), 'utf8');

    // Evaluate the script in the context of the JSDOM window
    // Use eval here because Jest's jsdom does not execute injected script tags by default
    eval(scriptContent);
  });

  afterEach(() => {
    jest.clearAllMocks();
  });

  it('should return errors when window.insforge.insert fails', async () => {
    const csvData = "name,email\nTest,test@example.com";
    const tableName = "test_table";

    // Setup the mock to throw an error
    const errorMessage = "Database constraint failed";
    window.insforge.insert.mockRejectedValue(new Error(errorMessage));

    // Call the function
    const results = await window.DataImport.fromCSV(csvData, tableName);

    // Verify expectations
    expect(window.insforge.insert).toHaveBeenCalledTimes(1);
    expect(window.insforge.insert).toHaveBeenCalledWith(tableName, {
      name: "Test",
      email: "test@example.com"
    });

    expect(results).toEqual({
      success: 0,
      failed: 1,
      errors: [errorMessage]
    });
  });

  it('should return successful results when window.insforge.insert succeeds', async () => {
    const csvData = "name,email\nTest,test@example.com";
    const tableName = "test_table";

    // Setup the mock to succeed
    window.insforge.insert.mockResolvedValue({ id: 1 });

    // Call the function
    const results = await window.DataImport.fromCSV(csvData, tableName);

    // Verify expectations
    expect(window.insforge.insert).toHaveBeenCalledTimes(1);
    expect(window.insforge.insert).toHaveBeenCalledWith(tableName, {
      name: "Test",
      email: "test@example.com"
    });

    expect(results).toEqual({
      success: 1,
      failed: 0,
      errors: []
    });
  });
});
