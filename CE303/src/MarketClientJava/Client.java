package MarketClientJava;
import java.io.PrintWriter;
import java.net.Socket;
import java.util.Scanner;

public class Client implements AutoCloseable{
    final int port = 9000;

    private final Scanner reader;
    private final PrintWriter writer;
    private int clientID;

    public Client() throws Exception {
        Socket socket = new Socket("localhost", port);
        reader = new Scanner(socket.getInputStream());
        writer = new PrintWriter(socket.getOutputStream(), true);

        String line = reader.nextLine();

        if (line.trim().compareToIgnoreCase("success") != 0) throw new Exception(line);

        clientID = Integer.parseInt(reader.nextLine());
    }

    public void isActive(){
        writer.println("ONLINE");
    }

    public int getClientID(){
        return clientID;
    }

    public int getTraderID(int clientID) {
        // Sending command
        writer.println("TRADER " + clientID);

        // Reading the number of traders
        String line = reader.nextLine();
        int traderID = Integer.parseInt(line);

        return traderID;
    }

    public int[] getTraders() {
        writer.println("TRADERS");

        String line = reader.nextLine();
        int tradersOnline = Integer.parseInt(line);

        int[] traders = new int[tradersOnline];
        for (int t = 0; t < tradersOnline; t++) {
            line = reader.nextLine();
            traders[t] = Integer.parseInt(line);
        }

        return traders;
    }

    public boolean getStock(int traderID) {
        writer.println("STOCK " + traderID);

        String line = reader.nextLine();
        return Boolean.parseBoolean(line);
    }

    public void transferStock(int fromTrader, int toTrader, boolean stock) throws Exception {
        writer.println("TRANSFER " + fromTrader + " " + toTrader + " " + stock);

        String line = reader.nextLine();
        if (line.trim().compareToIgnoreCase("success") != 0)
            throw new Exception(line);
    }

    @Override
    public void close() throws Exception {
        reader.close();
        writer.close();
    }
}
