Write-Host "=== SPRINT REVIEW DEMO ===" -ForegroundColor Cyan
Write-Host "Running complete CRUD demo for Account Service" -ForegroundColor Yellow

Write-Host "`nIMPORTANT: Make sure Flask is running in another terminal!" -ForegroundColor Red
Write-Host "Run this in a separate terminal while 'python app.py' is running" -ForegroundColor Yellow
Write-Host ""

# Test if service is running with curl
Write-Host "1. Testing if service is running..." -ForegroundColor Green
$testResult = curl -s -o $null -w "%{http_code}" http://localhost:5000/
if ($testResult -eq "200") {
    Write-Host "   ✓ Service is running (HTTP $testResult)" -ForegroundColor Green
} else {
    Write-Host "   ✗ Service not responding (HTTP $testResult)" -ForegroundColor Red
    Write-Host "   Start the service with: python app.py" -ForegroundColor Yellow
    exit 1
}

# Clean slate - delete any existing accounts
Write-Host "`n2. Cleaning up any existing accounts..." -ForegroundColor Green
$existing = curl -s http://localhost:5000/accounts
if ($existing -and $existing -ne "[]") {
    # Parse JSON and delete each account
    $accounts = $existing | ConvertFrom-Json
    foreach ($account in $accounts) {
        curl -X DELETE http://localhost:5000/accounts/$($account.id) -s -o $null
    }
    Write-Host "   ✓ Cleaned up existing accounts" -ForegroundColor Green
} else {
    Write-Host "   No accounts to clean up" -ForegroundColor Yellow
}

# DEMO 1: CREATE Account
Write-Host "`n3. DEMO: CREATE Account (John Doe)" -ForegroundColor Magenta
Write-Host "   Command:" -ForegroundColor Gray
Write-Host '   curl -i -X POST http://127.0.0.1:5000/accounts \' -ForegroundColor Gray
Write-Host '   -H "Content-Type: application/json" \' -ForegroundColor Gray
Write-Host '   -d "{\"name\":\"John Doe\",\"email\":\"john@doe.com\",\"address\":\"123 Main St.\",\"phone_number\":\"555-1212\"}"' -ForegroundColor Gray
Write-Host "`n   Output:" -ForegroundColor Gray
$createOutput = curl -i -X POST http://127.0.0.1:5000/accounts -H "Content-Type: application/json" -d '{"name":"John Doe","email":"john@doe.com","address":"123 Main St.","phone_number":"555-1212"}'
$createOutput
$createOutput | Out-File -FilePath "rest-create-done.txt" -Encoding UTF8
Write-Host "`n   ✓ Saved to: rest-create-done.txt" -ForegroundColor Green

# DEMO 2: LIST All Accounts
Write-Host "`n4. DEMO: LIST All Accounts" -ForegroundColor Magenta
Write-Host "   Command: curl -i -X GET http://127.0.0.1:5000/accounts" -ForegroundColor Gray
Write-Host "`n   Output:" -ForegroundColor Gray
$listOutput = curl -i -X GET http://127.0.0.1:5000/accounts
$listOutput
$listOutput | Out-File -FilePath "rest-list-done.txt" -Encoding UTF8
Write-Host "`n   ✓ Saved to: rest-list-done.txt" -ForegroundColor Green

# DEMO 3: READ Account
Write-Host "`n5. DEMO: READ Account (ID: 1)" -ForegroundColor Magenta
Write-Host "   Command: curl -i -X GET http://127.0.0.1:5000/accounts/1" -ForegroundColor Gray
Write-Host "`n   Output:" -ForegroundColor Gray
$readOutput = curl -i -X GET http://127.0.0.1:5000/accounts/1
$readOutput
$readOutput | Out-File -FilePath "rest-read-done.txt" -Encoding UTF8
Write-Host "`n   ✓ Saved to: rest-read-done.txt" -ForegroundColor Green

# DEMO 4: UPDATE Account (change phone number)
Write-Host "`n6. DEMO: UPDATE Account (change phone to 555-1111)" -ForegroundColor Magenta
Write-Host "   Command:" -ForegroundColor Gray
Write-Host '   curl -i -X PUT http://127.0.0.1:5000/accounts/1 \' -ForegroundColor Gray
Write-Host '   -H "Content-Type: application/json" \' -ForegroundColor Gray
Write-Host '   -d "{\"name\":\"John Doe\",\"email\":\"john@doe.com\",\"address\":\"123 Main St.\",\"phone_number\":\"555-1111\"}"' -ForegroundColor Gray
Write-Host "`n   Output:" -ForegroundColor Gray
$updateOutput = curl -i -X PUT http://127.0.0.1:5000/accounts/1 -H "Content-Type: application/json" -d '{"name":"John Doe","email":"john@doe.com","address":"123 Main St.","phone_number":"555-1111"}'
$updateOutput
$updateOutput | Out-File -FilePath "rest-update-done.txt" -Encoding UTF8
Write-Host "`n   ✓ Saved to: rest-update-done.txt" -ForegroundColor Green

# DEMO 5: DELETE Account
Write-Host "`n7. DEMO: DELETE Account" -ForegroundColor Magenta
Write-Host "   Command: curl -i -X DELETE http://127.0.0.1:5000/accounts/1" -ForegroundColor Gray
Write-Host "`n   Output:" -ForegroundColor Gray
$deleteOutput = curl -i -X DELETE http://127.0.0.1:5000/accounts/1
$deleteOutput
$deleteOutput | Out-File -FilePath "rest-delete-done.txt" -Encoding UTF8
Write-Host "`n   ✓ Saved to: rest-delete-done.txt" -ForegroundColor Green

# Final verification
Write-Host "`n8. Final Verification" -ForegroundColor Green
Write-Host "   Listing all accounts (should be empty):" -ForegroundColor Gray
$finalList = curl -s http://localhost:5000/accounts
if ($finalList -eq "[]") {
    Write-Host "   ✓ All accounts deleted successfully!" -ForegroundColor Green
} else {
    Write-Host "   ✗ Accounts still exist: $finalList" -ForegroundColor Red
}

Write-Host "`n=== SPRINT REVIEW COMPLETE ===" -ForegroundColor Cyan
Write-Host "Evidence files created in current directory:" -ForegroundColor Yellow
Get-ChildItem rest-*-done.txt | ForEach-Object { 
    Write-Host "   - $($_.Name) ($($_.Length) bytes)" -ForegroundColor Gray 
}

Write-Host "`nNext steps:" -ForegroundColor Cyan
Write-Host "1. Update Kanban board: Move stories to Closed/Done" -ForegroundColor Yellow
Write-Host "2. Submit evidence files for grading" -ForegroundColor Yellow
Write-Host "3. For Option 2 (Peer-Graded): Take screenshots of terminal output" -ForegroundColor Yellow
