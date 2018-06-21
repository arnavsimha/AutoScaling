import java.io.*;
import java.util.*;
import org.ho.yaml.*;

public class YAMLTest {
      //loading Yaml file
      try {
			  File f = new File("yml/mydata.yml");
			  Object mydata = Yaml.load(f);
			  System.out.println(mydata);
		    }
		catch (FileNotFoundException e) {
			  System.out.println("Not found!");
		}
