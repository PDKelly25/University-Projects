using System;
using System.IO;
using System.Net;
using System.Net.Sockets;
using System.Threading;
using System.Collections.Generic;

namespace MarketServerCS
{
    class ServerProgram
    {
        private const int port = 9000;
        private static Market market = new Market();

        static void Main(string[] args)
        {
            RunServer();
        }

        private static void RunServer()
        {
            //Setup connection
            TcpListener listener = new TcpListener(IPAddress.Loopback, port);
            listener.Start();
            Console.WriteLine("Waiting for incoming connections...");
            while (true)
            {
                TcpClient tcpClient = listener.AcceptTcpClient();
                new Thread(HandleClient).Start(tcpClient);
            }
        }

        private static void HandleClient(object param)
        {
            TcpClient tcpClient = (TcpClient) param;
            using (Stream stream = tcpClient.GetStream())
            {
                StreamWriter writer = new StreamWriter(stream);
                StreamReader reader = new StreamReader(stream);
                int clientID=0;
                int traderID;

                try
                {
                    clientID = market.CreateTrader(false);
                    traderID = market.GetCurrentTraderID(clientID);
                    writer.WriteLine("SUCCESS");
                    writer.WriteLine(clientID);
                    writer.Flush();
                    string online = reader.ReadLine();

                    if (online.Trim().ToLower()=="online"){market.SetActiveTraders(clientID);}
                    
                    if (market.GetActiveTraders().Count==1){
                        market.SetStock(traderID, true);
                        Console.WriteLine($"A Trader has connected. Client ID: {clientID}, Trader ID: {traderID} is Stock Owner\n");
                    }
                    else {
                        if (market.GetStock(traderID)){
                            market.SetStock(traderID, true);
                            Console.WriteLine($"A Trader has connected. Client ID: {clientID}, Trader ID: {traderID} is Stock Owner\n");
                        }
                        else {
                            market.SetStock(traderID, false);
                            Console.WriteLine($"A Trader has connected. Client ID: {clientID}, Trader ID: {traderID} is not Stock Owner\n");
                        }
                    }
                    market.PrintOnlineTraders();
                    
                    while(true){
                        string line = reader.ReadLine();
                        string[] substrings = line.Split(' ');
                        switch (substrings[0].ToLower()) 
                        {
                            case "online":
                                int client = int.Parse(substrings[1]);
                                market.SetActiveTraders(client);
                                break;

                            case "trader":
                                int client_id = int.Parse(substrings[1]);
                                writer.WriteLine(market.GetCurrentTraderID(client_id));
                                writer.Flush();
                                break;

                            case "traders":
                                List<int> traders = market.GetActiveTraders();
                                writer.WriteLine(traders.Count);
                                foreach (int t in traders)
                                    writer.WriteLine(t);
                                writer.Flush();
                                break;

                            case "stock":
                                int trader = int.Parse(substrings[1]);
                                writer.WriteLine(market.GetStock(trader));
                                writer.Flush();
                                break;

                            case "transfer":
                                int fromTrader = int.Parse(substrings[1]);
                                int toTrader = int.Parse(substrings[2]);
                                bool s = Boolean.Parse(substrings[3]); //stock
                                market.TransferStock(clientID, fromTrader, toTrader, s);
                                writer.WriteLine("SUCCESS");
                                writer.Flush();
                                if (market.GetStock(toTrader))
                                    Console.WriteLine($"Trader ID: {fromTrader} has transferred Stock to Trader ID: {toTrader}\n");
                                break;

                            default:
                                throw new Exception("Unknown command: " + substrings[0]);
                        }
                    }
                } catch (Exception e)
                {
                    try
                    {
                        writer.WriteLine("ERROR " + e.Message);
                        writer.Flush();
                        tcpClient.Close();
                    }
                    catch(Exception exception)
                    {
                    }
                }
                finally
                {
                    try{
                        traderID = market.GetCurrentTraderID(clientID);
                        if (market.GetStock(traderID)){
                            Console.WriteLine($"A Trader has left the market. \nClientID: {clientID}, Trader ID: {traderID}\n");
                            
                            try {
                                market.RemoveTrader(clientID);
                            } catch (Exception e) {Console.WriteLine(e);}
                            market.SetNewStock();
                        } 
                        else 
                        {
                            Console.WriteLine($"A Trader has left the market. \nClientID: {clientID}, Trader ID: {traderID}\n");
                            try{
                                market.RemoveTrader(clientID);
                            } catch (Exception e){}
                        } 
                        market.PrintOnlineTraders();
                    } catch (Exception exception) {}
                }
            }
        }
    }
}