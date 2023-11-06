package ui;

import javax.swing.*;


/**
 * The main application window.
 *
 * IMPORTANT: Please do not modify this class in any way,
 * it will be reset when grading your project.
 */
public class ApplicationWindow {

	private JFrame frame;
	private GridPanel gridPanel;

	public ApplicationWindow(GridPanel gridPanel) {
		this.gridPanel = gridPanel;
	    initialize();
	}

	private void initialize() {
		frame = new JFrame();
		frame.setResizable(false);
		frame.setBounds(50, 50, 500, 520);
		frame.setDefaultCloseOperation(WindowConstants.EXIT_ON_CLOSE);
		frame.getContentPane().add(gridPanel);
		frame.pack();
	}

	public JFrame getFrame() {
	    return frame;
    }

}
