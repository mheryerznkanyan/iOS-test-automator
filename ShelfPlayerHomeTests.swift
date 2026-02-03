import XCTest

final class ShelfPlayerHomeTests: XCTestCase {
    var app: XCUIApplication!

    override func setUpWithError() throws {
        continueAfterFailure = false
        app = XCUIApplication()
    }

    override func tearDownWithError() throws {
        app = nil
    }

    func testOpenAppAndVerifyAudiobooksDisplayedOnHomeScreen() throws {
        // Launch the app
        app.launch()

        // Wait for the app to fully load and display the home screen
        let itemList = app.tables["itemList"]
        XCTAssertTrue(itemList.waitForExistence(timeout: 10), "Item list (audiobooks) should appear on home screen")

        // Verify that the item list is visible and contains content
        XCTAssertTrue(itemList.exists, "Audiobooks list should be displayed on the home screen")

        // Verify that the list is not empty by checking for cells
        let cells = itemList.cells
        XCTAssertGreaterThan(cells.count, 0, "Home screen should display at least one audiobook")
    }
}
