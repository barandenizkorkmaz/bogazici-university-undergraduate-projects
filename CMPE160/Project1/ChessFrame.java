import java.awt.Graphics;
import java.awt.event.MouseEvent;
import java.awt.event.MouseListener;

import javax.swing.JFrame;

public class ChessFrame extends JFrame implements MouseListener{
    public static final int SQUARE_WIDTH = 45;
    public static final int BOARD_MARGIN = 50;
    int selectedSquareX = -1;
    int selectedSquareY = -1;
    Piece pieces[][] = new Piece[8][8];
    public int turn;

    public ChessFrame()
    {
        initializeChessBoard();
        setTitle("Chess Game");
        //let the screen size fit the board size
        setSize(SQUARE_WIDTH*8+BOARD_MARGIN*2, SQUARE_WIDTH*8+BOARD_MARGIN*2);
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        addMouseListener(this);

    }

    public void initializeChessBoard()
    {
        for(int i = 0; i<8; i++)
        {
            for(int j = 0; j<8; j++)
            {
                if(j == 1)
                {
                    pieces[i][j] = new Pawn(true);
                }
                else if(j == 6)
                {
                    pieces[i][j] = new Pawn(false);
                }
                else
                {
                    pieces[i][j] = null;
                }
            }
        }

        for(int i = 0; i<8; i++)
        {
            for(int j = 0; j<8; j++)
            {
                if(j==0 && (i==0 || i==7)){
                    pieces[i][j] = new Rook(true);
                }
                else if(j==7 && (i==0 || i==7))
                {
                    pieces[i][j] = new Rook(false);
                }

            }
        }

        for(int i = 0; i<8; i++)
        {
            for(int j = 0; j<8; j++)
            {
                if(j==0 && (i==1 || i==6)){
                    pieces[i][j] = new Knight(true);
                }
                else if(j==7 && (i==1 || i==6))
                {
                    pieces[i][j] = new Knight(false);
                }

            }
        }

        for(int i = 0; i<8; i++)
        {
            for(int j = 0; j<8; j++)
            {
                if(j==0 && (i==2 || i==5)){
                    pieces[i][j] = new Bishop(true);
                }
                else if(j==7 && (i==2 || i==5))
                {
                    pieces[i][j] = new Bishop(false);
                }

            }
        }

        for(int i = 0; i<8; i++)
        {
            for(int j = 0; j<8; j++)
            {
                if(j==0 && (i==3)){
                    pieces[i][j] = new Queen(true);
                }
                else if(j==7 && (i==3))
                {
                    pieces[i][j] = new Queen(false);
                }

            }
        }

        for(int i = 0; i<8; i++)
        {
            for(int j = 0; j<8; j++)
            {
                if(j==0 && (i==4)){
                    pieces[i][j] = new King(true);
                }
                else if(j==7 && (i==4))
                {
                    pieces[i][j] = new King(false);
                }

            }
        }
    }

    @Override
    public void paint(Graphics g) {
        // TODO Auto-generated method stub
        super.paint(g);
        //print the board 's lines to show squares
        for(int i = 0; i<=8; i++)
        {
            g.drawLine(BOARD_MARGIN,
                    BOARD_MARGIN+(i)*SQUARE_WIDTH,
                    BOARD_MARGIN+8*SQUARE_WIDTH,
                    BOARD_MARGIN+(i)*SQUARE_WIDTH);
            g.drawLine(BOARD_MARGIN+(i)*SQUARE_WIDTH,
                    BOARD_MARGIN,
                    BOARD_MARGIN+(i)*SQUARE_WIDTH,
                    BOARD_MARGIN+8*SQUARE_WIDTH);
        }
        //print the pieces
        for(int i = 0; i<8; i++)
        {
            for(int j = 0; j<8; j++)
            {
                if(pieces[i][j] != null)
                {
                    pieces[i][j].drawYourself(g, i*SQUARE_WIDTH+BOARD_MARGIN,
                            j*SQUARE_WIDTH+BOARD_MARGIN, SQUARE_WIDTH);
                }
            }
        }
    }
    @Override
    public void mouseClicked(MouseEvent e) {
        // TODO Auto-generated method stub
        //System.out.println("Clicked");

    }
    @Override
    public void mousePressed(MouseEvent e) {
        // TODO Auto-generated method stub
        //System.out.println("Pressed");
        //calculate which square is selected
        selectedSquareX = (e.getX()-BOARD_MARGIN)/SQUARE_WIDTH;
        selectedSquareY = (e.getY()-BOARD_MARGIN)/SQUARE_WIDTH;
        System.out.println(selectedSquareX+","+selectedSquareY);
    }
    @Override
    public void mouseReleased(MouseEvent e) {
        // TODO Auto-generated method stub
        //System.out.println("Released");
        //calculate which square is targeted
        int targetSquareX = (e.getX()-BOARD_MARGIN)/SQUARE_WIDTH;
        int targetSquareY = (e.getY()-BOARD_MARGIN)/SQUARE_WIDTH;
        System.out.println(targetSquareX+","+targetSquareY+"\n");

        //if these are inside the board
        if(selectedSquareX >= 0 && selectedSquareY >= 0 &&
                selectedSquareX < 8 && selectedSquareY < 8 &&
                targetSquareX >= 0 && targetSquareY >= 0 &&
                targetSquareX < 8 && targetSquareY < 8)
        {
            System.out.println("inside");
            if(pieces[selectedSquareX][selectedSquareY] != null)
            {
                System.out.println("selected");
                int diffX = targetSquareX - selectedSquareX;
                int diffY = targetSquareY - selectedSquareY;
                if(pieces[targetSquareX][targetSquareY] != null)
                {
                    System.out.println("a target");
                    if(pieces[selectedSquareX][selectedSquareY] instanceof Pawn && pieces[selectedSquareX][selectedSquareY].isBlack!=pieces[targetSquareX][targetSquareY].isBlack && pieces[selectedSquareX][selectedSquareY].canCapture(diffX, diffY,turn))
                    {
                        System.out.println("can capture");
                        pieces[targetSquareX][targetSquareY] =
                                pieces[selectedSquareX][selectedSquareY];
                        pieces[selectedSquareX][selectedSquareY] = null;
                        turn++;
                    }
                    else if(!(pieces[selectedSquareX][selectedSquareY] instanceof Pawn) && pieces[selectedSquareX][selectedSquareY].isBlack!=pieces[targetSquareX][targetSquareY].isBlack && pieces[selectedSquareX][selectedSquareY].canCapture(diffX, diffY,turn) && jumpChecker(pieces[selectedSquareX][selectedSquareY],targetSquareX,targetSquareY,selectedSquareX,selectedSquareY))
                    {
                        System.out.println("can capture");
                        pieces[targetSquareX][targetSquareY] =
                                pieces[selectedSquareX][selectedSquareY];
                        pieces[selectedSquareX][selectedSquareY] = null;
                        turn++;
                    }

                }
                else
                {
                    System.out.println("no target");
                    if(pieces[selectedSquareX][selectedSquareY] instanceof Pawn && pieces[selectedSquareX][selectedSquareY].canMove(diffX, diffY,turn,selectedSquareY) && jumpChecker(pieces[selectedSquareX][selectedSquareY],targetSquareX,targetSquareY,selectedSquareX,selectedSquareY)){
                        System.out.println("can move");
                        pieces[targetSquareX][targetSquareY] =
                                pieces[selectedSquareX][selectedSquareY];
                        pieces[selectedSquareX][selectedSquareY] = null;
                        turn++;
                    }
                    else if(!(pieces[selectedSquareX][selectedSquareY] instanceof Pawn) && pieces[selectedSquareX][selectedSquareY].canMove(diffX, diffY,turn,selectedSquareY) && jumpChecker(pieces[selectedSquareX][selectedSquareY],targetSquareX,targetSquareY,selectedSquareX,selectedSquareY))
                    {
                        System.out.println("can move");
                        pieces[targetSquareX][targetSquareY] =
                                pieces[selectedSquareX][selectedSquareY];
                        pieces[selectedSquareX][selectedSquareY] = null;
                        turn++;

                    }
                }

            }
        }

        repaint();
    }
    @Override
    public void mouseEntered(MouseEvent e) {
        // TODO Auto-generated method stub
        //System.out.println("Entered");

    }
    @Override
    public void mouseExited(MouseEvent e) {
        // TODO Auto-generated method stub
        //System.out.println("Exited");

    }

    public boolean jumpChecker(Piece p,int targetSquareX,int targetSquareY,int selectedSquareX,int selectedSquareY){
        if(p instanceof Pawn){
            if(pieces[selectedSquareX][selectedSquareY].isBlack){
                if(pieces[selectedSquareX][selectedSquareY+1]!=null)
                    return false;
            }
            if(!pieces[selectedSquareX][selectedSquareY].isBlack){
                if(pieces[selectedSquareX][selectedSquareY-1]!=null)
                    return false;
            }
        }

        else if(p instanceof Rook){
            if(selectedSquareX==targetSquareX){
                if(selectedSquareY<targetSquareY){
                    for(int i=selectedSquareY+1;i<targetSquareY;i++){
                        if(pieces[selectedSquareX][i]!=null)
                            return false;
                    }
                }
                else{
                    for(int i=selectedSquareY-1;i>targetSquareY;i--){
                        if(pieces[selectedSquareX][i]!=null)
                            return false;
                    }
                }
            }
            else if(selectedSquareY==targetSquareY){
                if(selectedSquareX<targetSquareX){
                    for(int i=selectedSquareX+1;i<targetSquareX;i++){
                        if(pieces[i][selectedSquareY]!=null)
                            return false;
                    }
                }
                else{
                    for(int i=selectedSquareX-1;i>targetSquareX;i--){
                        if(pieces[i][selectedSquareY]!=null)
                            return false;
                    }
                }
            }
        }

        else if(p instanceof Bishop){
            if(selectedSquareX<targetSquareX){
                if(selectedSquareY<targetSquareY){
                    for(int i=1;i<targetSquareY-selectedSquareY;i++){
                        if(pieces[selectedSquareX+i][selectedSquareY+i]!=null)
                            return false;
                    }
                }
                else{
                    for(int i=1;i<selectedSquareY-targetSquareY;i++){
                        if(pieces[selectedSquareX+i][selectedSquareY-i]!=null)
                            return false;
                    }
                }
            }
            else{
                if(selectedSquareY<targetSquareY){
                    for(int i=1;i<targetSquareY-selectedSquareY;i++){
                        if(pieces[selectedSquareX-i][selectedSquareY+i]!=null)
                            return false;
                    }
                }
                else{
                    for(int i=1;i<selectedSquareY-targetSquareY;i++){
                        if(pieces[selectedSquareX-i][selectedSquareY-i]!=null)
                            return false;
                    }
                }
            }
        }
        else if(p instanceof Queen){
            if((selectedSquareX==targetSquareX || selectedSquareY==targetSquareY)){
                if(!rookChecker(p,targetSquareX,targetSquareY,selectedSquareX,selectedSquareY)){
                    return false;
                }
                else{
                    return true;
                }
            }
            else{
                if(!bishopChecker(p,targetSquareX,targetSquareY,selectedSquareX,selectedSquareY)){
                    return false;
                }
                else{
                    return true;
                }
            }
        }


        return true;
    }

    public boolean rookChecker(Piece p,int targetSquareX,int targetSquareY,int selectedSquareX,int selectedSquareY){
        if(selectedSquareX==targetSquareX){
            if(selectedSquareY<targetSquareY){
                for(int i=selectedSquareY+1;i<targetSquareY;i++){
                    if(pieces[selectedSquareX][i]!=null)
                        return false;
                }
            }
            else{
                for(int i=selectedSquareY-1;i>targetSquareY;i--){
                    if(pieces[selectedSquareX][i]!=null)
                        return false;
                }
            }
        }
        else if(selectedSquareY==targetSquareY){
            if(selectedSquareX<targetSquareX){
                for(int i=selectedSquareX+1;i<targetSquareX;i++){
                    if(pieces[i][selectedSquareY]!=null)
                        return false;
                }
            }
            else{
                for(int i=selectedSquareX-1;i>targetSquareX;i--){
                    if(pieces[i][selectedSquareY]!=null)
                        return false;
                }
            }
        }
        return true;
    }

    public boolean bishopChecker(Piece p,int targetSquareX,int targetSquareY,int selectedSquareX,int selectedSquareY){
        if(selectedSquareX<targetSquareX){
            if(selectedSquareY<targetSquareY){
                for(int i=1;i<targetSquareY-selectedSquareY;i++){
                    if(pieces[selectedSquareX+i][selectedSquareY+i]!=null)
                        return false;
                }
            }
            else{
                for(int i=1;i<selectedSquareY-targetSquareY;i++){
                    if(pieces[selectedSquareX+i][selectedSquareY-i]!=null)
                        return false;
                }
            }
        }
        else{
            if(selectedSquareY<targetSquareY){
                for(int i=1;i<targetSquareY-selectedSquareY;i++){
                    if(pieces[selectedSquareX-i][selectedSquareY+i]!=null)
                        return false;
                }
            }
            else{
                for(int i=1;i<selectedSquareY-targetSquareY;i++){
                    if(pieces[selectedSquareX-i][selectedSquareY-i]!=null)
                        return false;
                }
            }
        }
        return true;
    }

}