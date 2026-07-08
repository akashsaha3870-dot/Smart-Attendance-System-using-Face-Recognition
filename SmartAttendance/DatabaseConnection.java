import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.SQLException;
import java.sql.PreparedStatement;
import java.sql.ResultSet;

public class DatabaseConnection {

    private static final String URL = "jdbc:mysql://localhost:3306/smart_attendance";
    private static final String USER = "root";
    private static final String PASSWORD = "akash@2006";

    public static Connection getConnection() {
        try {
            Class.forName("com.mysql.cj.jdbc.Driver");
            return DriverManager.getConnection(URL, USER, PASSWORD);
        } catch (Exception e) {
            System.out.println("Database connection failed!");
            e.printStackTrace();
        }
        return null;
    }

    // Insert Student
    public static void insertStudent(int id, String name) {
        String query = "INSERT INTO students (id, name) VALUES (?, ?)";

        try (Connection conn = getConnection();
             PreparedStatement ps = conn.prepareStatement(query)) {

            ps.setInt(1, id);
            ps.setString(2, name);
            ps.executeUpdate();

            System.out.println("Student added to database!");

        } catch (SQLException e) {
            System.out.println("Insert failed!");
            e.printStackTrace();
        }
    }

    // Mark Attendance
    public static void markAttendance(int studentId) {

        String updateCount = "UPDATE students SET attendance_count = attendance_count + 1 WHERE id = ?";
        String insertLog = "INSERT INTO attendance_log (student_id, date, time) VALUES (?, CURDATE(), CURTIME())";

        try (Connection conn = getConnection()) {

            PreparedStatement ps1 = conn.prepareStatement(updateCount);
            ps1.setInt(1, studentId);
            ps1.executeUpdate();

            PreparedStatement ps2 = conn.prepareStatement(insertLog);
            ps2.setInt(1, studentId);
            ps2.executeUpdate();

            System.out.println("Attendance marked in database!");

        } catch (SQLException e) {
            System.out.println("Attendance marking failed!");
            e.printStackTrace();
        }
    }

    // Show Report
    public static void showReport() {

        String query = "SELECT * FROM students";

        try (Connection conn = getConnection();
             PreparedStatement ps = conn.prepareStatement(query);
             ResultSet rs = ps.executeQuery()) {

            System.out.println("\n===== STUDENT REPORT =====");

            while (rs.next()) {
                System.out.println("ID: " + rs.getInt("id"));
                System.out.println("Name: " + rs.getString("name"));
                System.out.println("Total Attendance: " + rs.getInt("attendance_count"));
                System.out.println("-------------------------");
            }

        } catch (SQLException e) {
            System.out.println("Report fetch failed!");
            e.printStackTrace();
        }
    }
}