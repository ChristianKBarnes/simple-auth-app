from datetime import datetime

def test_get_returns_checked_in_attendance(test_app_with_db):
    date = datetime.now().strftime("%Y-%m-%d")
    response = test_app_with_db.get("/teachers-attendance/checked-in?date={date}".format(date=date))
    assert response.status_code == 200
    assert isinstance(response.json(), object)

def test_get_returns_checked_out_attendance(test_app_with_db):
    date = datetime.now().strftime("%Y-%m-%d")
    response = test_app_with_db.get("/teachers-attendance/checked-out?date={date}".format(date=date))
    assert response.status_code == 200
    assert isinstance(response.json(), object)
