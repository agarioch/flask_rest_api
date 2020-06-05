# Student search API

Endpoint | Method | Result |
---- | ---- | ---- |
/students | GET | Get list of all students |
/student/{id} | GET | Get student by unique ID |
/student/{id} | POST | Create student with ID and set name |
/student/{id} | PUT | Update student with ID and change name |
/student/{id} | DELETE | Delete student with ID |
/degree{name} | GET | Create degree and associated students by name |
/degree{name} | POST | Create a new degree with the given name |
/degree{name} | DELETE | Delete the degree with the given name |
/degrees | GET | Get list of all degrees and associated students |
/auth | POST | Get authentication key with valid username & password |
/register | POST | Create new user with username & password |