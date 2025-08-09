package main;

import java.awt.Color;
import java.awt.Graphics;
import java.awt.Image;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.awt.event.ItemEvent;
import java.awt.event.ItemListener;
import java.awt.event.KeyEvent;
import java.awt.event.KeyListener;


import javax.swing.ButtonGroup;
import javax.swing.JButton;
import javax.swing.JLabel;
import javax.swing.JPanel;
import javax.swing.JRadioButton;
import javax.swing.JScrollPane;
import javax.swing.JTextArea;
import javax.swing.JTextField;

public class CharScreen extends JPanel implements ItemListener, KeyListener, ActionListener {
	
	Color backcolor = new Color (246,220,117);
	JScrollPane charScroll;
	TextArea charText = new TextArea ();
	JTextField playerText = new JTextField ();
	TextArea validText = new TextArea ();
	TextArea thirdText = new TextArea ();
	Image backgroundImg;
	JLabel conv = new JLabel ("Conversation options:");
	int identifier;
	
	JButton exitButton = new JButton ("Exit Encounter");
	JButton thirdButton = new JButton ("Some Button");
	JButton butaction1 = new JButton ("ActionButton 1");
	JButton butaction2 = new JButton ("ActionButton 2");
	JButton butaction3 = new JButton ("ActionButton 3");
	JRadioButton but1 = new JRadioButton("Say something clever");
	JRadioButton but2 = new JRadioButton("Say something stupid");
	JRadioButton but3 = new JRadioButton("Say something offensive");
	JRadioButton but4 = new JRadioButton("Enter custom text");
	ButtonGroup butgroup = new ButtonGroup();
	JButton validButton = new JButton ("Test Validity");
	JButton enterButton = new JButton ("Enter Chosen Option");
	JRadioButton radiobutholder;
	JButton butholder;
	String validHolder;
	String charHolder;
	
	public CharScreen (int num){
		
		identifier = num;
		thirdText.setText("Additional info");
		MainFrame.charScreenList.add(this);
		setLayout(null);
		setBackground (backcolor);
		charScroll = new JScrollPane (charText);
		charScroll.setBounds(1,302,995,120);
		playerText.setBorder(MainFrame.border);
		conv.setBackground(null);
		conv.setBounds(10, 460, 220, 20);
		exitButton.setBounds (814 ,636  , 170, 24);
		thirdButton.setBounds (781 ,145  , 170, 24);
		butaction1.setBounds (35 ,430  , 280, 24);
		butaction2.setBounds (355, 430 , 280, 24);
		butaction3.setBounds (675, 430 , 280, 24);
		butgroup.add(but1);
		butgroup.add(but2);
		butgroup.add(but3);
		butgroup.add(but4);
		but1.setBounds (5,480  , 400, 20);
		but2.setBounds (5, 501 , 400, 20);
		but3.setBounds (5, 522 , 400, 20);
		but4.setBounds (5, 543 , 400, 20);
		but1.setBackground(null);
		but2.setBackground(null);
		but3.setBackground(null);
		but4.setBackground(null);
		playerText.setBounds (9, 568, 490, 24);
		validText.setBounds (9, 599, 639, 24);
		thirdText.setBounds (521, 175, 430, 110);
		validButton.setBounds (507, 568, 140,24);
		enterButton.setBounds (9, 636, 170,24);
		but1.addItemListener(this);
		but2.addItemListener(this);
		but3.addItemListener(this);
		but4.addItemListener(this);
		playerText.addKeyListener(this);
		validButton.addActionListener(this);
		thirdButton.addActionListener(this);
		enterButton.addActionListener(this);
		exitButton.addActionListener(this);
		
		this.add(conv);
		this.add(butaction1);
		this.add(butaction2);
		this.add(butaction3);
		this.add(but1);this.add(but2);
		this.add(but3);this.add(but4);
		this.add(charScroll);
		this.add(playerText);
		this.add(validButton);
		this.add(validText);
		this.add(thirdText);
		this.add(enterButton);
		this.add(thirdButton);
		this.add(exitButton);
		
		
		
		initPanel();
		
	}
		
	public void paintComponent (Graphics g){
		super.paintComponent(g);
		g.drawImage(backgroundImg, 2, 1, this);
	}

	
	public void resetDefault(){
		
		this.add(MainFrame.infoText);
		TextBase.setInfoText();
		thirdButton.setEnabled(false);
		playerText.setEnabled(false);
		validButton.setEnabled(false);
		enterButton.setEnabled(false);
		butgroup.clearSelection();
		validText.setText("");
		playerText.setText("");
		charText.setText("");
	}
	
	public void actionPerformed(ActionEvent e) {
		butholder = (JButton) e.getSource();
		if (butholder == validButton){
			validHolder = null;
			charHolder = null;
			ConvText.getOutput(this, playerText.getText());
			validButton.setEnabled(false);
			playerText.setText("");
			playerText.requestFocus();
			validText.setText(validHolder);
			if (charHolder != null) enterButton.setEnabled (true);
			else enterButton.setEnabled (false);
		}
		if (butholder == enterButton){
			if (but4.isSelected()){
				charText.setText(charHolder);
				
			}		
			
			butgroup.clearSelection();
			enterButton.setEnabled(false);
			validText.setText("");
			playerText.setEnabled(false);
			
				
		}
		if (butholder == thirdButton){
			
		}
		if (butholder == exitButton){
			MainFrame.setScreen(0);
			
		}

	}
	
	public void itemStateChanged(ItemEvent arg0) {
		radiobutholder = (JRadioButton) arg0.getSource();
		
		if (radiobutholder != but4){
			playerText.setEnabled(false);
			validText.setText("");
			validButton.setEnabled(false);
			enterButton.setEnabled(true);
			
		}
		if (radiobutholder == but4){
			playerText.setEnabled(true);
			if (!playerText.getText().equals("")){
				validButton.setEnabled(true);
			}
			enterButton.setEnabled(false);
			
		}
		
	}
	public void keyPressed(KeyEvent e) {
		
		if (e.getKeyCode() == 10 && !playerText.getText().equals("")){
			validButton.doClick();
			
		}
		else if (playerText.getText().equals("")){
			validButton.setEnabled(false);
		}
		else {			
			validButton.setEnabled(true);
		}
	
	}
	public void keyReleased(KeyEvent e) {
		


	}
	public void keyTyped(KeyEvent e) {
	}
	
	   public static class TextArea extends JTextArea {
		   
		   public TextArea (){
			   
			   this.setEditable (false);
				this.setBorder(MainFrame.border);
				this.setLineWrap(true);
				this.setWrapStyleWord(true);
				setFocusable(false);
		   }
		   
		   public TextArea (String str){
				this.setText(str);
				this.setBorder(MainFrame.border);
				this.setLineWrap(true);
				this.setWrapStyleWord(true);
				setFocusable(false);
			}
		}

	   
	   public  void initPanel(){
		   
		   if (identifier == 1){
				backgroundImg = Images.ezeltjeBackgr;
				World.currentChar = World.ezeltje;
		   }
		   if (identifier == 4){
				backgroundImg = Images.langejanBackgr;
				World.currentChar = World.langnek;
		   }
		   
	   }


}
