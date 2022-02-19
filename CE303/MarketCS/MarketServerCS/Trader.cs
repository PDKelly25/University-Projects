namespace MarketServerCS
{
    class Trader {
    public Trader(int traderID, int clientID) {
        TraderID = traderID;
        ClientID = clientID;
    }
    
    public int TraderID {get;}
    public int ClientID {get;}
    public bool Stock {get; set;}
    
    }
}