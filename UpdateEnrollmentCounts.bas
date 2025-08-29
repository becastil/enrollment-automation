Attribute VB_Name = "UpdateEnrollmentCounts"
'===============================================================================
' Module: UpdateEnrollmentCounts
' Purpose: Updates enrollment counts in Excel template from CSV data
' Author: Prime Enrollment System
' Date: Generated automatically
'===============================================================================

Option Explicit

' Constants for file paths (update these as needed)
Const CSV_FILE_PATH As String = "C:\Users\becas\Prime_EFR\enrollment_data_detailed.csv"
Const DISCOVERY_MAP_PATH As String = "C:\Users\becas\Prime_EFR\config\enrollment_discovery_map.json"

' Main update procedure
Public Sub UpdateEnrollmentFromCSV()
    Dim startTime As Single
    startTime = Timer
    
    On Error GoTo ErrorHandler
    
    Application.ScreenUpdating = False
    Application.Calculation = xlCalculationManual
    Application.DisplayAlerts = False
    
    ' Status update
    Application.StatusBar = "Loading enrollment data from CSV..."
    
    ' Load CSV data
    Dim csvData As Collection
    Set csvData = LoadCSVData(CSV_FILE_PATH)
    
    If csvData Is Nothing Or csvData.Count = 0 Then
        MsgBox "No data loaded from CSV file.", vbExclamation, "No Data"
        GoTo Cleanup
    End If
    
    ' Process each enrollment record
    Dim successCount As Long, failCount As Long
    Dim record As Variant
    Dim updateResult As Boolean
    
    successCount = 0
    failCount = 0
    
    For Each record In csvData
        Application.StatusBar = "Processing " & record("ClientID") & " - " & record("Tier")
        
        updateResult = UpdateEnrollmentCell( _
            record("Tab"), _
            record("ClientID"), _
            record("PlanType"), _
            record("PlanName"), _
            record("Tier"), _
            record("Value") _
        )
        
        If updateResult Then
            successCount = successCount + 1
        Else
            failCount = failCount + 1
        End If
    Next record
    
    ' Show results
    Dim elapsedTime As Single
    elapsedTime = Timer - startTime
    
    MsgBox "Update Complete!" & vbCrLf & vbCrLf & _
           "Successfully updated: " & successCount & " values" & vbCrLf & _
           "Failed: " & failCount & " values" & vbCrLf & vbCrLf & _
           "Time taken: " & Format(elapsedTime, "0.0") & " seconds", _
           vbInformation, "Enrollment Update Complete"
    
Cleanup:
    Application.ScreenUpdating = True
    Application.Calculation = xlCalculationAutomatic
    Application.DisplayAlerts = True
    Application.StatusBar = False
    Exit Sub
    
ErrorHandler:
    MsgBox "Error: " & Err.Description, vbCritical, "Update Failed"
    Resume Cleanup
End Sub

' Load CSV data into collection
Private Function LoadCSVData(csvPath As String) As Collection
    Dim fso As Object
    Dim textStream As Object
    Dim csvLine As String
    Dim headers() As String
    Dim values() As String
    Dim dataCollection As New Collection
    Dim record As Object
    Dim i As Long
    Dim isFirstLine As Boolean
    
    Set fso = CreateObject("Scripting.FileSystemObject")
    
    ' Check if file exists
    If Not fso.FileExists(csvPath) Then
        MsgBox "CSV file not found: " & csvPath, vbCritical, "File Not Found"
        Set LoadCSVData = Nothing
        Exit Function
    End If
    
    ' Open CSV file
    Set textStream = fso.OpenTextFile(csvPath, 1) ' 1 = ForReading
    
    isFirstLine = True
    
    ' Read each line
    Do While Not textStream.AtEndOfStream
        csvLine = textStream.ReadLine
        
        If isFirstLine Then
            ' Parse headers
            headers = Split(csvLine, ",")
            isFirstLine = False
        Else
            ' Parse data row
            values = Split(csvLine, ",")
            
            ' Create dictionary-like object for this record
            Set record = CreateObject("Scripting.Dictionary")
            
            For i = 0 To UBound(headers)
                If i <= UBound(values) Then
                    record.Add headers(i), values(i)
                End If
            Next i
            
            dataCollection.Add record
        End If
    Loop
    
    textStream.Close
    
    Set LoadCSVData = dataCollection
End Function

' Update a single enrollment cell
Private Function UpdateEnrollmentCell(tabName As String, clientID As String, _
                                     planType As String, planName As String, tier As String, _
                                     value As Variant) As Boolean
    On Error GoTo ErrorHandler
    
    Dim ws As Worksheet
    Dim foundCell As Range
    Dim targetCell As Range
    
    ' Check if worksheet exists
    On Error Resume Next
    Set ws = ThisWorkbook.Worksheets(tabName)
    On Error GoTo ErrorHandler
    
    If ws Is Nothing Then
        Debug.Print "Tab not found: " & tabName
        UpdateEnrollmentCell = False
        Exit Function
    End If
    
    ' Find Client ID in the worksheet
    Set foundCell = FindClientID(ws, clientID)
    
    If foundCell Is Nothing Then
        Debug.Print "Client ID not found: " & clientID & " in " & tabName
        UpdateEnrollmentCell = False
        Exit Function
    End If
    
    ' Find the target cell for this tier
    Set targetCell = FindTierCell(ws, foundCell, planType, planName, tier)
    
    If targetCell Is Nothing Then
        Debug.Print "Tier cell not found for: " & clientID & "/" & planType & "/" & tier
        UpdateEnrollmentCell = False
        Exit Function
    End If
    
    ' Update the value
    targetCell.Value = CDbl(value)
    
    UpdateEnrollmentCell = True
    Exit Function
    
ErrorHandler:
    Debug.Print "Error updating " & clientID & ": " & Err.Description
    UpdateEnrollmentCell = False
End Function

' Find Client ID in worksheet
Private Function FindClientID(ws As Worksheet, clientID As String) As Range
    Dim searchRange As Range
    Dim foundCell As Range
    Dim col As Range
    
    ' Search in columns A through E for Client ID
    For Each col In ws.Range("A:E").Columns
        Set searchRange = col.Cells(1, 1).Resize(200, 1) ' Search first 200 rows
        
        ' Try exact match first
        Set foundCell = searchRange.Find(What:=clientID, LookIn:=xlValues, _
                                        LookAt:=xlPart, MatchCase:=False)
        
        If Not foundCell Is Nothing Then
            Set FindClientID = foundCell
            Exit Function
        End If
    Next col
    
    Set FindClientID = Nothing
End Function

' Find the target cell for a specific tier
Private Function FindTierCell(ws As Worksheet, clientIDCell As Range, _
                             planType As String, planName As String, tier As String) As Range
    Dim searchRow As Long
    Dim maxRows As Long
    Dim cellValue As String
    Dim planFound As Boolean
    Dim tierColumn As Long
    Dim valueColumn As Long
    
    ' Typically tier names are in column C or D, values in column D or E
    ' Adjust based on your template structure
    
    searchRow = clientIDCell.Row + 1
    maxRows = 50 ' Maximum rows to search below Client ID
    planFound = False
    
    ' Look for plan type indicator
    Do While searchRow <= clientIDCell.Row + maxRows
        cellValue = UCase(Trim(ws.Cells(searchRow, clientIDCell.Column).Value))
        
        ' Check if this row contains the plan type
        If (planType = "EPO" And InStr(cellValue, "EPO") > 0) Or _
           (planType = "VALUE" And InStr(cellValue, "VALUE") > 0) Then
            planFound = True
            searchRow = searchRow + 1 ' Move to tier rows
            Exit Do
        End If
        
        searchRow = searchRow + 1
    Loop
    
    If Not planFound Then
        Set FindTierCell = Nothing
        Exit Function
    End If
    
    ' Now look for the specific tier
    ' Assume tiers are in column C (3) and values in column D (4)
    ' Adjust these based on your actual template
    tierColumn = 3
    valueColumn = 4
    
    Dim tierSearchLimit As Long
    tierSearchLimit = searchRow + 10 ' Search next 10 rows for tiers
    
    Do While searchRow <= tierSearchLimit
        cellValue = UCase(Trim(ws.Cells(searchRow, tierColumn).Value))
        
        ' Normalize and match tier name
        If MatchTierName(cellValue, tier) Then
            Set FindTierCell = ws.Cells(searchRow, valueColumn)
            Exit Function
        End If
        
        searchRow = searchRow + 1
    Loop
    
    Set FindTierCell = Nothing
End Function

' Match tier names with normalization
Private Function MatchTierName(cellTier As String, searchTier As String) As Boolean
    Dim normalizedCell As String
    Dim normalizedSearch As String
    
    ' Normalize both tier names for comparison
    normalizedCell = NormalizeTierName(cellTier)
    normalizedSearch = NormalizeTierName(searchTier)
    
    MatchTierName = (normalizedCell = normalizedSearch)
End Function

' Normalize tier names to standard format
Private Function NormalizeTierName(tierName As String) As String
    Dim normalized As String
    normalized = UCase(Trim(tierName))
    
    ' Map various tier name formats to standard names
    If InStr(normalized, "EE ONLY") > 0 Or _
       InStr(normalized, "EMP") > 0 Or _
       InStr(normalized, "EMPLOYEE ONLY") > 0 Then
        NormalizeTierName = "EE ONLY"
        
    ElseIf InStr(normalized, "EE+SPOUSE") > 0 Or _
           InStr(normalized, "ESP") > 0 Or _
           InStr(normalized, "EMPLOYEE + SPOUSE") > 0 Then
        NormalizeTierName = "EE+SPOUSE"
        
    ElseIf InStr(normalized, "EE+CHILD") > 0 Or _
           InStr(normalized, "ECH") > 0 Or _
           InStr(normalized, "EMPLOYEE + CHILD") > 0 Then
        NormalizeTierName = "EE+CHILD(REN)"
        
    ElseIf InStr(normalized, "EE+FAMILY") > 0 Or _
           InStr(normalized, "FAM") > 0 Or _
           InStr(normalized, "FAMILY") > 0 Then
        NormalizeTierName = "EE+FAMILY"
        
    ElseIf InStr(normalized, "EE+1") > 0 Or _
           InStr(normalized, "E1D") > 0 Or _
           InStr(normalized, "1 DEP") > 0 Then
        NormalizeTierName = "EE+1 DEP"
        
    Else
        NormalizeTierName = normalized
    End If
End Function

' Quick test procedure
Public Sub TestSingleUpdate()
    Dim result As Boolean
    
    ' Test with a known facility
    result = UpdateEnrollmentCell("Monroe", "H3397", "EPO", "EPO (Default)", "EE+Family", 100)
    
    If result Then
        MsgBox "Test update successful!", vbInformation
    Else
        MsgBox "Test update failed.", vbExclamation
    End If
End Sub

' Utility to show current status
Public Sub ShowEnrollmentStatus()
    Dim csvData As Collection
    Set csvData = LoadCSVData(CSV_FILE_PATH)
    
    If csvData Is Nothing Then
        MsgBox "Could not load CSV data", vbExclamation
        Exit Sub
    End If
    
    MsgBox "CSV contains " & csvData.Count & " enrollment records ready to update.", _
           vbInformation, "Enrollment Data Status"
End Sub