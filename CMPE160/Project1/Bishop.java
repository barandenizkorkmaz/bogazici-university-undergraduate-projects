import java.awt.Color;
import java.awt.Graphics;

public class Bishop extends Piece{
	/*
	public boolean isBlack;
	public abstract void drawYourself(Graphics g, int positionX, int positionY, int squareWidth);
	public abstract boolean canMove(int x, int y);
	public abstract boolean canCapture(int x, int y);
	*/
	
	public Bishop(boolean isBlack){
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
		
		g.fillOval(positionX+(int)(squareWidth*2.0/6.0), 
				positionY+squareWidth/8, 
				squareWidth/3, squareWidth/3);
		
		int[] xPoints={positionX+(int)(squareWidth*1.0/4.0),positionX+(int)(squareWidth*3.0/4.0),positionX+(int)(squareWidth*2.0/4.0)};
		int[] yPoints={positionY+(int)(squareWidth*3.0/5.0),positionY+(int)(squareWidth*3.0/5.0),positionY+(int)(squareWidth*1.0/4.0)};
		
		g.fillPolygon(xPoints, yPoints, 3);
		
		g.fillRect(positionX+(int)(squareWidth*1.0/4.0), 
				positionY+(int)(squareWidth*3.0/5.0), 
				squareWidth/2, squareWidth/5);
		
	}

	@Override
	public boolean canMove(int x, int y,int turn,int selectedSquareY) {
		// TODO Auto-generated method stub
		if(turn%2==1 && isBlack){
			if(x==y || x==-y){
				return true;
				
			}
			else{
				return false;
			}
		}
		else if(turn%2==0 && !(isBlack)){
			if(x==y || x==-y){
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
			if(x==y || x==-y){
				return true;
				
			}
			else{
				return false;
			}
		}
		else if(turn%2==0 && !(isBlack)){
			if(x==y || x==-y){
				return true;
			}
			else{
				return false;
			}
		}
		return false;
	}

}
