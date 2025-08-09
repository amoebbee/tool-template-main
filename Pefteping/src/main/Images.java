package main;

import java.awt.Image;
import java.awt.Toolkit;

import javax.swing.ImageIcon;

public class Images {
	public static Toolkit toolkit = Toolkit.getDefaultToolkit();
	
	
	public static Image mapimg = toolkit.getImage("map2.png");
	public static Image toonimg = toolkit.getImage("toon.png");
	public static Image ruitersimg = toolkit.getImage("ruiters.png");
	
	public static Image langejanBackgr = toolkit.getImage("langejanbackgr.png");
	public static Image ezeltjeBackgr = toolkit.getImage("ezeltjebackgr.png");
	
	public static Image ruiter1horse = toolkit.getImage("horsered.png");
	public static Image ruiter1horseright = toolkit.getImage("horseredright.png");
	public static Image ruiter1horseleft = toolkit.getImage("horseredleft.png");
	public static Image altruiter1horseright = toolkit.getImage("altredright.png");
	public static Image altruiter1horseleft = toolkit.getImage("altredleft.png");
	
	public static ImageIcon klokicon = new ImageIcon("klok.png");
	public static ImageIcon blipicon = new ImageIcon("blip.png");
	public static ImageIcon blipofficon = new ImageIcon("blipoff.png");
	

}
