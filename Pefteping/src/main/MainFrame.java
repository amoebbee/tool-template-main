package main;

import java.awt.CardLayout;
import java.awt.Color;
import java.awt.Graphics;
import java.awt.Toolkit;
import java.awt.event.ActionListener;
import java.awt.event.MouseEvent;
import java.awt.event.MouseListener;
import java.awt.event.MouseMotionListener;
import java.awt.event.WindowAdapter;
import java.awt.event.WindowEvent;
import java.util.ArrayList;

import javax.swing.BorderFactory;
import javax.swing.ImageIcon;
import javax.swing.JButton;
import javax.swing.JFrame;
import javax.swing.JPanel;
import javax.swing.JTextArea;
import javax.swing.border.Border;


import main.Data.*;


public class MainFrame {
	
	public static Toolkit toolkit = Toolkit.getDefaultToolkit();
	static JFrame window = new JFrame("Monsiarmeur");	
	
	static Border border = BorderFactory.createEtchedBorder();
	static TextArea infoText = new TextArea();
	public static int atChar = 0;
	static BlipButtonListener blipButList = new BlipButtonListener ();	

	World world = new World ();	
	Images images = new Images ();
	static CardLayout cl1 = new CardLayout();
	static JPanel underPanel = new JPanel ();		
	static MainPanel mainPanel = new MainPanel ();	
	static ClockPanel clockPanel = new ClockPanel ();
	
	
	static ArrayList <IconButton> buttonList = new ArrayList  <IconButton> ();
	static ArrayList <CharScreen> charScreenList = new ArrayList  <CharScreen> ();
	
	static IconButton butklok = new IconButton (Images.klokicon, 0, 406, 275);
	static IconButton butezeltje = new IconButton (Images.blipicon, 1 ,748,280);
	static IconButton buttrol = new IconButton (Images.blipicon, 2, 749, 162);
	static IconButton buthansgrietje = new IconButton (Images.blipicon, 3, 534, 154);
	static IconButton butlangnek = new IconButton (Images.blipicon, 4, 283, 121);
	static IconButton butfakir = new IconButton (Images.blipicon, 5, 366, 547);
	static IconButton butkabouterdorp = new IconButton (Images.blipicon, 6, 160, 181);
	static IconButton butdraak = new IconButton (Images.blipicon, 7, 470, 110);
	static IconButton butsprookjesboom = new IconButton (Images.blipicon, 8, 623, 596);
	static IconButton butzwavelstokjes = new IconButton (Images.blipicon, 9, 831, 421);
	static IconButton butrepelsteeltje = new IconButton (Images.blipicon, 10, 337, 395);
	
	static CharScreen langejanPanel = new CharScreen (1);
	static CharScreen ezeltjePanel = new CharScreen (4);
	
	
	   
	   
	static boolean buttonsActive = false;
	

	
	   public static void main(String[] args) {
		      
		   Data.initSound ();   	      
		   
		   infoText.setText("Click on the clock to start.");
		      window.setSize(1000,700);
		      window.setResizable(false);
		      window.setLocation(0,0);		      
		      window.setLayout (null);    
 
		      underPanel.setLayout (cl1);
		      underPanel.setBounds (0,0,1000,700);
		      
		      underPanel.add(mainPanel, "0");
		      underPanel.add(clockPanel, "1");
		      underPanel.add(langejanPanel, "2");
		      underPanel.add(ezeltjePanel, "5");
			   cl1.show(underPanel, "" + (0));

		      initButtons ();
		      window.add(underPanel);
		      window.addWindowListener(new WindowAdapter(){
		    	  public void windowClosing(WindowEvent e){
		    	   System.exit(0);
		    	  }
		    	   });
		      
		      window.requestFocus() ;
		      window.setVisible(true);
		 

		   }
	   
	   
	   public static class MainPanel extends JPanel implements MouseListener {
		   
			int xcoord;
			int ycoord;	
			int drawx;
			int drawy;
			TextArea coords;	
			
		   
		   public MainPanel (){	
			   
			  this.setBounds (0,0,1000,700);
			  this.setLayout(null);				  
			  coords = new TextArea();
				coords.setBounds(0,0,59,18);
				this.add(coords);
				infoText.setBounds(694,0,300,98);
				infoText.setBackground (Color.pink);
				this.add(infoText);
				this.addMouseListener(this);			   
		   }
		   
	   public void paintComponent (Graphics g){			   
			   g.drawImage(Images.mapimg,0 ,0, this);
			   
			   if (World.ruiterSelected == true && World.underWay == false){
				   g.drawImage(Images.ruiter1horse, Data.drawlocx , Data.drawlocy, this);				   
			   }
			   
			   if (Data.travellingRight == false){
				   
				   if (World.ruiterSelected == true && World.underWay == true && Data.alternateDraw == false)					   
					   g.drawImage(Images.ruiter1horseright, Data.drawlocx ,Data.drawlocy, this);	   
					   
				   
				   if (World.ruiterSelected == true && World.underWay == true && Data.alternateDraw == true)					   
					   g.drawImage(Images.ruiter1horseleft, Data.drawlocx ,Data.drawlocy, this);	   
				   
			   }
			   
			   if (Data.travellingRight == true){
				   
				   if (World.ruiterSelected == true && World.underWay == true && Data.alternateDraw == false)					   
					   g.drawImage(Images.altruiter1horseright, Data.drawlocx ,Data.drawlocy, this);	   

				   if (World.ruiterSelected == true && World.underWay == true && Data.alternateDraw == true){
					   g.drawImage(Images.altruiter1horseleft, Data.drawlocx ,Data.drawlocy, this);	   
					   
				   }				  
				   
			   }
	
		   }
		   
		public void mouseClicked(MouseEvent arg0) {
		}
		public void mouseEntered(MouseEvent arg0) {
		}
		public void mouseExited(MouseEvent arg0) {
		}
		public void mousePressed(MouseEvent arg0) {
			xcoord = arg0.getX();
			ycoord = arg0.getY();
			coords.setText(xcoord + "  " + ycoord);			
		}
		public void mouseReleased(MouseEvent arg0) {			
		}	   
		
	   }
	   
	   public static class ClockPanel extends JPanel implements MouseMotionListener {
		   
		   TextArea toonText = new TextArea ("Slimme Toon.");
		   TextArea ruiterText = new TextArea ("Ruiter Info.");
		   RiderButtonListener riderButList = new RiderButtonListener ();
		   
		   JButton butruit1  = new JButton ("Select Ruiter 1");
		   JButton butruit2  = new JButton ("Select Ruiter 2");
		   JButton butruit3  = new JButton ("Select Ruiter 3");
		   JButton butruit4  = new JButton ("Select Ruiter 4");
		   JButton butruit5  = new JButton ("Select Ruiter 5");
		   JButton butruit6  = new JButton ("Select Ruiter 6");
		   
		   public ClockPanel  (){
			   
			   setLayout (null);
			   setBounds (0,0,1000,700);
			   setBackground (Color.blue);
			   
			   toonText.setBounds(300,0,300,98);
				this.add(toonText);
				ruiterText.setBounds(495,310,475,74);
				
				ruiterText.setFocusable(false);
				
					this.add(ruiterText);
				
				butruit1.setBounds ( 20 , 310 ,  130, 26);
				butruit2.setBounds ( 20 , 358 ,  130, 26);
				butruit3.setBounds ( 180 , 310 ,  130, 26);
				butruit4.setBounds ( 180 , 358 ,  130, 26);
				butruit5.setBounds ( 340 , 310 ,  130, 26);
				butruit6.setBounds ( 340 , 358 ,  130, 26);
				
				butruit1.addMouseMotionListener(this);
				butruit2.addMouseMotionListener(this);
				butruit3.addMouseMotionListener(this);
				butruit4.addMouseMotionListener(this);
				butruit5.addMouseMotionListener(this);
				butruit6.addMouseMotionListener(this);
				butruit1.addActionListener(riderButList);
				butruit2.addActionListener(riderButList);
				butruit3.addActionListener(riderButList);
				butruit4.addActionListener(riderButList);
				butruit5.addActionListener(riderButList);
				butruit6.addActionListener(riderButList);
				
				

				this.add(butruit1);
				this.add(butruit2);
				this.add(butruit3);
				this.add(butruit4);
				this.add(butruit5);
				this.add(butruit6);
			   
		   }
		   
		   public void paintComponent (Graphics g){			   
			  
			   super.paintComponent(g);
			   g.drawImage(Images.toonimg,0 ,0, this);
			   g.drawImage(Images.ruitersimg, 0 ,409, this);
		   }		   
			public void mouseDragged(MouseEvent arg0) {

			}
			public void mouseMoved(MouseEvent arg0) {
				ruiterText.setText(TextBase.getRuiterText( (JButton) arg0.getSource()));
			}
			


		  
	   }
	   
	   public static void setScreen (int num){
		   atChar = 0;
		   if (num == 0){
				MainFrame.mainPanel.add(MainFrame.infoText);
				MainFrame.cl1.show(MainFrame.underPanel, "" + (0));
				World.currentScreen = 0; 
				TextBase.setInfoText();			   
		   }
		   if (num == 1){	
				MainFrame.clockPanel.add(MainFrame.infoText);
				MainFrame.cl1.show(MainFrame.underPanel, "" + (1));
				World.currentScreen = 1; 
				TextBase.setInfoText();
				TextBase.setToonText();	
		   }		   
	   }
	   
	   public static void switchToChar (int id){
		   atChar = id;
		   
		   for (Object scr : charScreenList){
			   CharScreen pu = (CharScreen) scr;
			   if (atChar == pu.identifier) pu.resetDefault();
		   }
		   if (id == 1){
				MainFrame.cl1.show(MainFrame.underPanel, "" + (2));	   
		   }
		   if (id == 4){	
				MainFrame.cl1.show(MainFrame.underPanel, "" + (5));
		   }		   
	   }
	   
	   public static void initButtons (){
		   
		  butklok.setBounds (452,203,41,98);
		   butezeltje.setBounds (730,307,31,31);
		   buttrol.setBounds (731,189,31,31);
		   buthansgrietje.setBounds (516,181,31,31);
		   butlangnek.setBounds (265,148,31,31);
		   butfakir.setBounds (348,574,31,31);
		   butkabouterdorp.setBounds (142 , 208,31,31);
		   butdraak.setBounds ( 452,137 ,31,31);
		   butsprookjesboom.setBounds ( 605, 623,31,31);
		   butzwavelstokjes.setBounds (813 , 448,31,31);
		   butrepelsteeltje.setBounds ( 319,422 ,31,31);
		   
			for( ActionListener al :  butklok.getActionListeners() ) {
				butklok.removeActionListener( al );}
		   butklok.addActionListener (new Data.ClockListener());
		   buttonList.remove(butklok);
		   
		   offButtons ();
	   }
	   
	   public static void offButtons (){
		   
		   for (Object obj : buttonList){
			   IconButton but = (IconButton) obj;
			   
			   but.setIcon (Images.blipofficon);
			   
			   
			for( ActionListener al :  but.getActionListeners() ) {
					 but.removeActionListener( al );}			   
		   }
		   
	   }
	   
	   public static void onButtons () {
		   
		   for (Object obj : buttonList){
			   IconButton but = (IconButton) obj;
			   
			   but.setIcon (Images.blipicon);
			   but.addActionListener (blipButList);
		   }
	   }
	   
	   public static class IconButton extends JButton {
			
		   int identifier = 0;
		   int xcoord;
		   int ycoord;
			
			public IconButton (ImageIcon img, int num){
				
				identifier = num;
				setIcon (img);				
				setBorderPainted(false);
				setFocusPainted(false);
				setContentAreaFilled(false);
				setRolloverEnabled(false);
				mainPanel.add(this);
				buttonList.add(this);
				
				addActionListener (blipButList);
			}
			public IconButton (ImageIcon img, int num, int x, int y){
				
				xcoord=x;
				ycoord=y;
				identifier = num;
				setIcon (img);				
				setBorderPainted(false);
				setFocusPainted(false);
				setContentAreaFilled(false);
				setRolloverEnabled(false);
				mainPanel.add(this);
				buttonList.add(this);
				
				addActionListener (blipButList);
			}
		}
	   
	   public static class TextArea extends JTextArea {
		   
		   public TextArea (){
			   
			   this.setEditable (false);
				this.setBorder(border);
				this.setLineWrap(true);
				this.setWrapStyleWord(true);
				setFocusable(false);
		   }
		   
		   public TextArea (String str){
				this.setText(str);
				this.setBorder(border);
				this.setLineWrap(true);
				this.setWrapStyleWord(true);
				setFocusable(false);
			}
		}
		   
}

