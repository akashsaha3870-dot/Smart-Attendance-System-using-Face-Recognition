public class Student {

    private int id;
    private String name;
    private int attendance;

    public Student(int id, String name) {
        this.id = id;
        this.name = name;
        this.attendance = 0;
    }

    public int getId() {
        return id;
    }

    public String getName() {
        return name;
    }

    public int getAttendance() {
        return attendance;
    }

    public void incrementAttendance() {
        attendance++;
    }
}