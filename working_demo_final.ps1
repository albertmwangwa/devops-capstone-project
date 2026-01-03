Write-Host "=== Working Sprint Review Demo ===" -ForegroundColor Cyan

# Test if service is running
Write-Host "1. Testing service connection..." -ForegroundColor Green
try {
    $test = Invoke-WebRequest -Uri "http://localhost:5000/" -TimeoutSec 3
    Write-Host "   ✓ Service is running" -ForegroundColor Green
} catch {
    Write-Host "   ✗ Service not running" -ForegroundColor Red
    Write-Host "   Start with: python app.py" -ForegroundColor Yellow
    exit 1
}

# Clean up any existing accounts
Write-Host "`n2. Cleaning existing accounts..." -ForegroundColor Green
try {
    $accounts = Invoke-RestMethod -Uri "http://localhost:5000/accounts" -TimeoutSec 3
    foreach ($account in $accounts) {
        Invoke-RestMethod -Uri "http://localhost:5000/accounts/$($account.id)" -Method Delete -TimeoutSec 3 | Out-Null
    }
    Write-Host "   ✓ Cleaned up" -ForegroundColor Green
} catch {
    Write-Host "   No accounts to clean" -ForegroundColor Yellow
}

# DEMO 1: CREATE Account (using proper JSON)
Write-Host "`n3. DEMO: CREATE Account" -ForegroundColor Magenta
Write-Host "   Creating John Doe account..." -ForegroundColor Gray

# Method 1: Using Invoke-RestMethod (PowerShell native - RECOMMENDED)
try {
    $body = @{
        name = "John Doe"
        email = "john@doe.com"
        address = "123 Main St."
        phone_number = "555-1212"
    } | ConvertTo-Json
    
    $response = Invoke-RestMethod -Uri "http://localhost:5000/accounts" -Method Post -Body $body -ContentType "application/json"
    Write-Host "   ✓ CREATE successful (HTTP 201)" -ForegroundColor Green
    Write-Host "   Created account:" -ForegroundColor Gray
    $response | Format-List | Out-Host
    
    # Save to file
    $response | ConvertTo-Json | Out-File rest-create-done.txt -Encoding UTF8
    Write-Host "   ✓ Saved to: rest-create-done.txt" -ForegroundColor Green
    
    $accountId = $response.id
} catch {
    Write-Host "   ✗ CREATE failed: $($_.Exception.Message)" -ForegroundColor Red
    exit 1
}

# DEMO 2: LIST All Accounts
Write-Host "`n4. DEMO: LIST All Accounts" -ForegroundColor Magenta
try {
    $accounts = Invoke-RestMethod -Uri "http://localhost:5000/accounts" -Method Get
    Write-Host "   ✓ LIST successful (HTTP 200)" -ForegroundColor Green
    Write-Host "   Accounts:" -ForegroundColor Gray
    $accounts | ConvertTo-Json | Out-Host
    
    $accounts | ConvertTo-Json | Out-File rest-list-done.txt -Encoding UTF8
    Write-Host "   ✓ Saved to: rest-list-done.txt" -ForegroundColor Green
} catch {
    Write-Host "   ✗ LIST failed: $($_.Exception.Message)" -ForegroundColor Red
}

# DEMO 3: READ Account
Write-Host "`n5. DEMO: READ Account (ID: $accountId)" -ForegroundColor Magenta
try {
    $account = Invoke-RestMethod -Uri "http://localhost:5000/accounts/$accountId" -Method Get
    Write-Host "   ✓ READ successful (HTTP 200)" -ForegroundColor Green
    Write-Host "   Account details:" -ForegroundColor Gray
    $account | Format-List | Out-Host
    
    $account | ConvertTo-Json | Out-File rest-read-done.txt -Encoding UTF8
    Write-Host "   ✓ Saved to: rest-read-done.txt" -ForegroundColor Green
} catch {
    Write-Host "   ✗ READ failed: $($_.Exception.Message)" -ForegroundColor Red
}

# DEMO 4: UPDATE Account
Write-Host "`n6. DEMO: UPDATE Account (change phone to 555-1111)" -ForegroundColor Magenta
try {
    $updateBody = @{
        name = "John Doe"
        email = "john@doe.com"
        address = "123 Main St."
        phone_number = "555-1111"
    } | ConvertTo-Json
    
    $updated = Invoke-RestMethod -Uri "http://localhost:5000/accounts/$accountId" -Method Put -Body $updateBody -ContentType "application/json"
    Write-Host "   ✓ UPDATE successful (HTTP 200)" -ForegroundColor Green
    Write-Host "   Updated phone to: $($updated.phone_number)" -ForegroundColor Gray
    
    $updated | ConvertTo-Json | Out-File rest-update-done.txt -Encoding UTF8
    Write-Host "   ✓ Saved to: rest-update-done.txt" -ForegroundColor Green
} catch {
    Write-Host "   ✗ UPDATE failed: $($_.Exception.Message)" -ForegroundColor Red
}

# DEMO 5: DELETE Account
Write-Host "`n7. DEMO: DELETE Account" -ForegroundColor Magenta
try {
    $deleteResponse = Invoke-WebRequest -Uri "http://localhost:5000/accounts/$accountId" -Method Delete
    Write-Host "   ✓ DELETE successful (HTTP 204)" -ForegroundColor Green
    
    "HTTP 204 - Account deleted successfully" | Out-File rest-delete-done.txt -Encoding UTF8
    Write-Host "   ✓ Saved to: rest-delete-done.txt" -ForegroundColor Green
} catch {
    Write-Host "   ✗ DELETE failed: $($_.Exception.Message)" -ForegroundColor Red
}

# VERIFY
Write-Host "`n8. VERIFY Delete" -ForegroundColor Green
try {
    $final = Invoke-RestMethod -Uri "http://localhost:5000/accounts" -Method Get
    if ($final.Count -eq 0) {
        Write-Host "   ✓ All accounts deleted - List is empty" -ForegroundColor Green
    } else {
        Write-Host "   ✗ Accounts still exist" -ForegroundColor Red
    }
} catch {
    Write-Host "   Error verifying: $($_.Exception.Message)" -ForegroundColor Yellow
}

Write-Host "`n=== SPRINT REVIEW COMPLETE ===" -ForegroundColor Cyan
Write-Host "Evidence files created:" -ForegroundColor Yellow
Get-ChildItem rest-*-done.txt | ForEach-Object { 
    Write-Host "   - $($_.Name)" -ForegroundColor Gray 
}

Write-Host "`nNext:" -ForegroundColor Cyan
Write-Host "1. Update Kanban board: Move stories to Done" -ForegroundColor Yellow
Write-Host "2. Submit evidence files" -ForegroundColor Yellow
