import java.awt.Color;
import java.awt.Graphics;

public class Knight extends Piece{
	/*
	public boolean isBlack;
	public abstract void drawYourself(Graphics g, int positionX, int positionY, int squareWidth);
	public abstract boolean canMove(int x, int y);
	public abstract boolean canCapture(int x, int y);
	*/
	
	public Knight(boolean isBlack){
		super(isBlack);
	}
	
	public void drawYourself(Graphics g, int positionX, int positionY, int squareWidth) {
		// TODO Auto-generated method stub
		
		
		if(isBlack)
		{
			g.setColor(Color.black);
		}
		else
		{
			g.setColor(Color.white);
		}
		
		int[] xPoints={positionX+(int)(squareWidth*6.0/12.0),positionX+(int)(squareWidth*4.0/12.0),positionX+(int)(squareWidth*9.0/12.0)};
		int[] yPoints={positionY+(int)(squareWidth*1.0/12.0),positionY+(int)(squareWidth*5.0/12.0),positionY+(int)(squareWidth*5.0/12.0)};
		
		g.fillPolygon(xPoints, yPoints, 3);
		
		g.fillRect(positionX+(int)(squareWidth*5.0/12.0), 
				positionY+squareWidth/4, 
				squareWidth/6, squareWidth/2);
		g.fillRect(positionX+(int)(squareWidth*1.0/4.0), 
				positionY+(int)(squareWidth*3.0/5.0), 
				squareWidth/2, squareWidth/5);
		
	}

	@Override
	public boolean canMove(int x, int y,int turn,int selectedSquareY) {
		// TODO Auto-generated method stub
		if(turn%2==1 && isBlack){
			if(((x==1 || x==-1) && (y==2 || y==-2))||((x==2 || x==-2) && (y==1 || y==-1))){
				return true;
				
			}
			else{
				return false;
			}
		}
		else if(turn%2==0 && !(isBlack)){
			if(((x==1 || x==-1) && (y==2 || y==-2))||((x==2 || x==-2) && (y==1 || y==-1))){
				return true;
			}
			else{
				return false;
			}
		}
		return false;
		
	}

	@Override
	public boolean canCapture(int x, int y,int turn) {
		// TODO Auto-generated method stub
		if(turn%2==1 && isBlack){
			if(((x==1 || x==-1) && (y==2 || y==-2))||((x==2 || x==-2) && (y==1 || y==-1))){
				return true;
				
			}
			else{
				return false;
			}
		}
		else if(turn%2==0 && !(isBlack)){
			if(((x==1 || x==-1) && (y==2 || y==-2))||((x==2 || x==-2) && (y==1 || y==-1))){
				return true;
			}
			else{
				return false;
			}
		}
		return false;
		
	}

}
