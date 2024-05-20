"""
 MIT License
 
 Copyright (c) 2024 Riccardo Leonelli
 
 Permission is hereby granted, free of charge, to any person obtaining a copy
 of this software and associated documentation files (the "Software"), to deal
 in the Software without restriction, including without limitation the rights
 to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 copies of the Software, and to permit persons to whom the Software is
 furnished to do so, subject to the following conditions:
 
 The above copyright notice and this permission notice shall be included in all
 copies or substantial portions of the Software.
 
 THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
 SOFTWARE.
 
"""

import pytest
from fastapi.testclient import TestClient
from app.main import app
from unittest.mock import MagicMock, patch, mock_open

client = TestClient(app)

def test_add_or_update_person():
    response = client.post("/api/add_or_update_person", data={
        "rowId": 123456789,
        "first_name": "MOCK_NAME",
        "last_name": "MOCK_SURNAME",
        "email": "MOKE.MAIL@example.com",
        "role": "IT",
        "hire_date": "2023-01-01",
        "end_date": "2023-12-31",
        "user_password": "password123"
    })
    assert response.status_code == 200
    assert response.json() == {"message": "Person updated"} or response.json() == {"message": "Person added"}

def test_insert_presence():
    response = client.post("/api/insert_presence", data={"id": "123456789"})
    assert response.status_code == 200
    assert response.json() == {"message": "Presence logged successfully"}

def test_delete_person():
    response = client.post("/api/delete_person", data={"rowId": 123456789})
    assert response.status_code == 200
    assert response.json() == {"message": "Person deleted"}

@patch('app.services.AccessService.AccessService.extract_delays')
def test_extract_delays(mock_extract_delays):
    mock_extract_delays.return_value = 'delays_05012024.xlsx'
    # Mock the file existence and file opening
    with patch('os.path.exists', return_value=True), \
         patch('builtins.open', mock_open(read_data="data")) as mocked_file:
        response = client.get("/api/extract_delays", params={"monthYear": "2023-05-01"})
        assert response.status_code == 200
        mocked_file.assert_called_with('delays_05012024.xlsx', 'rb')  # Ensure file is opened as expected


@patch('app.services.AccessService.AccessService.create_excel_report', return_value='month_report_2024_05.xlsx')
@patch('os.path.exists', return_value=True)
@patch('builtins.open', new_callable=MagicMock)
def test_create_excel_report(mock_open, mock_exists, mock_create_excel_report):
    response = client.get("/api/create_excel_report", params={"monthYear": "2024-05-01"})
    assert response.status_code == 200
    assert response.headers['content-type'] == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
