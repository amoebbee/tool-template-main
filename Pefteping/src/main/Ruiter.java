package main;

public class Ruiter {
	
	int identifier = 0;
	String name;
	String description;
	boolean active = false;
	boolean turnTaken = false;
	int visitsLeft = 3;
	int stepsLeft = 1000;
	
	

	public Ruiter (int num, String str){
		
		identifier = num;
		name = str;
		
	}

}
