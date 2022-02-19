using System;
using System.Collections.Generic;

namespace MarketServerCS
{
    class Market {
        private readonly Dictionary<int, Trader> traders = new Dictionary<int, Trader>();
        private List<int> activeTraders = new List<int>();

        public int CreateTrader(bool stock){
            int clientID = traders.Count + 1;
            int traderID = traders.Count + 101;
            Trader client = new Trader(traderID, clientID);
            client.Stock=stock;
            traders.Add(traderID, client);
            return clientID;
        }

        public void SetActiveTraders(int clientID){
            activeTraders.Add(GetCurrentTraderID(clientID));
        }

        public List<int> GetActiveTraders(){return activeTraders;}

        public void RemoveTrader(int clientID){
            int i = activeTraders.IndexOf(GetCurrentTraderID(clientID));
            activeTraders.RemoveAt(i);
        }

        public int GetCurrentTraderID(int clientID){
            int result = 0;
            lock (traders)
            {
                foreach (Trader client in traders.Values)
                {
                    if (client.ClientID == clientID)
                    {
                        result=client.TraderID;
                    }
                }
            } return result;
        }

        public bool GetStock(int traderID){
            bool stock = false;
            lock (traders)
            {
                foreach (Trader t in traders.Values)
                {
                    if (t.TraderID==traderID)
                    {
                        stock = t.Stock;
                    }
                }
            } return stock;
        }

        public void SetStock(int trader, bool stock){
            lock(traders){
                foreach (Trader t in traders.Values)
                {
                    if (t.TraderID==trader)
                    {
                        t.Stock=stock;
                    }
                }
            }
        }

        public void TransferStock(int clientID, int fromTrader, int toTrader, bool stock){
            lock(traders){
                if (traders[fromTrader].ClientID != clientID){
                    throw new Exception("Trader: " + clientID + " is not allowed to transfer the stock to " + fromTrader + ".");}
                if (!(traders[fromTrader].Stock)){
                    throw new Exception("Trader: " + fromTrader +  " is not the Stock Owner.");
                }
                
            if (activeTraders.Contains(fromTrader) && !(activeTraders.Contains(toTrader))) { //If toTrader is not an active trader
                Console.WriteLine("" + toTrader + " is not online. Stock transfer revoked.");
            } else {
                SetStock(fromTrader, !stock);
                SetStock(toTrader, stock);
            }
            }
        }

        public void SetNewStock(){
            int nextTrader = 0;
            int next = 0;
            if (activeTraders!=null){
                if(activeTraders[next]!=null){
                    nextTrader=activeTraders[next];
                }
                else{
                    foreach (int t in activeTraders)
                    {
                        if(activeTraders[t]!=null){
                            nextTrader=activeTraders[t];
                            break;
                        }
                    }
                }
            }
            lock(traders){
                if (!(traders!.Count==0)){
                    traders[nextTrader].Stock=true;
                    Console.WriteLine("[AUTO] Stock transferred to Trader ID: " + nextTrader);
                }
                else{
                    Console.WriteLine("No Traders to transfer stock to.");
                }
            }
        }
        public void PrintOnlineTraders(){
            int[] tradersOnline = GetActiveTraders().ToArray();
            if (tradersOnline.Length>0){
                Console.WriteLine("Traders Online: ");
                foreach (int t in tradersOnline){
                    if (t!=null)
                    {
                        if (GetStock(t))
                        {
                            Console.WriteLine($"[Online] Trader {t} <- StockOwner");
                        }
                        else
                        {
                            Console.WriteLine($"[Online] Trader {t}");
                        }
                    }
                }
                Console.WriteLine("\n");
            }   
        }
    }
}