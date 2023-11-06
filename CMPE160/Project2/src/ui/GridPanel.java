package ui;

import javax.swing.*;
import java.awt.*;
import java.awt.image.BufferedImage;


/**
 * A drawable panel structured as a grid.
 * Provides some drawing methods suitable for pixel-like game entities.
 *
 * IMPORTANT: Please do not modify this class in any way,
 * it will be reset when grading your project.
 */
public class GridPanel extends JPanel {

    private final int gamePanelWidth;
    private final int gamePanelHeight;

    private BufferedImage gameImage;

    private int gridSquareSize;

    /**
     * Constructs a grid panel that can be drawn on
     * @param gridWidth width of the grid
     * @param gridHeight height of the grid
     * @param gridSquareSize size of a grid square in pixels
     */
    public GridPanel(int gridWidth, int gridHeight, int gridSquareSize) {
        this.gridSquareSize = gridSquareSize;
        gamePanelWidth = gridWidth * gridSquareSize;
        gamePanelHeight = gridHeight * gridSquareSize;
        gameImage = new BufferedImage(gamePanelWidth, gamePanelHeight, BufferedImage.TYPE_INT_ARGB);
        setBackground(Color.WHITE);
    }

    @Override
    public Dimension getPreferredSize() {
        return new Dimension(gamePanelWidth, gamePanelHeight);
    }

    @Override
    protected void paintComponent(Graphics g) {
        super.paintComponent(g);
        if (gameImage != null) {
            g.drawImage(gameImage, 0, 0, null);
        }
    }

    /**
     * Repaints the panel to white
     */
    public void clearCanvas() {
        Graphics g = gameImage.getGraphics();
        g.setColor(Color.WHITE);
        g.fillRect(0, 0, gameImage.getWidth(), getHeight());
        g.dispose();
    }

    /**
     * Returns the number of grid squares along the width
     * @return grid width
     */
    public int getGridWidth() {
        return gamePanelWidth / gridSquareSize;
    }

    /**
     * Returns the number of grid squares along the height
     * @return grid height
     */
    public int getGridHeight() {
        return gamePanelHeight / gridSquareSize;
    }

    /**
     * Draws gridlines
     */
    public void drawGrid() {
        Graphics g = gameImage.getGraphics();
        g.setColor(Color.LIGHT_GRAY);

        // vertical grid
        for (int i = 0; i < gamePanelWidth / gridSquareSize; i++) {
            int lineX = i * gridSquareSize;
            g.drawLine(lineX, 0, lineX, gamePanelHeight);
        }
        // horizontal grid
        for (int i = 0; i < gamePanelHeight / gridSquareSize; i++) {
            int lineY = i * (gridSquareSize);
            g.drawLine(0, lineY, gamePanelWidth, lineY);
        }
        g.dispose();
    }

    /**
     * Draws a filled square in the given grid position
     * @param gridX x position
     * @param gridY y position
     * @param color fill color of the square
     */
    public void drawSquare(int gridX, int gridY, Color color) {
        if (gridX < 0 || gridY < 0 ||
                gridX >= gamePanelWidth / gridSquareSize || gridY >= gamePanelHeight / gridSquareSize) {
            return;
        }
        Graphics g = gameImage.getGraphics();
        g.setColor(color);
        int x = gridX * gridSquareSize + 1;
        int y = gridY * gridSquareSize + 1;
        g.fillRect(x, y, gridSquareSize - 1, gridSquareSize - 1);
        g.dispose();
    }

    /**
     * Draws a small filled square in the given grid position
     * @param gridX x position
     * @param gridY y position
     * @param color fill color of the square
     */
    public void drawSmallSquare(int gridX, int gridY, Color color) {
        if (gridX < 0 || gridY < 0 ||
                gridX >= gamePanelWidth / gridSquareSize || gridY >= gamePanelHeight / gridSquareSize) {
            return;
        }
        Graphics g = gameImage.getGraphics();
        g.setColor(color);
        int x = gridX * gridSquareSize + 3;
        int y = gridY * gridSquareSize + 3;
        g.fillRect(x, y, gridSquareSize - 5, gridSquareSize - 5);
        g.dispose();
    }

}
