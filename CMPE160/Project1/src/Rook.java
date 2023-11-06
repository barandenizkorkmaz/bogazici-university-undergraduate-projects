import java.awt.Color;
import java.awt.Graphics;

public class Rook extends Piece{
	/*
	public boolean isBlack;
	public abstract void drawYourself(Graphics g, int positionX, int positionY, int squareWidth);
	public abstract boolean canMove(int x, int y);
	public abstract boolean canCapture(int x, int y);
	*/
	
	public Rook(boolean isBlack){
		super(isBlack);
	}
	/*
	 * pieces[i][j].drawYourself(g, i*SQUARE_WIDTH+BOARD_MARGIN, 
							j*SQUARE_WIDTH+BOARD_MARGIN, SQUARE_WIDTH);
	 */
	
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
		g.fillRect(positionX+(int)(squareWidth*1.0/4.0), 
				positionY+(int)(squareWidth/5.0), 
				squareWidth/8, squareWidth/2);
		
		g.fillRect(positionX+(int)(squareWidth*2.5/4.0), 
				positionY+(int)(squareWidth/5.0), 
				squareWidth/8, squareWidth/2);
		
		g.fillRect(positionX+(int)(squareWidth*1.0/4.0), 
				positionY+(int)(squareWidth*1.8/5.0), 
				squareWidth/2, (int)(squareWidth/2.0));
		
	}
	
	public boolean canMove(int x, int y,int turn,int selectedSquareY) {
		// TODO Auto-generated method stub
		if(turn%2==1 && isBlack){
			if(x==0 || y==0){
				return true;
				
			}
			else{
				return false;
			}
		}
		else if(turn%2==0 && !(isBlack)){
			if(x==0 || y==0){
				return true;
			}
			else{
				return false;
			}
		}
		return false;
		
	}

	public boolean canCapture(int x, int y,int turn) {
		// TODO Auto-generated method stub
		if(turn%2==1 && isBlack){
			if(x==0 || y==0){
				return true;
				
			}
			else{
				return false;
			}
		}
		else if(turn%2==0 && !(isBlack)){
			if(x==0 || y==0){
				return true;
			}
			else{
				return false;
			}
		}
		return false;
	}

}
