package atcapi;
package atcapi.model;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

public class autoScaling {
  //set up two LinkedLists holding internal workers and external workers
  DirectorClient client = new SpringDirectorClientBuilder();
  ATC atc = new ATC(); 
  
  public static boolean scaleUp(){
    boolean scaledUp = false
    int external_workers_added = 0
    int index = 0;
    //load and place each concourse internal worker in LinkedList
    for { //each individual internal worker in LinkedList 
      if { //check if workers have over CPU usage (in either percent or raw memory)
        //run yml file to spin up external worker
        scaledUp = true;
        external_workers_added += 1;
      }
      if(external_workers_added > 8){
        break;
      }
    }
    return scaledUp;
  }
  public static boolean scaleDown(){
    boolean scaledDown = false
    //feed in time value
    double time = //fed time 
      if (scaledUp){
      for { //iterating over external workers LinkedList
        if(time < 100 && time > 40 && worker.cpuUsage < 200){ //these are arbitrary values needed to be determined by looking at grafana
          //set individual external worker in landing state
          if{ //worker is landed
            //retire worker
            if{ //worker is retired
              //bosh kill external worker
            }
          }
        }
      }
      scaledDown = true;
    }
    return scaledDown;
  }
  
  public static void main(String args[])
  {
    
    
          
