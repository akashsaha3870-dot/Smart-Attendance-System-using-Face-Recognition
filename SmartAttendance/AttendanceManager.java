import java.util.ArrayList;

public class AttendanceManager {

    private ArrayList<Student> students = new ArrayList<>();
    private int totalClasses = 0;

    // Add Student
    public void addStudent(Student student) {
        students.add(student);
        System.out.println("Student added: " + student.getName());
    }

    // Find Student by ID
    public Student findStudentById(int id) {
        for (Student s : students) {
            if (s.getId() == id) {
                return s;
            }
        }
        return null;
    }

    // Mark Attendance
    public void markAttendanceById(int id) {
        Student s = findStudentById(id);
        if (s != null) {
            s.incrementAttendance();
            System.out.println("Attendance marked for: " + s.getName());
        } else {
            System.out.println("Student not found!");
        }
    }

    // Increase total classes
    public void increaseClassCount() {
        totalClasses++;
    }

    // Show Report
    public void showReport() {
        System.out.println("\nAttendance Report:");
        System.out.println("------------------------");

        for (Student s : students) {
            double percentage = 0;
            if (totalClasses > 0) {
                percentage = (s.getAttendance() * 100.0) / totalClasses;
            }

            System.out.println(
                "ID: " + s.getId() +
                " | Name: " + s.getName() +
                " | Attendance: " + s.getAttendance() +
                " | %: " + percentage
            );
        }
    }
}