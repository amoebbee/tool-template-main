package main;



public class World {
	
	public static int currentNight = 1;
	public static int currentScreen = 0; // 0=mapscreen, 1=ruiterscreen, 2=karakterscreen
	public static boolean ruiterSelected = false;
	public static boolean underWay = false;
	
	public static Ruiter currentRuiter; 
	public static Ruiter    ruiter1= new Ruiter (1 , "Alfus" );     
	public static Ruiter    ruiter2 = new Ruiter (2 , "Berfos" );     
	public static 	Ruiter ruiter3= new Ruiter (3 , "Corfas"); 
	public static Ruiter    ruiter4= new Ruiter (4 , "Durfis");     
	public static Ruiter    ruiter5  = new Ruiter (5 , "Ermes");       
	public static Ruiter    ruiter6  = new Ruiter (6 , "Fons");     
	
	public static Character currentChar;
	public static Character  ezeltje= new Character ();
	public static Character  trol= new Character ();
	public static Character  hansgrietje= new Character ();
	public static Character  langnek= new Character ();
	public static Character  fakir= new Character ();
	public static Character  kabouterdorp= new Character ();
	public static Character  draak= new Character ();
	public static Character  boom= new Character ();
	public static Character  stokjes= new Character ();
	public static Character  repelsteeltje= new Character ();
	
	
	
	
	public World (){

	}

	
	
	
}
