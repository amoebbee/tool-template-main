package main;

import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;

import javax.sound.sampled.AudioInputStream;
import javax.sound.sampled.AudioSystem;
import javax.sound.sampled.Clip;
import javax.sound.sampled.LineUnavailableException;
import javax.swing.JButton;
import javax.swing.Timer;
import main.MainFrame.IconButton;
import  sun.audio.*;    //import the sun.audio package
import  java.io.*;

public class Data {

	static JButton but;
	static IconButton but2;
	static TravelAnimator travelAnimator = new TravelAnimator();
	static int currentx, currenty, xdone, ydone, targetx, targety, distancedivider, xdistance, ydistance, timerdistance, timercount;
	static boolean travellingRight = false;
	static boolean alternateDraw = false;
	static boolean destinationReached = false;
	static boolean travelling = false;
	static int drawlocx = MainFrame.butklok.xcoord;
	static int drawlocy = MainFrame.butklok.ycoord;
	
	public static int clockActivations = 0;
	public static IconButton currentLocation = MainFrame.butklok;
	public static IconButton currentDestination;
	static Timer horseTimer = new Timer (230, travelAnimator);
	
	static boolean soundUsed = false;
	static File soundFile = new File("clop.wav");	
	static AudioInputStream audioIn;
	static Clip clip;
	
	
	public static void initSound (){
		
		try{
			audioIn = AudioSystem.getAudioInputStream(soundFile);
		}
		catch (Exception e){			
		}
		
			try {
				clip = AudioSystem.getClip();
			} catch (Exception e1) {
				// TODO Auto-generated catch block
				e1.printStackTrace();
				return;
				}
		
	
		
		try {
			clip.open(audioIn);
		} catch (Exception e) {			
			e.printStackTrace();
			return;
		}
		
		soundUsed = true;
		 
		
	}
	
	        
	
	public static class ClockListener implements ActionListener {

		public void actionPerformed(ActionEvent arg0) {
			
			
			if (false){
				MainFrame.switchToChar(4);	
			}
			
			else {
				
				MainFrame.setScreen(1);
				clockActivations++;
				destinationReached = false;
			}
			
		}
	}
	
	public static class RiderButtonListener implements ActionListener {

		public void actionPerformed(ActionEvent arg0) {
			but = (JButton) arg0.getSource();
			
			if (but == MainFrame.clockPanel.butruit1){
				World.currentRuiter = World.ruiter1;
				World.ruiter1.active=true;
				World.ruiter1.turnTaken=true;
				MainFrame.clockPanel.butruit1.setEnabled(false);				
			}
			if (but == MainFrame.clockPanel.butruit2){
				World.currentRuiter = World.ruiter2;
				World.ruiter2.active=true;
				World.ruiter2.turnTaken=true;	
				MainFrame.clockPanel.butruit2.setEnabled(false);
			}
			if (but == MainFrame.clockPanel.butruit3){
				World.currentRuiter = World.ruiter3;
				World.ruiter3.active=true;
				World.ruiter4.turnTaken=true;	
				MainFrame.clockPanel.butruit3.setEnabled(false);
			}
			if (but == MainFrame.clockPanel.butruit4){
				World.currentRuiter = World.ruiter4;
				World.ruiter4.active=true;
				World.ruiter4.turnTaken=true;		
				MainFrame.clockPanel.butruit4.setEnabled(false);
			}
			if (but == MainFrame.clockPanel.butruit5){
				World.currentRuiter = World.ruiter5;
				World.ruiter5.active=true;
				World.ruiter5.turnTaken=true;		
				MainFrame.clockPanel.butruit5.setEnabled(false);
			}
			if (but == MainFrame.clockPanel.butruit6){
				World.currentRuiter = World.ruiter6;
				World.ruiter6.active=true;
				World.ruiter6.turnTaken=true;	
				MainFrame.clockPanel.butruit6.setEnabled(false);
			}
			
			World.ruiterSelected = true;
			TextBase.setInfoText();
			MainFrame.butklok.setEnabled(false);
			MainFrame.onButtons();
			MainFrame.setScreen(0);
			
			
			
		}
		
	}
	
	
	public static class BlipButtonListener implements ActionListener {
		
		public void actionPerformed(ActionEvent e) {
			but2 = (IconButton) e.getSource();		
			destinationReached = false;
			
			
			if (currentLocation == but2){			
				World.currentRuiter.visitsLeft--;
					MainFrame.switchToChar(but2.identifier);				
			}
			
			else{			
			if (soundUsed) clip.loop(Clip.LOOP_CONTINUOUSLY);
			
			xdone = 0;
			ydone = 0;
			timercount = 0;			
			World.underWay = true;
			travelling = true;
			currentDestination = but2;	
        	drawlocx = currentLocation.xcoord;
        	drawlocy = currentLocation.ycoord;
        	currentx = currentLocation.xcoord;
        	currenty = currentLocation.ycoord;
        	targetx = but2.xcoord;
        	targety = but2.ycoord;
            
        	if (currentx > targetx ){
        		if (currenty > targety){
        			distancedivider = 4;
        		}
        		if (currenty< targety){
        			distancedivider = 3;
        		}
        	}
        	else if (currentx < targetx){
        		travellingRight = true;
        		if (currenty > targety){
        			distancedivider = 2;
        		}
        		if (currenty< targety){
        			distancedivider = 1;
        		}
           	}
        	
        	if (distancedivider == 1){
        		xdistance = (but2.xcoord - currentLocation.xcoord);
        		ydistance = (but2.ycoord - currentLocation.ycoord); 
        	}
        	if (distancedivider == 2){
        		xdistance = (but2.xcoord - currentLocation.xcoord);
        		ydistance = (currentLocation.ycoord - but2.ycoord); 
        		
        	}
        	if (distancedivider == 3){
        		xdistance = (currentLocation.xcoord - but2.xcoord);
        		ydistance = (but2.ycoord - currentLocation.ycoord); 

        	}
        	if (distancedivider == 4){
        		xdistance = (currentLocation.xcoord - but2.xcoord);
        		ydistance = (currentLocation.ycoord - but2.ycoord); 

        	}
        	
        	if (xdistance > ydistance) timerdistance = xdistance;
        	if (ydistance > xdistance) timerdistance = ydistance;
			
			
			horseTimer.start();
		
		}
		
		}
	}
	
	public static class TravelAnimator implements ActionListener {

		int b = 13;
		public void actionPerformed(ActionEvent e) {
			
			
			
	           xdone += b;
	           ydone += b;
	           
	           if (distancedivider == 2){
	        	   if (xdistance > xdone){
	       			drawlocx += b;
	        	   }
	        	   if (ydistance > ydone){
	       			drawlocy -= b;
	        	   }
	           }
	           if (distancedivider == 1){
	        	   if (xdistance > xdone){
	        		   drawlocx += b;
	        	   }
	        	   if (ydistance > ydone){
	        		   drawlocy += b;
	        	   }
	           }
	           if (distancedivider == 4){
	        	   if (xdistance > xdone){
	        		   drawlocx -= b;
	        	   }
	        	   if (ydistance > ydone){
	        		   drawlocy -= b;
	        	   }
	           }
	           if (distancedivider ==3){
	        	   if (xdistance > xdone){
	        		   drawlocx -= b;
	        	   }
	        	   if (ydistance > ydone){
	        		   drawlocy += b;
	        	   }
	           }
			
			
	           World.currentRuiter.stepsLeft--;
	           TextBase.setInfoText();
			MainFrame.mainPanel.repaint();
			if (alternateDraw)	alternateDraw = false;
			else if (!alternateDraw) alternateDraw = true;

			timercount += b;
			
			if (timercount >= timerdistance ){ 
				
				if (soundUsed && clip.isRunning()) clip.stop();
				
				travelling = false;
				destinationReached = true;
				currentLocation = currentDestination;
				horseTimer.stop();
				drawlocx=currentLocation.xcoord;
				drawlocy=currentLocation.ycoord;
				
				travellingRight = false;
				World.underWay = false;
				MainFrame.mainPanel.repaint();
				TextBase.setInfoText();
			}
			

			
		}
			
	}
}
