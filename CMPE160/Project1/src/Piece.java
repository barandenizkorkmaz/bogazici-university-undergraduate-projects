import java.awt.Graphics;

public abstract class Piece {
	public boolean isBlack;
	public abstract void drawYourself(Graphics g, int positionX, int positionY, int squareWidth);
	public abstract boolean canMove(int x, int y,int turn,int selectedSquareY);
	public abstract boolean canCapture(int x, int y,int turn);
	
	public Piece(boolean isBlack){
		this.isBlack=isBlack;
	}
	
}
