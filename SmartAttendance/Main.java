import java.util.Scanner;

public class Main {

    public static void main(String[] args) {

        Scanner sc = new Scanner(System.in);

        while (true) {

            System.out.println("\n===== SMART ATTENDANCE SYSTEM =====");
            System.out.println("1. Add Student");
            System.out.println("2. Mark Attendance");
            System.out.println("3. Show Report");
            System.out.println("4. Exit");
            System.out.print("Enter choice: ");

            int choice = sc.nextInt();

            switch (choice) {

                case 1:
                    System.out.print("Enter Student ID: ");
                    int id = sc.nextInt();
                    sc.nextLine();
                    System.out.print("Enter Student Name: ");
                    String name = sc.nextLine();

                    DatabaseConnection.insertStudent(id, name);
                    break;

                case 2:
                    System.out.print("Enter Student ID: ");
                    int sid = sc.nextInt();
                    DatabaseConnection.markAttendance(sid);
                    break;

                case 3:
                    DatabaseConnection.showReport();
                    break;

                case 4:
                    System.out.println("Exiting...");
                    sc.close();
                    return;

                default:
                    System.out.println("Invalid choice!");
            }
        }
    }
}