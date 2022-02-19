using System;
using System.IO;
using System.Net.Sockets;

namespace MarketClientCS
{
    class Client: IDisposable
    {
        const int port = 9000;
        private readonly StreamReader reader;
        private readonly StreamWriter writer;
        private int clientID;
        
        public Client(){
        
            TcpClient tcpClient = new TcpClient("localhost", port);
            NetworkStream stream = tcpClient.GetStream();
            reader = new StreamReader(stream);
            writer = new StreamWriter(stream);

            //Read response
            string line = reader.ReadLine();
            if (line.Trim().ToLower()!="success"){
                throw new Exception(line);
            }
            clientID = int.Parse(reader.ReadLine());          
            }

        public void IsActive(){
            writer.WriteLine("ONLINE");
            writer.Flush();
        }

        public int GetClientID(){
            return clientID;
        }

        public int GetTraderID(int clientID) {
            // Sending command
            writer.WriteLine("TRADER " + clientID);
            writer.Flush();

            // Reading the number of traders
            string line = reader.ReadLine();
            int traderID = int.Parse(line);

            return traderID;
        }

        public int[] GetTraders()
        {
            //Write command
            writer.WriteLine("TRADERS");
            writer.Flush();

            string line = reader.ReadLine();
            int tradersOnline = int.Parse(line);

            int[] traders = new int[tradersOnline];
            for (int i = 0; i < tradersOnline; i++)
            {
                line = reader.ReadLine();
                traders[i] = int.Parse(line);
            }

            return traders;
        }

        public bool GetStock(int traderID) {
            writer.WriteLine("STOCK " + traderID);
            writer.Flush();

            string line = reader.ReadLine();
            return bool.Parse(line);
        }

        public void TransferStock(int fromTrader, int toTrader, bool stock){
            writer.WriteLine("TRANSFER " + fromTrader + " " + toTrader + " " + stock);
            writer.Flush();

            string line = reader.ReadLine();
            if (line.Trim().ToLower() != "success"){
                throw new Exception(line);
            }
        }


        public void Dispose()
        {
            reader.Close();
            writer.Close();
        }
        }
    }
