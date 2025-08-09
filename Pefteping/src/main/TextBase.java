package main;

import javax.swing.JButton;

public class TextBase {
	
	
	
	
	public static void setInfoText (){
		
		if (MainFrame.atChar != 0){
			autoInfoText("Converse, take action, annoy.");
			return;
		}
		
	if (World.ruiterSelected == false){		
		if (World.currentNight == 1){
			
				if (World.currentScreen == 0) autoInfoText("Click clock to start.");
				if (World.currentScreen == 1) autoInfoText("Choose a rider.");					
			
				if (World.currentScreen == 0) autoInfoText("Choose a destination.");							
		}
		if (World.currentNight == 2){
			
		}
		if (World.currentNight == 3){
			
		}
		if (World.currentNight == 4){
			
		}
		if (World.currentNight == 5){
			
		}
		if (World.currentNight == 6){
			
		}		
	}		
		if (World.ruiterSelected == true){			
		 autoInfoText(World.currentRuiter.name + "\nChoose a destination \nVisits remaining: "
		+ World.currentRuiter.visitsLeft + "\nSteps remaining:" + World.currentRuiter.stepsLeft);
		 
		 		if (Data.travelling == true){
		 			autoInfoText(World.currentRuiter.name + "\nTravelling \nVisits remaining: "
		 					+ World.currentRuiter.visitsLeft + "\nSteps remaining:" + World.currentRuiter.stepsLeft);
		 		}
				if (Data.destinationReached == true){
					autoInfoText(World.currentRuiter.name + "\nDestination reached. Click it again to visit." +
							"\nVisits remaining: " + World.currentRuiter.visitsLeft + "\nSteps remaining:" + World.currentRuiter.stepsLeft);
					}
		
		
		}		
		
	}
	
	public static void setToonText (){
		
		if (World.currentNight == 1){
			autoToonText("Night 1 text");
		}		
		
	}
	
	public static void autoInfoText (String str){
		MainFrame.infoText.setText(str);		
	}
	public static void autoToonText (String str){
		MainFrame.clockPanel.toonText.setText(str);		
	}
	
	public static String getRuiterText (JButton but){
		
		if (but == MainFrame.clockPanel.butruit1 && MainFrame.clockPanel.butruit1.isEnabled()){
			return "1. Alfus. Heeft geen hoop ooit nog beter te worden maar vindt het hun plicht de parkbewoners te helpen  (moraalridder)";
		}
		if (but == MainFrame.clockPanel.butruit2 && MainFrame.clockPanel.butruit2.isEnabled()){
			return "2. Berfos. Heeft ook weinig hoop maar ziet het nut niet zo van anderen helpen    (depressed)   ";
		}
		if (but == MainFrame.clockPanel.butruit3 && MainFrame.clockPanel.butruit3.isEnabled()){
			return "3. Corfas. Denkt dat ze voor hun goede daden ooit vanzelf beloond zullen worden     (persistent)  ";
		}
		if (but == MainFrame.clockPanel.butruit4 && MainFrame.clockPanel.butruit4.isEnabled()){
			return "4. Durfis.  Denkt dat ze steeds iets over het hoofd zien terwijl ze anderen helpen    (vigilant)   ";
		}
		if (but == MainFrame.clockPanel.butruit5 && MainFrame.clockPanel.butruit5.isEnabled()){
			return "5. Ermes. Ziet meer waarde in chaos dan in het herstellen van orde   (roekeloos)   ";
		}
		if (but == MainFrame.clockPanel.butruit6 && MainFrame.clockPanel.butruit6.isEnabled()){
			return "6. Fons. Ziet overal wel de lol van in, ook het noodlot van hunzelf en anderen    (grapjurk)   ";
		}
		
		return "No Valid Return";
	}
	
	
	
	

}
