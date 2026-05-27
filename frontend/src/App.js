import React, { useEffect, useState } from "react";
import axios from "axios";

function App() {
  const [employees, setEmployees] = useState([]);
  const [token, setToken] = useState(localStorage.getItem("token") || "");

  // ================= LOGIN =================
  const loginUser = async () => {
    try {
      const res = await axios.post("https://employee-management-portal-6bb4.onrender.com/login", {
        username: "admin",
        password: "1234"
      });

      localStorage.setItem("token", res.data.token);
      setToken(res.data.token);

      alert("Login Successful ✅");
    } catch (err) {
      alert("Login Failed ❌");
    }
  };

  // ================= GET EMPLOYEES =================
  const fetchEmployees = async () => {
    try {
      const res = await axios.get("https://employee-management-portal-6bb4.onrender.com/employees", {
        headers: {
          Authorization: `Bearer ${token}`
        }
      });

      setEmployees(res.data);
    } catch (err) {
      console.log(err);
      alert("Unauthorized / Token missing ❌");
    }
  };

  useEffect(() => {
    if (token) {
      fetchEmployees();
    }
  }, [token]);

  // ================= ADD EMPLOYEE =================
  const addEmployee = async () => {
    try {
      await axios.post(
        "https://employee-management-portal-6bb4.onrender.com/employees",
        {
          name: "Rahul",
          email: "rahul" + Math.random() + "@gmail.com",
          department: "HR",
          salary: 40000
        },
        {
          headers: {
            Authorization: `Bearer ${token}`
          }
        }
      );

      alert("Employee Added ✅");
      fetchEmployees();
    } catch (err) {
      alert("Error adding employee ❌");
    }
  };

  return (
    <div style={{ padding: "20px" }}>
      <h1>Employee Management 🚀</h1>

      {!token ? (
        <button onClick={loginUser}>Login</button>
      ) : (
        <>
          <button onClick={addEmployee}>Add Employee</button>

          <h2>Employees List</h2>
          {employees.map((emp) => (
            <div key={emp.id} style={{ border: "1px solid gray", margin: "10px", padding: "10px" }}>
              <p><b>Name:</b> {emp.name}</p>
              <p><b>Email:</b> {emp.email}</p>
              <p><b>Department:</b> {emp.department}</p>
              <p><b>Salary:</b> {emp.salary}</p>
            </div>
          ))}
        </>
      )}
    </div>
  );
}

export default App;