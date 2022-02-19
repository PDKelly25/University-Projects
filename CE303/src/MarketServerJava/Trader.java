package MarketServerJava;

public class Trader {
    private int traderID;
    private int clientID;
    private boolean stock;
    public Trader(int traderID, int clientID){ this.traderID=traderID; this.clientID = clientID; }

    public int getTraderID(){ return traderID; }

    public int getClientID(){ return clientID; }

    public boolean getStock(){ return stock; }

    public void setStock(boolean stock){ this.stock=stock; }


}
