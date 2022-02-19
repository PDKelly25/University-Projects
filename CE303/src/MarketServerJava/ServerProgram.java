package MarketServerJava;
import java.io.*;
import java.net.ServerSocket;
import java.net.Socket;

public class ServerProgram implements Serializable
{
    private static final int port = 9000;

    private static Market market = new Market();

    public static void main(String[] args) throws FileNotFoundException, IOException, ClassNotFoundException {
//        market = deserialise("market.txt");
        RunServer();
    }

//    public static void serialise(Market market, String filename) {
//        try {
//            ObjectOutputStream out = new ObjectOutputStream((new FileOutputStream(filename)));
//            out.writeObject(market);
//            System.out.println("Serialisation successful.");
//        } catch (IOException e) {
//            e.printStackTrace();
//        }
//    }
//
//    public static Market deserialise(String filename) {
//        try {
//            ObjectInputStream in = new ObjectInputStream(new FileInputStream(filename));
//            market = (Market) in.readObject();
//            System.out.println("De-serialisation successful.");
//        } catch (IOException e) {
//            e.printStackTrace();
//        } catch (ClassNotFoundException e) {
//            e.printStackTrace();
//        }
//        return market;
//    }

    private static void RunServer() throws IOException, ClassNotFoundException{
        ServerSocket serverSocket = null;
        try {
            serverSocket = new ServerSocket(port);
            System.out.println("Waiting for incoming connections...");
            while (true) {
                Socket socket = serverSocket.accept();
                new Thread(new ClientHandler(socket, market)).start();
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
//        finally {
//            try{
//            serialise(market, "market.txt");
//            } catch (Exception e){}
//        }
    }
}

