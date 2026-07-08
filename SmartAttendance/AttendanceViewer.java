import java.sql.*;

public class AttendanceViewer {

    public static void main(String[] args) {

        String url = "jdbc:mysql://localhost:3306/smart_attendance";
        String user = "root";
        String password = "akash@2006"; // your password

        try {
            // Load MySQL Driver
            Class.forName("com.mysql.cj.jdbc.Driver");

            // Connect to Database
            Connection con = DriverManager.getConnection(url, user, password);

            System.out.println("Connected to Database ✅");
            System.out.println("----------------------------------");

            // JOIN query (IMPORTANT 🔥)
            String query = "SELECT s.name, a.date, a.time " +
                           "FROM attendance_log a " +
                           "JOIN students s ON a.student_id = s.id";

            Statement stmt = con.createStatement();
            ResultSet rs = stmt.executeQuery(query);

            System.out.println("Attendance Records:");
            System.out.println("----------------------------------");

            // Print with NAME
            while (rs.next()) {
                System.out.println(
                        "Name: " + rs.getString("name") +
                        " | Date: " + rs.getDate("date") +
                        " | Time: " + rs.getTime("time")
                );
            }

            con.close();

        } catch (Exception e) {
            System.out.println("Error: " + e.getMessage());
        }
    }
}