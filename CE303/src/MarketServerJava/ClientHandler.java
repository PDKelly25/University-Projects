package MarketServerJava;

import java.io.PrintWriter;
import java.net.Socket;
import java.util.List;
import java.util.Scanner;

public class ClientHandler implements Runnable {
    private final Socket socket;
    private Market market;
//    static boolean offline = false;

    public ClientHandler(Socket socket, Market market) {
        this.socket = socket;
        this.market = market;
    }

    @Override
    public void run() {

        int clientID = 0;
        int traderID;

//        offline = false;
        try (
                Scanner scanner = new Scanner(socket.getInputStream());
                PrintWriter writer = new PrintWriter(socket.getOutputStream(), true)) {
            try {
                clientID = market.createTrader(false);
                traderID = market.getCurrentTraderID(clientID);
                writer.println("SUCCESS");
                writer.println(clientID);
                String online = scanner.nextLine();
                if (online.strip().compareToIgnoreCase("online") == 0) {market.setActiveTraders(clientID);}

                if (market.getActiveTraders().size()==1) {
                    market.setstock(traderID, true);
                    System.out.println("A Trader has connected. Client ID: " + clientID + ", Trader ID: " + traderID + " is Stock Owner");
                }
                else {
                    if (market.getstock(traderID)){
                        market.setstock(traderID, true);
                        System.out.println("A Trader has connected. Client ID: " + clientID + ", Trader ID: " + traderID + " is Stock Owner");
                    }
                    else {
                        market.setstock(traderID, false);
                        System.out.println("A Trader has connected. Client ID: " + clientID + ", Trader ID: " + traderID + " is not Stock Owner.");

                    }
                }
                market.printOnlineTraders();

                while (true) {
                    String line = scanner.nextLine();
                    String[] substrings = line.split(" ");
                    switch (substrings[0].toLowerCase()) {
                        case "online":
                            int client = Integer.parseInt(substrings[1]);
                            market.setActiveTraders(client);
                            break;

                        case "trader":
                            int client_id = Integer.parseInt(substrings[1]);
                            writer.println(market.getCurrentTraderID(client_id));
                            break;

                        case "traders":
                            List<Integer> traders = market.getActiveTraders();
                            writer.println(traders.size());
                            for (Integer t : traders)
                                writer.println(t);
                            break;

                        case "stock":
                            int trader = Integer.parseInt(substrings[1]);
                            writer.println(market.getstock(trader));
                            break;

                        case "transfer":
                            int fromTrader = Integer.parseInt(substrings[1]);
                            int toTrader = Integer.parseInt(substrings[2]);
                            boolean s = Boolean.valueOf(substrings[3]); //stock
                            market.transferStock(clientID, fromTrader, toTrader, s);
                            writer.println("SUCCESS");
                            if (market.getstock(toTrader))
                                System.out.println("Trader ID: "+ fromTrader +" has transferred Stock to Trader ID: " + toTrader);
                            break;

                        default:
                            throw new Exception("Unknown command: " + substrings[0]);
                    }
                }
            } catch (Exception e) {
                writer.println(e.getMessage());
                socket.close();
            }
        } catch (Exception e) {
        } finally {
//            if (!offline) {
                try {
                    traderID = market.getCurrentTraderID(clientID);
                    if (market.getstock(traderID)) {
                        System.out.println("\nA Trader has left the market. \nClient ID: " + clientID + ", Trader ID: " + traderID + " was Stock Owner.\n");
                        try {
                            market.removeTrader(clientID);
                        } catch (Exception e) {
                            System.out.println(e);
                        }
                        market.setNewstock(); //assign a new trader to give it to

                    } else {
                        System.out.println("\nA Trader has left the market. \nClient ID: " + clientID + ", Trader ID: " + traderID + " was not Stock Owner.\n");
//                        market.removeTrader(clientID);
                        try {
                            market.removeTrader(clientID);
                        } catch (Exception e) {
                        }
                    }
                    market.printOnlineTraders();
                } catch (Exception exception) {}
//            }
        }
    }
}