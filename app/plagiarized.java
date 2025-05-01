public class LoopPrinter {
    public void printNumbers(int n) {
        System.out.println("Starting"); // Added logging
        for (int i = 0; i < n; i++) {
            System.out.println(i);
        }
        System.out.println("Done"); // Added logging
    }
}
