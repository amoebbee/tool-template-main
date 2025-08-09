package main;

public class ConvText {
		static CharScreen scrholder;
		static int count;
	
	public static void noQuestion (String str){
		MyString sub = new MyString (str);
		
		if (sub.has("like") && (sub.has("poop") || sub.has("poo"))) 
			set("I like poop", "That is a bit vile");
		if (sub.hasOrder("you", "stupid"))
			set("I think you are stupid", "Well so are you");		
		 if (sub.hasOrder("you", "not", "stupid")) 
			set("I think you are not stupid", "Well that's your opinion");
				
		 
		set("No valid return for your statement", null);
	}
	
	
	public static void yesQuestion (String str){
		MyString sub = new MyString (str);
		
		if (sub.has("you") && sub.has("like") && (sub.has("poop") || sub.has("poo"))) 
			set("Do you like poop?", "Sometimes I do");

		
		set("No valid return for your question", null);
	}


	
	public static void getOutput (CharScreen scr, String str){	
		count = 0;
		scrholder = scr;
		if (findQuestion(str)) yesQuestion(str);			
		else  noQuestion (str);
	}	
	public static void set (String str1, String str2){
		if (str2 != null){
		scrholder.validHolder = str1;
		scrholder.charHolder = str2;
		}
		else if (str2 == null && count == 0){
		scrholder.validHolder = str1;
		scrholder.charHolder = str2;
		}
		count++;
		
	}
	public static boolean findQuestion (String str){
		return (str.indexOf("?") >= 0);
	}	
	static class MyString{
	    public String mystr;
	    public MyString(String str){
	        this.mystr = str;
	    }
		public boolean has (String str){
			return mystr.indexOf(str) >= 0;								
		}
		public boolean hasOrder (String str1, String str2){
			if (mystr.indexOf(str1) >= 0 && mystr.indexOf(str2) >= mystr.indexOf(str1))	return true;
			return false;							
		}
		public boolean hasOrder (String str1, String str2, String str3){
			if (mystr.indexOf(str1) >= 0 && mystr.indexOf(str2) >= mystr.indexOf(str1) && mystr.indexOf(str3) >= mystr.indexOf(str2))	return true;
			return false;							
		}
		public boolean hasOrder (String str1, String str2, String str3, String str4){
			return false;							
		}
		public boolean hasOrder (String str1, String str2, String str3, String str4, String str5){
			return false;							
		}
	}
}
