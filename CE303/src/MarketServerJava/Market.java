package MarketServerJava;
import javax.lang.model.type.ArrayType;
import java.util.*;


public class Market {
    private static final Map<Integer, Trader> traders = new TreeMap<>();
    //changes made
    private static List<Integer> activeTraders = new ArrayList<>();
// end
    public int createTrader(boolean stock)
    {
        int clientID = traders.size()+1; //first client created = client id: 1  -   increments each time trader created
        int traderID = traders.size()+101; //first trader id: 101  -    increments each time
        Trader client = new Trader(traderID, clientID);
        client.setStock(stock); //set to false initially
        traders.put(traderID, client); //added to map to store both IDs
        return clientID;
    }
//changes made
    public void setActiveTraders(int clientID){
        activeTraders.add(getCurrentTraderID(clientID));
        } //adds the client who calls this method to list stating client is online (Trader is Active)

    public List<Integer> getActiveTraders(){
        return activeTraders;
    } //returns list of online clients

    public void removeTrader(int clientID){
        int i = activeTraders.indexOf(getCurrentTraderID(clientID));
        activeTraders.remove(i);
    }

    public int getCurrentTraderID(int clientID){
        int result = 0;
        synchronized (traders) {
            for (Trader client : traders.values()) {
                if (client.getClientID() == clientID)
                    result = client.getTraderID();
            }
        }
        return result;
    }

    public boolean getstock(int traderID) {
        boolean stock=false;
        synchronized (traders) {
            for (Trader t : traders.values())
                if (t.getTraderID()==traderID) //if trader is online
                    stock = t.getStock();
        }
        return stock;
    }

    public void setstock(int trader, boolean stock) throws Exception {
        synchronized (traders) {
            for (Trader t : traders.values())
                if (t.getTraderID()==trader)
                    t.setStock(stock);
        }
    }

    public void transferStock(int clientID, int fromTrader, int toTrader, boolean stock) throws Exception {
        synchronized (traders)
        {
            if (traders.get(fromTrader).getClientID() != clientID)
                throw new Exception("Trader: " + clientID + " is not allowed to transfer the stock to " + fromTrader + ".");
            if (!(traders.get(fromTrader).getStock()))
                throw new Exception("Trader: " + fromTrader +  " is not the Stock Owner.");

            if (activeTraders.contains(fromTrader) && !(activeTraders.contains(toTrader))) { //If toTrader is not an active trader
                System.out.println("" + toTrader + " is not online. Stock transfer revoked.");
            } else {
                setstock(fromTrader, !stock);
                setstock(toTrader, stock);
            }
        }
    }

    public void setNewstock() { //pick trader from those available - next one who joined in succession.
        int nextTrader = 0; //TraderIDs start at 100, cannot be 0.
        int next = 0;

        if (activeTraders!=null) {
            if(activeTraders.get(next)!=null) nextTrader=activeTraders.get(next); //next Trader in list [longest time connected]
            else {
                for (int t : activeTraders) {
                    if (activeTraders.get(t) != null){
                        nextTrader = activeTraders.get(t);
                        break;
                    }
                }
            }
//            Iterator<Integer> it = activeTraders.iterator();
//            while (it.hasNext()) {
//                if (nextTrader != 0) { //breaks loop straight away once nextTrader is obtained
//                    break;
//                }
//                if (it == null) {
//                }//do nothing, go through loop again
//                else {
//                    nextTrader = it.next();
//                }
            }
            synchronized (traders) {
                if (!(traders.isEmpty())) {
                    traders.get(nextTrader).setStock(true);
                    System.out.println("\n[AUTO] Stock transferred to Trader ID: " + nextTrader);
                }
                else {
                    System.out.println("\nNo Traders to transfer stock to.");
                }
            }
        }

    public void printOnlineTraders(){
        Object[] tradersOnline = getActiveTraders().toArray();
        if (tradersOnline.length>0) {
            System.out.println("Traders Online: ");
            for (Object t : tradersOnline) {
                if (t != null) {
                    if (getstock((Integer) t)){
                        System.out.printf("[Online] Trader %2d <- StockOwner.\n", t);
                    }
                    else {
                        System.out.printf("[Online] Trader %2d\n", t);
                    }
                }
            } System.out.println("\n");
        }
    }
}
//    public boolean existingTrader(int traderID){
//        for (Trader trader : traders) {
//            if (traderID != trader.getTraderID()) return false;
//        } return true;
//    }

//    public boolean CheckStockStatus(int traderID){
//
//    }



