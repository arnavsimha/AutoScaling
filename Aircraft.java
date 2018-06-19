package atcapi.model;

public class Aircraft {


    private long acId;
    private AircraftType type;
    private AircraftSize size;

    public Aircraft(long acId, AircraftType type, AircraftSize size){
        this.acId = acId;
        this.type = type;
        this.size = size;
    }

    public long getAcId(){ return acId; }

    public AircraftType getType() {
        return type;
    }

    public AircraftSize getSize() {
        return size;
    }

    public String toString(){
        return "Type: " + this.getType() + ", Size: " + this.getSize();
    }
}
