import java.awt.Color;
import java.awt.Graphics;

public class King extends Piece{
	/*
	public boolean isBlack;
	public abstract void drawYourself(Graphics g, int positionX, int positionY, int squareWidth);
	public abstract boolean canMove(int x, int y);
	public abstract boolean canCapture(int x, int y);
	*/

    public King(boolean isBlack){
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

        g.drawLine(positionX+(int)(squareWidth*5.0/12.0), positionY+(int)(squareWidth*1.8/12.0), positionX+(int)(squareWidth*7.0/12.0), positionY+(int)(squareWidth*1.8/12.0));
        g.drawLine(positionX+(int)(squareWidth*1.0/2.0), positionY+(int)(squareWidth*2.0/6.0), positionX+(int)(squareWidth*1.0/2.0), positionY);



        g.fillOval(positionX+(int)(squareWidth*2/6.0),
                positionY+(int)(squareWidth*1.5/6.0),
                squareWidth/3, squareWidth/3);


        int[] xPoints={positionX+(int)(squareWidth*1.0/2.0),positionX+(int)(squareWidth*1.0/4.0),positionX+(int)(squareWidth*3.0/4.0)};
        int[] yPoints={positionY+(int)(squareWidth*1.0/2.0),positionY+(int)(squareWidth*5.0/6.0),positionY+(int)(squareWidth*5.0/6.0)};

        g.fillPolygon(xPoints, yPoints, 3);

    }

    @Override
    public boolean canMove(int x, int y,int turn,int selectedSquareY) {
        // TODO Auto-generated method stub
        if(turn%2==1 && isBlack){
            if(((x == -1 || x == 1) && (y == -1 || y==1)) || ((x==0) && (y==1 || y==-1) || (y==0) && (x==1 || x==-1))){
                return true;

            }
            else{
                return false;
            }
        }
        else if(turn%2==0 && !(isBlack)){
            if(((x == -1 || x == 1) && (y == -1 || y==1)) || ((x==0) && (y==1 || y==-1) || (y==0) && (x==1 || x==-1))){
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
            if(((x == -1 || x == 1) && (y == -1 || y==1)) || ((x==0) && (y==1 || y==-1) || (y==0) && (x==1 || x==-1))){
                return true;

            }
            else{
                return false;
            }
        }
        else if(turn%2==0 && !(isBlack)){
            if(((x == -1 || x == 1) && (y == -1 || y==1)) || ((x==0) && (y==1 || y==-1) || (y==0) && (x==1 || x==-1))){
                return true;
            }
            else{
                return false;
            }
        }
        return false;
    }

}
