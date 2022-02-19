package MarketClientJava;

import java.util.Scanner;

public class ClientProgram {

    public static void main(String[] args) {
        int clientID;
            try {
                Scanner in = new Scanner(System.in); //user input

                try (Client client = new Client()) {
                    clientID = client.getClientID();
                    System.out.printf("Status: Connected with Client ID:%2d", clientID);
                    client.isActive();

                    while (true) {

                        int traderID = client.getTraderID(clientID);
                        int[] traders = client.getTraders(); //activeTraders List
                        int fromTrader;
                        int toTrader;

                        for (int t : traders) {
                            if (client.getStock(t)) {
                                System.out.printf("\n[Online] Trader %2d <- StockOwner.", t);
                            } else {
                                System.out.printf("\n[Online] Trader %2d", t);
                            }
                        }

                        if (client.getStock(traderID)) {
                            System.out.printf("\nTrader %2d: You are the Stock Owner.\n", traderID);
                            fromTrader = traderID;

                            System.out.println("\nPress <Enter Button> to update online traders. \nOr press 't' to Transfer stock to available traders.");
                            String next = in.nextLine().trim().toLowerCase();

                            if (next.equals("t")) {
                                System.out.println("\nEnter the Trader ID of who you want to transfer the stock to. \nYou can also transfer to yourself");
                                toTrader = Integer.parseInt(in.nextLine());
                                client.transferStock(fromTrader, toTrader, client.getStock(traderID));
                            }

                            else {
                                if (next.equals("")) {}//do nothing, run loop again
                                else
                                    throw new Exception("Unknown command " + next);
                            }
                        }
                        else {
                            System.out.printf("\nTrader %2d: You are not the Stock Owner.\n", traderID);
                            System.out.println("\nWaiting for Stock transfer...");
                            System.out.println("\nPress <Enter Button> to update online traders, and to check the Stock Status");
                            String next = in.nextLine().trim();
                            if (client.getStock(traderID)){next.equals(""); continue;} //if transferred stock, run loop again
                            if (next.equals("")) {} //do nothing - runs loop again, printing trader list
                            else {
                                throw new Exception("Unknown command " + next);
                            }

                        }
                    }
                }
            } catch (Exception e) {
                System.out.println(e.getMessage());
            }
        }
    }

