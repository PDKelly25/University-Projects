using System;
using System.Collections.Generic;
using System.IO;
using System.Threading;

namespace MarketClientCS
{
    class ClientProgram
    {
        static void Main(string[] args)
        {
            int clientID;
            try
            {
                using (Client client = new Client())
                {
                    clientID = client.GetClientID();
                    Console.WriteLine("Status: Connected with Client ID: " + clientID);
                    client.IsActive();

                    while (true)
                    {
                        int traderID = client.GetTraderID(clientID);
                        int[] traders = client.GetTraders(); //activeTraders List
                        int fromTrader;
                        int toTrader;

                        foreach (int t in traders)
                        {
                            if (client.GetStock(t)){
                                Console.WriteLine($"[Online] Trader {t} <- StockOwner");
                            }
                            else
                            {
                                Console.WriteLine($"[Online] Trader {t}");
                            }
                        }
                        if (client.GetStock(traderID)) {
                            Console.WriteLine($"Trader {traderID}: You are the Stock Owner.");
                            fromTrader = traderID;

                            Console.WriteLine("Press <Enter Button> to update online traders. \nOr press 't' to Transfer stock to available traders.");
                            string next = Console.ReadLine().Trim().ToLower();

                            if (next.Equals("t")) {
                                Console.WriteLine("Enter the Trader ID of who you want to transfer the stock to. \nYou can also transfer to yourself");
                                toTrader = int.Parse(Console.ReadLine());
                                client.TransferStock(fromTrader, toTrader, client.GetStock(traderID));
                            }

                            else {
                                if (next.Equals("")) {}//do nothing, run loop again
                                else
                                    throw new Exception("Unknown command " + next);
                            }
                        }
                        else {
                            Console.WriteLine($"Trader {traderID}: You are not the Stock Owner.");
                            Console.WriteLine("Waiting for Stock transfer...");
                            Console.WriteLine("Press <Enter Button> to update online traders, and to check the Stock Status");
                            string next = Console.ReadLine().Trim();
                            if (client.GetStock(traderID)){next.Equals(""); continue;} //if transferred stock, run loop again
                            if (next.Equals("")) {} //do nothing - runs loop again, printing trader list
                            else {
                                throw new Exception("Unknown command " + next);
                            }
                        }
                    }
                }
            } catch (Exception e){
                Console.WriteLine(e.Message);
            }
        }
    }
}